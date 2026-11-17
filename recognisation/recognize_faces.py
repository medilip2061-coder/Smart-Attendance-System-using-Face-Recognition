
import cv2
import json
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "lbph_model.yml"
LABELS_PATH = MODEL_DIR / "labels.json"
CASCADE_PATH = MODEL_DIR / "haarcascade_frontalface_default.xml"

# Load trained LBPH model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(str(MODEL_PATH))

# Load student labels
with open(LABELS_PATH, "r") as file:
    labels = json.load(file)

# Load face detector
face_detector = cv2.CascadeClassifier(str(CASCADE_PATH))

if face_detector.empty():
    raise RuntimeError("Could not load Haar Cascade model!")

# Open webcam
# Change 1 to 0 if your external webcam does not open
camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("Camera not found. Try camera index 0.")
    exit()

print("Live face recognition started!")
print("Press Q to exit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read camera frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if str(label) in labels and confidence < 75:
            student_id = labels[str(label)]
            display_text = f"Recognized: {student_id}"
            color = (0, 255, 0)
        else:
            display_text = "Unknown Student"
            color = (0, 0, 255)

        cv2.rectangle(
            frame, (x, y), (x+w, y+h), color, 2
        )

        cv2.putText(
            frame,
            display_text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    cv2.imshow("Smart Attendance - Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

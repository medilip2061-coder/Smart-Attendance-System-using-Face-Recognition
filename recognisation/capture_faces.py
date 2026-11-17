
import cv2
import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "attendance.db"
FACE_DIR = BASE_DIR / "data" / "faces"

FACE_DIR.mkdir(parents=True, exist_ok=True)

# Load face detection model
cascade_path = Path(__file__).resolve().parent / "models" / "haarcascade_frontalface_default.xml"

face_detector = cv2.CascadeClassifier(str(cascade_path))

if face_detector.empty():
    raise RuntimeError("Could not load face detection model!")


def student_exists(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM students WHERE student_id = ?",
        (student_id,)
    )

    result = cursor.fetchone()
    conn.close()

    return result


def capture_faces():
    print("\n===== FACE CAPTURE SYSTEM =====")

    student_id = input("Enter Student ID: ").strip()

    student = student_exists(student_id)

    if student is None:
        print("Student not found! Register the student first.")
        return

    student_name = student[0]

    print("Student:", student_name)
    print("Camera is starting...")

    # Create student folder
    student_folder = FACE_DIR / student_id
    student_folder.mkdir(parents=True, exist_ok=True)

    # Open webcam
    # On this Windows machine the built-in camera is device1.
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Camera not detected!")
        return

    count = len(list(student_folder.glob("*.jpg")))
    max_images = 30

    print("\nInstructions:")
    print("1. Look directly at the camera.")
    print("2. Press SPACE to capture a face.")
    print("3. Change your head angle slightly between captures.")
    print("4. Press Q to finish.")

    try:
        while count < max_images:

            success, frame = camera.read()

            if not success:
                print("Cannot read camera!")
                break

            gray = cv2.cvtColor(
                frame, cv2.COLOR_BGR2GRAY
            )

            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(80, 80)
            )

            # Display detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                frame,
                f"Student: {student_name}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Captured: {count}/{max_images}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "Student Face Capture",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            # Capture face using SPACE
            if key == 32:

                if len(faces) == 0:
                    print("No face detected. Try again.")
                    continue

                if len(faces) > 1:
                    print("Only one person should be in the frame.")
                    continue

                x, y, w, h = faces[0]

                face = gray[y:y+h, x:x+w]

                face = cv2.resize(face, (200, 200))

                count += 1

                filename = (
                    student_folder
                    / f"{student_id}_{count:02d}.jpg"
                )

                cv2.imwrite(str(filename), face)

                print(
                    f"Image {count}/{max_images} saved!"
                )

            # Exit using Q
            elif key == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    print("\nFace capture finished.")
    print(f"Total images: {count}")
    print(f"Saved in: {student_folder}")


if __name__ == "__main__":
    capture_faces()


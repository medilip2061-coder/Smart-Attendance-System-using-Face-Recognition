
import cv2
import json
import numpy as np
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FACE_DIR = BASE_DIR / "data" / "faces"
MODEL_DIR = Path(__file__).resolve().parent / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "lbph_model.yml"
LABELS_PATH = MODEL_DIR / "labels.json"


def train_model():

    print("===== LBPH MODEL TRAINING =====")

    faces = []
    labels = []
    label_map = {}

    current_label = 0

    # Check dataset folder
    if not FACE_DIR.exists():
        print("Face dataset folder not found!")
        return

    # Read each student's folder
    for student_folder in FACE_DIR.iterdir():

        if not student_folder.is_dir():
            continue

        student_id = student_folder.name
        image_count = 0

        label_map[str(current_label)] = student_id

        for image_path in student_folder.iterdir():

            if image_path.suffix.lower() not in [
                ".jpg", ".jpeg", ".png"
            ]:
                continue

            image = cv2.imread(
                str(image_path),
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                print(f"Skipping unreadable image: {image_path.name}")
                continue

            image = cv2.resize(image, (200, 200))

            faces.append(image)
            labels.append(current_label)

            image_count += 1

        print(
            f"Student ID: {student_id} | "
            f"Images loaded: {image_count}"
        )

        if image_count > 0:
            current_label += 1
        else:
            label_map.pop(str(current_label), None)

    # Check training data
    if len(faces) == 0:
        print("No face images found!")
        return

    # Create LBPH recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8
    )

    # Train model
    print("\nTraining LBPH model...")

    recognizer.train(
        faces,
        np.array(labels, dtype=np.int32)
    )

    # Save model
    recognizer.write(str(MODEL_PATH))

    # Save student label mapping
    with open(LABELS_PATH, "w") as file:
        json.dump(label_map, file, indent=4)

    print("\n===== TRAINING COMPLETED =====")
    print(f"Total images: {len(faces)}")
    print(f"Total students: {len(label_map)}")
    print(f"Model saved: {MODEL_PATH}")
    print(f"Labels saved: {LABELS_PATH}")


if __name__ == "__main__":
    train_model()

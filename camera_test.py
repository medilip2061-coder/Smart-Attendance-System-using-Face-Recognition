
import cv2

camera_indexes = [0, 1, 2]

for camera_index in camera_indexes:
    print(f"Testing camera index: {camera_index}")

    camera = cv2.VideoCapture(camera_index,cv2.CAP_DSHOW)

    if not camera.isOpened():
        print(f"Camera {camera_index} could not open.")
        camera.release()
        continue

    print(f"Camera {camera_index} opened successfully.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Could not read camera frame.")
            break

        cv2.imshow(
            f"Camera Test - Index {camera_index}",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print(f"Finished testing camera {camera_index}.")

print("All camera tests finished.")

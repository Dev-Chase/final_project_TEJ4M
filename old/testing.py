import cv2

# Initialize the camera (0 is usually the default webcam)
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    raise RuntimeError("Cannot open camera")

print("Press 's' to save a picture and 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Display the live feed
    cv2.imshow('Camera Feed', frame)

    # Check for key presses
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        # Quit on 'q' press
        break
    elif k == ord('s'):
        # Save image on 's' press
        img_name = "capture.png"
        cv2.imwrite(img_name, frame)
        print(f"Image saved as {img_name}")
        break

# Release the capture object and close windows
cap.release()
cv2.destroyAllWindows()

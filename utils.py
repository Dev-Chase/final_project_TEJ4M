import cv2
import os
# import picamera2
import pickle
import sys
import time

CV_SCALER = 5

# TODO: Separate files according to these categories:
# The CLI, the inital image capturing, the model training, the verification of a person, hardware interaction (this last one can be incoporated into others if necessary), CSV or cloud stuff if being done

# Camera and General Running
def load_encodings(known_face_encodings, known_face_names, override):
    if not known_face_encodings or not known_face_names or override:
        print("[INFO] loading encodings...")
        with open("encodings.pickle", "rb") as f:
            data = pickle.loads(f.read())
        return data["encodings"], data["names"]

    return known_face_encodings, known_face_names

def init_camera(cam, CAM_I):
    if not (not cam):
        return cam

    # Initialize the camera
    # For Raspberry Pi:
    # picam2 = Picamera2()
    # picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
    # picam2.start()
    # time.sleep(2)

    # return picam2

    # For macOS:
    cam = cv2.VideoCapture(CAM_I)
    if not cam.isOpened():
        print("Cannot open camera")
        sys.exit()

    return cam

def clean_up(cam):
    cv2.destroyAllWindows()
    cv2.waitKey(1) # Let OpenCV process the window close event

    if not cam:
        return

    # For macOS:
    cam.release()

    # For Raspberry Pi:
    # picam2.stop()

    return None

def capture_frame(cam, CAM_I):
    cam = init_camera(cam, CAM_I)

    # For macOS:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        sys.exit()

    return frame

    # For Raspberry Pi:
    # frame = picam2.capture_array()
    # return frame

# Returns frame_count, start_time, fps
def calculate_fps(frame_count, start_time, fps):
    frame_count = frame_count + 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
    return frame_count, start_time, fps

def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

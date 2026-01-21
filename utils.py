import cv2
import os
# import picamera2
import sys
import time

CV_SCALER = 5
ENCODINGS_FILE = "encodings.pickle"
PEOPLE_DATA_FILE = "people.pickle"
DATASET_FOLDER = "dataset"

# Data (BGR)
colours = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (244, 42, 3),
    "white": (255, 255, 255)
}

# Camera and General Running
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_formatted_time(given_time, date=False):
    local_time = time.localtime(given_time)
    if date:
        format_str = "%Y-%m-%d %H:%M:%S"
    else:
        format_str = "%H:%M:%S"
    return time.strftime(format_str, local_time)


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

def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

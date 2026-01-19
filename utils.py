import cv2
import os
# import picamera2
import sys
import time

CV_SCALER = 5
ENCODINGS_FILE = "encodings.pickle"
PEOPLE_DATA_FILE = "people.pickle"

#TODO: consider using classes

# TODO: Separate files according to these categories:
# The CLI, the inital image capturing, the model training, the verification of a person, hardware interaction (this last one can be incoporated into others if necessary), CSV or cloud stuff if being done

# Camera and General Running
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Imagining that there are two pickle files:
# One that contains the data for the people themselves
#   - each name has its own dict with optional titles and other info
#   - format is like this for the file itself {"people": [{"name": name, "info":[titles/info]}]}

# NOTE: THIS IS THE ONE WE'RE WORKING WITH IN THIS FILE *THIS ALONE*
# One that contains the encodings for the people (associated with a name)
#   - each name has a list of associated encodings
#   - format is like this for the file itself {"encodings": [{"name": name, "encodings": [encodings]}]}

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

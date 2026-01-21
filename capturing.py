import cv2
from datetime import datetime
import os
import time
from utils import *

def create_person_folder(name):
    create_folder(DATASET_FOLDER)
    
    person_folder = os.path.join(DATASET_FOLDER, name)
    create_folder(person_folder)
    return person_folder

def capture_photos(name, cam, CAM_I, hardware):
    cam = init_camera(cam, CAM_I)

    # Name will be formated as firstname_lastname in lowercase
    # name = "_".join(part.lower() for part in input("What is your full name?: ").split())

    folder = create_person_folder(name)
    print(f"Taking photos for {name}. Press SPACE to capture, 'q' to quit.")
    photo_count = 0
    
    while True:
        hardware.set_lights(False, True)

        # Capture frame from Camera
        frame = capture_frame(cam, CAM_I)
        
        # Display the frame
        cv2.imshow("Capture", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space key
            photo_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            filepath = os.path.join(folder, filename)
            cv2.imwrite(filepath, frame)
            print(f"Photo {photo_count} saved: {filepath}")
            hardware.set_lights(True, False)
            time.sleep(1.0)
        
        elif key == ord('q'):  # Q key
            break
    
    print(f"Photo capture completed. {photo_count} photos saved for {name}.")
    hardware.set_lights(False, False)

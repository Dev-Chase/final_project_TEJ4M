from utils import *
import os
from datetime import datetime

def create_folder(name):
    dataset_folder = "dataset"
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    person_folder = os.path.join(dataset_folder, name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    return person_folder

def capture_photos(cam):
    # Name will be formated as firstname_lastname in lowercase
    name = "_".join(part.lower() for part in input("What is your full name?: ").split())
    folder = create_folder(name)
    print(f"Taking photos for {name}. Press SPACE to capture, 'q' to quit.")
    photo_count = 0
    
    while True:
        # Capture frame from Pi Camera
        frame = capture_frame(cam)
        
        # Display the frame
        cv2.imshow('Capture', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space key
            photo_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            filepath = os.path.join(folder, filename)
            cv2.imwrite(filepath, frame)
            print(f"Photo {photo_count} saved: {filepath}")
        
        elif key == ord('q'):  # Q key
            break
    
    print(f"Photo capture completed. {photo_count} photos saved for {name}.")

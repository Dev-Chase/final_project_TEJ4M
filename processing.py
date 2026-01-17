import face_recognition
import numpy as np
from utils import *

VERIFICATION_TIME = 4.0 # seconds
VERIFICATION_CV_SCALER = 2

# NOTE: Returns face_locations, face_encodings, and face_names
# cv_scaler must be a whole number
def process_frame(frame, known_face_encodings, known_face_names, known_face_ids, cv_scaler = CV_SCALER):
    known_face_encodings, known_face_names, known_face_ids = load_encodings(known_face_encodings, known_face_names, known_face_ids, False)

    # Resize the frame using cv_scaler to increase performance (less pixels processed, less time spent)
    resized_frame = cv2.resize(frame, (0, 0), fx = (1/cv_scaler), fy = (1/cv_scaler))
    
    # Convert the image from BGR to RGB colour space, the facial recognition library uses RGB, OpenCV uses BGR
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
    
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "unknown"
        
        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    return face_locations, face_encodings, face_names

def get_current_person(cam, CAM_I, hardware, known_face_encodings, known_face_names, known_face_ids, cv_scaler=VERIFICATION_CV_SCALER):
    cam = init_camera(cam, CAM_I)
    time.sleep(1.0)
    start_time = time.time()

    # Get and process the current frame
    frame = capture_frame(cam, CAM_I)
    _, _, face_names = process_frame(frame, known_face_encodings, known_face_names, known_face_ids, cv_scaler)

    print(f"Original names: {face_names}")
    last_face_names = face_names

    while time.time() - start_time < VERIFICATION_TIME:
        # Get and process the current frame
        frame = capture_frame(cam, CAM_I)
        _, _, face_names = process_frame(frame, known_face_encodings, known_face_names, known_face_ids, cv_scaler)
        print(face_names)

        # Check for invalidations of the current verification
        if len(face_names) == 0:
            print("I couldn't detect anyone in the frame.")
            hardware.fail_sound()
            return None

        if len(face_names) > 1:
            print("Only one person in frame at a time please.")
            hardware.fail_sound()
            return None

        if last_face_names != face_names:
            print("Something changed while I was verifying, please try again.")
            hardware.fail_sound()
            return None

        last_face_names = face_names

    hardware.set_lights(False, True)
    hardware.success_sound()
    return face_names[0]

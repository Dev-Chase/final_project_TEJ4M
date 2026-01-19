import face_recognition
from utils import *

VERIFICATION_TIME = 4.0 # seconds
VERIFICATION_CV_SCALER = 2

# TODO: reorganize so it goes through person at a time instead of encoding

# NOTE: Returns face_locations, face_encodings, and face_names
# cv_scaler must be a whole number
def process_frame(frame, known_people, cv_scaler = CV_SCALER):
    # Resize the frame using cv_scaler to increase performance (less pixels processed, less time spent)
    resized_frame = cv2.resize(frame, (0, 0), fx = (1/cv_scaler), fy = (1/cv_scaler))
    
    # Convert the image from BGR to RGB colour space, the facial recognition library uses RGB, OpenCV uses BGR
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
    
    face_people = []
    for face_encoding in face_encodings:
        tolerance = 0.4

        # Find the person with the closest looking face
        lowest_distance = tolerance + 0.1
        current_match = None
        for person in known_people:
            if len(person.encodings) == 0:
                continue

            person_min_distance = min(face_recognition.face_distance(person.encodings, face_encoding))
            if person_min_distance < lowest_distance:
                lowest_distance = person_min_distance
                current_match = person


        # Compare the closest looking face to the tolerance
        if lowest_distance > tolerance:
            current_match = None
        
        # Use the known face with the smallest distance to the new face
        face_people.append(current_match)

    return face_locations, face_encodings, face_people


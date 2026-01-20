import face_recognition
from utils import *
from drawing import draw_results

VERIFICATION_TIME = 3.0 # seconds
VERIFICATION_CV_SCALER = 2
VERIFICATION_TOLERANCE = 0.4

# TODO: reorganize so it goes through person at a time instead of encoding

# NOTE: Returns face_locations, face_encodings, and face_names
# cv_scaler must be a whole number
def process_frame(frame, known_people, cv_scaler = CV_SCALER, tolerance=0.6):
    # Resize the frame using cv_scaler to increase performance (less pixels processed, less time spent)
    resized_frame = cv2.resize(frame, (0, 0), fx = (1/cv_scaler), fy = (1/cv_scaler))
    
    # Convert the image from BGR to RGB colour space, the facial recognition library uses RGB, OpenCV uses BGR
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
    
    face_people = []
    for face_encoding in face_encodings:
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

def live_preview(cam, CAM_I, known_people, cv_scaler = CV_SCALER):
    cam = init_camera(cam, CAM_I)

    while True:
        # Capture frame from Camera
        frame = capture_frame(cam, CAM_I)

        face_locations, _, face_people = process_frame(frame, known_people, cv_scaler)

        draw_results(frame, face_locations, face_people, cv_scaler)
        
        # Display the frame
        cv2.imshow("Preview", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Q key
            break


def verify_person(cam, CAM_I, hardware, known_people, cv_scaler=VERIFICATION_CV_SCALER):
    cam = init_camera(cam, CAM_I)
    start_time = time.time()

    # Get and process the current frame
    frame = capture_frame(cam, CAM_I)
    _, _, face_people = process_frame(frame, known_people, cv_scaler)

    print(f"Original People: {face_people}")
    last_face_people = face_people

    while time.time() - start_time < VERIFICATION_TIME:
        # Get and process the current frame
        frame = capture_frame(cam, CAM_I)
        face_locations, _, face_people = process_frame(frame, known_people, cv_scaler, VERIFICATION_TOLERANCE)

        draw_results(frame, face_locations, face_people, cv_scaler, colours["green"])

        # Check for invalidations of the current verification
        if len(face_people) == 0:
            print("I couldn't detect anyone in the frame.")
            hardware.fail_sound()
            return None

        if len(face_people) > 1:
            print("Only one person in frame at a time please.")
            hardware.fail_sound()
            return None

        if last_face_people != face_people:
            print("Something changed while I was verifying, please try again.")
            hardware.fail_sound()
            return None

        # Display the frame
        cv2.imshow("Attendance", frame)

        last_face_people = face_people

    hardware.set_lights(False, True)
    hardware.success_sound()
    return face_people[0]

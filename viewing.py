from processing import *
from utils import *

# Drawing
def draw_results(frame, face_locations, face_people, cv_scaler=CV_SCALER):
    # Display the results
    for (top, right, bottom, left), person in zip(face_locations, face_people):
        name = "Unkown"
        colour = (244, 42, 3)
        if person:
            name = person.get_full_name_text()
            if person.is_threat():
                colour = (0, 0, 255)
                name, _ = person.get_separate_names()
                name = name + " (THREAT!)"

        # Scale back up face locations since the frame we detected in was scaled
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler
        
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), colour, 3)
        
        # Draw a label with a name below the face

        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), colour, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)


def draw_fps(display_frame, fps):
    # Attach FPS counter to the text and boxes
    cv2.putText(display_frame, f"FPS: {fps:.1f}", (display_frame.shape[1] - 150, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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


# TODO: fix/implement (links to take_attendance)
def wait_for_person(cam, CAM_I, hardware, known_people, cv_scaler=VERIFICATION_CV_SCALER):
    cam = init_camera(cam, CAM_I)
    time.sleep(1.0)
    start_time = time.time()

    # Get and process the current frame
    frame = capture_frame(cam, CAM_I)
    _, _, face_people = process_frame(frame, known_people, cv_scaler)

    print(f"Original People: {face_people}")
    last_face_people = face_people

    while time.time() - start_time < VERIFICATION_TIME:
        # Get and process the current frame
        frame = capture_frame(cam, CAM_I)
        _, _, face_people = process_frame(frame, known_people, cv_scaler)
        print(face_people)

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
        cv2.imshow("Preview", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Q key
            break

        last_face_people = face_people

    hardware.set_lights(False, True)
    hardware.success_sound()
    return face_people[0]

from processing import *
from utils import *

# Drawing
def draw_results(frame, face_locations, face_names, cv_scaler=CV_SCALER):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler
        
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)


def draw_fps(display_frame, fps):
    # Attach FPS counter to the text and boxes
    cv2.putText(display_frame, f"FPS: {fps:.1f}", (display_frame.shape[1] - 150, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def live_preview(cam, CAM_I, known_face_encodings, known_face_names, cv_scaler = CV_SCALER):
    known_face_encodings, known_face_names = load_encodings(known_face_encodings, known_face_names, False)
    cam = init_camera(cam, CAM_I)

    while True:
        # Capture frame from Camera
        frame = capture_frame(cam, CAM_I)

        face_locations, face_encodings, face_names = process_frame(frame, known_face_encodings, known_face_names)
        draw_results(frame, face_locations, face_names)
        
        # Display the frame
        cv2.imshow("Preview", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Q key
            break


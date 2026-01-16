import cv2
from utils import *
from processing import get_current_person

if __name__ == "__main__":
    # Load pre-trained face encodings
    known_face_encodings, known_face_names = load_encodings(None, None)

    # Initialize Camera
    cam = init_camera()

    # Input Loop
    try:
        while True:
            inp = input("What do you want to do?: ")

            if inp == "reco" or inp == "recognize":
                current_person = get_current_person(cam, known_face_encodings, known_face_names)
                print(f"Current Person is {current_person}")
            elif inp == "clear":
                clear_console()
            elif inp == "break" or inp == "exit":
                break
            else:
                print(f"{inp} is not a valid option, try something else")
    except KeyboardInterrupt:
        pass
    except Exception:
        print("Something unexpected happened!")

    print("Cleaning things up")
    cam.release()
    cv2.destroyAllWindows()


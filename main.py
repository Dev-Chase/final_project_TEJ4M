from image_capture import *
from model_training import *
from processing import *
from utils import *
from viewing import live_preview

if __name__ == "__main__":
    # Load pre-trained face encodings
    known_face_encodings, known_face_names = load_encodings(None, None, True)

    # Initialize Camera
    CAM_I = int(input("What camera index are you using? (0 for plugged-in webcam, 1 for built-in): "))
    cam = init_camera(None, CAM_I)

    # TODO: add option for replacing a person/updating their photos and/or deleting a person from the dataset

    # Input Loop
    try:
        while True:
            inp = input("What do you want to do?: ")

            if inp == "capture":
                capture_photos(cam, CAM_I)
                cam = clean_up(cam) # TODO: review if cam is mutable and altered by clean_up for both rpi and macOS (so that clean_up can be done from any function and not in the main one)
            elif inp == "clean":
                cam = clean_up(cam)
            elif inp == "train":
                cam = clean_up(cam)
                train_model()
                known_face_encodings, known_face_names = load_encodings(known_face_names, known_face_encodings, True)
            elif inp == "reco" or inp == "recognize":
                current_person = get_current_person(cam, CAM_I, known_face_encodings, known_face_names)
                print(f"Current Person is {current_person}")
            elif inp == "preview":
                # Get and process frame
                live_preview(cam, CAM_I,  known_face_encodings, known_face_names)
                cam = clean_up(cam)
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
    cam = clean_up(cam)


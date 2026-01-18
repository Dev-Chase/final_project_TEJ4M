from hardware import Hardware
from capturing import *
from training import *
from processing import *
from utils import *
from viewing import live_preview

def print_options():
    print("--------------------------------")
    print("Options:")
    print("ls/list - List options")
    print("cv - Set the CV Scaler (how much the image is scaled down)")
    print("people - See the currently saved people")
    print("capt(ure) - Take photos for a person to train the model on their face")
    print("train - Train the model on the faces in the dataset folder")
    print("reco(gnize) - Validate a person in frame")
    print("prev(iew) - Show a live preview of all the people in frame")
    print("clean - Close all windows and Stop Camera")
    print("clear - Clear the console")
    print("break/exit/stop - Stop the Program")

if __name__ == "__main__":
    # Load pre-trained face encodings
    if not Path(ENCODINGS_FILE_PATH).is_file():
        train_model()
    known_people = load_people(None, True)
    # TODO: handle people_data as seen in training.py

    # Initialize Hardware/GPIO
    hardware = Hardware(testing=True) # TODO: remove testing for raspberry pi

    # Initialize Camera
    CAM_I = int(input("What camera index are you using? (0 for plugged-in webcam, 1 for built-in): "))
    cam = init_camera(None, CAM_I)

    cv_scaler = CV_SCALER
    # TODO: add option for replacing a person/updating their photos and/or deleting a person from the dataset

    # Input Loop
    try:
        print("Enter 'list' to list options")
        while True:
            inp = input("What do you want to do?: ")

            if inp == "list" or inp == "ls":
                print_options()
            elif inp == "cv":
                cv_scaler = int(input("What do you want to set the CV Scaler to? (must be a whole number): "))
                print(f"Set CV Scaler to {cv_scaler}")
            elif inp == "people":
                known_people = load_people(known_people)
                print()
            elif inp == "capture" or inp == "capt":
                capture_photos(cam, CAM_I, hardware)
                cam = clean_up(cam) # TODO: review if cam is mutable and altered by clean_up for both rpi and macOS (so that clean_up can be done from any function and not in the main one)
                print("Enter 'train' to train the model on the pictures")
            elif inp == "train":
                cam = clean_up(cam)
                train_model()
                known_people = load_people(known_people, True)
            elif inp == "reco" or inp == "recognize":
                current_person = get_current_person(cam, CAM_I, hardware, known_people)
                print(f"Current Person is {current_person}")
            elif inp == "preview" or inp == "prev":
                # Get and process frame
                live_preview(cam, CAM_I,  known_people, cv_scaler)
                cam = clean_up(cam)
            elif inp == "clean":
                cam = clean_up(cam)
            elif inp == "clear":
                clear_console()
            elif inp == "break" or inp == "exit" or inp == "stop":
                break
            else:
                print(f"{inp} is not a valid option, try something else")
    except KeyboardInterrupt:
        pass
    except Exception:
        print("Something unexpected happened!")

    print("Cleaning things up")
    cam = clean_up(cam)


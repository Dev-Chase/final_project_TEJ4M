from hardware import Hardware
from capturing import *
from training import *
from person import Person
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
    # Get Information on People
    people = []
    if Path(PEOPLE_DATA_FILE).is_file():
        Person.load_people_from_file(people)

    # Load pre-trained face encodings
    if not Path(ENCODINGS_FILE).is_file():
        train_model()
    Person.load_encodings(people)

    # Initialize Hardware/GPIO
    hardware = Hardware(testing=True) # TODO: remove testing for raspberry pi

    # Initialize Camera
    CAM_I = int(input("What camera index are you using? (0 for plugged-in webcam, 1 for built-in): "))
    cam = init_camera(None, CAM_I)

    cv_scaler = CV_SCALER
    # TODO: add option for replacing a person/updating their photos and/or deleting a person from the dataset
    # NOTE: it would have to retrain the model afterwards

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
                print("Here are the people I have saved")
                for person in people:
                    print("------------------")
                    person.print_info()
            elif inp == "capture" or inp == "capt":
                person_name = Person.get_aggregate_name(input("Who's pictures am I taking (full name)?: "))
                person = Person.get_person(people, person_name)
                if not person:
                    inp = input("That person is not yet saved. Do you want me to add them (y/n)?: ")
                    if inp != "y" and inp != "Y":
                        continue

                    people.append(Person(person_name))

                capture_photos(person_name, cam, CAM_I, hardware)
                cam = clean_up(cam) # TODO: review if cam is mutable and altered by clean_up for both rpi and macOS (so that clean_up can be done from any function and not in the main one)
                # train_model()
                print("Enter 'train' to train the model on the new pictures")
            elif inp == "train":
                cam = clean_up(cam)
                train_model()
                Person.load_encodings(people, True)
            elif inp == "reco" or inp == "recognize":
                current_person = get_current_person(cam, CAM_I, hardware, people)
                if current_person:
                    print("Current person is:")
                    current_person.print_info()
            elif inp == "preview" or inp == "prev":
                # Get and process frame
                live_preview(cam, CAM_I,  people, cv_scaler)
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

    print("Saving Changes to People")
    Person.save_people_to_file(people)

    print("\nCleaning things up")
    cam = clean_up(cam)


from capturing import *
from cloud import Cloud
from drawing import *
from group import Group
from hardware import Hardware
import os
from person import Person
from processing import *
import shutil
from training import *
from utils import *

def print_options():
    print("--------------------------------")
    print("Options:")
    print("ls/list - List options")
    print("cv - Set the CV Scaler (how much the image is scaled down)")
    print("people - See the currently saved people")
    print("add to - Add a person to a group")
    print("rem(ove) from - Remove a person from a group")
    print("rem(ove) - Remove a person from the dataset")
    print("capt(ure) - Take photos for a person to train the model on their face")
    print("train - Train the model on the faces in the dataset folder")
    print("save - Save People Information")
    print("prev(iew) - Show a live preview of all the people in frame")
    print("clean - Close all windows and Stop Camera")
    print("clear - Clear the console")
    print("break/exit/stop - Stop the Program")

if __name__ == "__main__":
    # Group/Class Information
    groups = []

    # Get Information on People
    people = []
    if Path(PEOPLE_DATA_FILE).is_file():
        Person.load_people_from_file(people, groups)

    # Load pre-trained face encodings
    if not Path(ENCODINGS_FILE).is_file():
        train_model()
    Person.load_encodings(people)

    # Initialize Cloud Handler
    cloud = Cloud()

    # Initialize Hardware/GPIO
    hardware = Hardware(testing=True) # TODO: remove testing for raspberry pi

    # Initialize Camera
    CAM_I = int(input("What camera index are you using? (0 for plugged-in webcam, 1 for built-in): "))
    cam = init_camera(None, CAM_I)

    cv_scaler = CV_SCALER

    # TODO: add removing someone from a group
    
    # Input Loop
    try:
        print("Enter 'list' to list options")
        while True:
            inp = input("What do you want to do?: ")

            if inp == "list" or inp == "ls":
                print_options()
            #TODO: remove this option
            elif inp == "empty":
                for person in people:
                    person.info.clear()
                for group in groups:
                    group.members.clear()
            elif inp == "cv":
                cv_scaler = int(input("What do you want to set the CV Scaler to? (must be a whole number): "))
                print(f"Set CV Scaler to {cv_scaler}")
            elif inp == "att" or inp == "attendance":
                group_name = input("Which group do you want to take attendance for?: ")
                group_names = [group.code for group in groups]
                if not group_name in group_names:
                    print("That group doesn't exist")
                    continue

                group = groups[group_names.index(group_name)]
                ex_start_time = time.time() + 10
                ex_end_time = time.time() + 25 # One minute from now
                attendance_info = group.take_attendance(cam, CAM_I, people, hardware, ex_start_time, ex_end_time, cv_scaler=cv_scaler)
                cam = clean_up(cam)
                time.sleep(0.5)

                inp = input("Do you want to log the attendance sheet in the cloud (Y/n)?: ")
                if inp != "Y" and inp != "y":
                    continue
                cloud.log_attendance(attendance_info)
            elif inp == "people":
                print("Here are the people I have saved")
                for person in people:
                    print("------------------")
                    person.print_info()
            elif inp == "add to":
                person = Person.get_person(people, None, "Who do you want to add to the group (full name)?: ")
                if not person:
                    continue

                label = input(f"What group do you want to add {person.get_full_name_text()} to?: ")
                group_names = [group.code for group in groups]
                if not label in group_names:
                    groups.append(Group(label))
                group_names = [group.code for group in groups]

                group = groups[group_names.index(label)]
                person.add_to_group(group)
            elif inp == "rem from" or inp == "remove from":
                person = Person.get_person(people, None, "Who do you want to remove from the group (full name)?: ")
                if not person:
                    continue

                group_name = input("What group do you want to remove them from?: ")
                if not group_name in person.info:
                    print(f"{person.get_full_name_text()} is not associated with {group_name}")
                    continue
                person.info.pop(person.info.index(group_name))

                group_names = [group.code for group in groups]
                if not group_name in group_names:
                    print(f"{group_name} doesn't exist")
                    continue

                group = groups[group_names.index(group_name)]
                group.remove_member(person.aggregate_name)

            elif inp == "rem" or inp == "remove":
                print(f"Input: {inp}")
                person = Person.get_person(people, None, "Who do you want to remove (full name)?: ")
                if not person:
                    continue

                inp = input(f"Are you sure you want to remove {person.aggregate_name} from the dataset (y/n)?: ")
                if inp != "y" and inp != "Y":
                    print("Alright, cancelling")
                    continue

                person_encodings_folder = person.get_encodings_folder()
                if os.path.exists(person_encodings_folder):
                    shutil.rmtree(person_encodings_folder)
                person_i = people.index(person)
                people.pop(person_i)
                print("Retraining Model")
                train_model()
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
            # TODO: consider removing
            # elif inp == "reco" or inp == "recognize":
            #     current_person = get_current_person(cam, CAM_I, hardware, people)
            #     if current_person:
            #         print("Current person is:")
            #         current_person.print_info()
            elif inp == "preview" or inp == "prev":
                # Get and process frame
                live_preview(cam, CAM_I,  people, cv_scaler)
                cam = clean_up(cam)
            elif inp == "save":
                Person.save_people_to_file(people)
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

    Person.save_people_to_file(people)

    print("\nCleaning things up")
    cam = clean_up(cam)


from hardware import Hardware
from processing import process_frame, verify_person
import time
from utils import *
from drawing import draw_results

# Attendance Codes:
# NOTE: I named it Group so that I wouldn't have a class named Class
class Group:
    def __init__(self, code, members=[]):
        self.code = code
        self.members = []
        self.members.extend(members)

    @staticmethod
    def print_attendance_code_meaning(at_code):
        if at_code == "J":
            print("Justified Absence")
        elif at_code == "R":
            print("Late")
        elif at_code == "A":
            print("Absent")
        elif at_code == "P":
            print("Present")

    def add_member(self, name):
        self.members.append(name)

    # TODO: consider adding separate function to justify an absence
    def take_attendance(self, cam, CAM_I, known_people, hardware, start_time, end_time, justified_people=[], cv_scaler=CV_SCALER):
        cam = init_camera(cam, CAM_I)

        print(f"Taking attendance for {self.code}")
        print(f"The Group starts at {get_formatted_time(start_time)} and ends at {get_formatted_time(end_time)}")
        attendance_info = {}
        for member in self.members:
            attendance_info[member] = {"code": "A"} # Default absent

        for person in justified_people:
            if not person.aggregate_name in self.members:
                print(f"{person.get_full_name_text()} is not a part of {self.code}, so I can't justify their absence")
                continue
            attendance_info[person.aggregate_name] = {"code": "J"}

        while time.time() < end_time:
            # Capture frame from Camera and process it
            frame = capture_frame(cam, CAM_I)
            face_locations, _, face_people = process_frame(frame, known_people, cv_scaler)

            colour = colours["blue"]
            if len(face_people) > 1:
                colour = colours["red"]
            draw_results(frame, face_locations, face_people, cv_scaler, colour)

            # Display the frame
            cv2.imshow("Attendance", frame)
            
            key = cv2.waitKey(1) & 0xFF

            if key == ord('v'):
                check_in_time = time.time()
                person = verify_person(cam, CAM_I, hardware, known_people)
                if not person:
                    continue

                print(f"I found {person.aggregate_name}!")
                if not person.aggregate_name in self.members:
                    print(f"{person.get_full_name_text()} is not a member of {self.code}.")
                    continue

                if attendance_info[person.aggregate_name]["code"] != "A":
                    print(f"{person.get_full_name_text()} has already taken attendance.")
                    continue
                
                code = "P"
                if check_in_time > start_time:
                    code = "R"
                attendance_info[person.aggregate_name] = {"code": code, "time": get_formatted_time(check_in_time, date=True)}

            # TODO: remove q key break or add a way to come back if ended prematurily?
            if key == ord('q'):  # Q key
                break

        print("This is my attendance sheet:")
        print(attendance_info)
        return attendance_info


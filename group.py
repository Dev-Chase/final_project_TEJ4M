from datetime import datetime
from hardware import Hardware
from utils import *

# Attendance Codes:
# NOTE: I named it Group so that I wouldn't have a class named Class
class Group:
    def __init__(self, code, members=[]):
        self.code = code
        self.members = members # List of names

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

    def take_attendance(self, cam, CAM_I, known_people, hardware, start_time, end_time):
        print(f"Taking attendance for {self.code}")
        print(f"The Group starts at {start_time} and ends at {end_time}")
        attendance_info = []
        while datetime.now() < end_time:
            if hardware.is_mock():
                input("Enter anything when you want to take attendance.")

        cam = clean_up(cam)


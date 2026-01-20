from capturing import capture_photos
import pickle
from group import Group
from utils import *

#TODO: write about problem with using the same array from the pickle file for all instances of a person
class Person:
    def __init__(self, aggregate_name, info=[], encodings=[]):
        self.aggregate_name = aggregate_name
        self.first_name, self.last_name = self.get_separate_names()
        self.info = []
        self.info.extend(info)
        self.encodings = []
        self.encodings.extend(encodings)

    # Data Management
    @staticmethod
    def load_people_from_file(people_arr, group_arr):
        group_arr.clear()

        print("[INFO] loading people...")
        with open(PEOPLE_DATA_FILE, "rb") as f:
            people_data = pickle.loads(f.read())

        for person_dict in people_data["people"]:
            # Add Person to Person Array
            person_obj = Person(person_dict["name"], person_dict["info"])
            person_obj.add_to_associated_groups(group_arr)
            people_arr.append(person_obj)

    @staticmethod
    def load_encodings(known_people, override=True):
        print("[INFO] loading encodings...")
        with open(ENCODINGS_FILE, "rb") as f:
            encodings_data = pickle.loads(f.read())

        print("[INFO] adding encodings to associated people")
        for person_dict in encodings_data["encodings"]:
            name = person_dict["name"]
            person = Person.get_person(known_people, name)
            if not person:
                print(f"I made a new person entry for {name}, since there wasn't one already.")
                person = Person(name)
                known_people.append(person)

            if override:
                person.encodings.clear()
            person.encodings.extend(person_dict["encodings"])

    def get_encodings_folder(self):
        return os.path.join(DATASET_FOLDER, self.aggregate_name)

    def get_person_dict(self):
        return {"name": self.aggregate_name, "info": self.info}

    # NOTE: overwrites current people data (assuming that changes aren't made mid execution that aren't reflected in the program's representation of the data)
    @staticmethod
    def save_people_to_file(people):
        people_data = {"people": []}
        for person in people:
            people_data["people"].append(person.get_person_dict())

        print(f"[INFO] saving people information to {PEOPLE_DATA_FILE}")
        with open(PEOPLE_DATA_FILE, "wb") as f:
            f.write(pickle.dumps(people_data))

    # Names
    @staticmethod
    def get_aggregate_name(full_name_text):
        return "_".join(part.lower() for part in full_name_text.split())

    def has_same_name(self, other_name):
        return self.aggregate_name == other_name

    def get_separate_names(self):
        full_name = self.aggregate_name.split("_")
        return full_name[0].capitalize(), full_name[1].capitalize()

    def get_full_name_text(self):
        return " ".join(self.get_separate_names())

    # Helper
    @staticmethod
    def get_person(people, name, inp_str=None):
        if inp_str:
            name = Person.get_aggregate_name(input(inp_str))
        for person in people:
            if person.has_same_name(name):
                return person
        
        print(f"{name} isn't saved")
        return None

    def print_info(self):
        print(f"Name:{self.get_full_name_text()}")
        print(f"Info: {self.info}")
        print(f"N Encodings: {len(self.encodings)}")

    # Groups
    def add_to_associated_groups(self, group_arr):
        for label in self.info:
            associated_group = None
            for group in group_arr:
                if group.code == label:
                    associated_group = group
            
            if not associated_group:
                associated_group = Group(label)
                group_arr.append(associated_group)

            if not self.aggregate_name in associated_group.members:
                associated_group.members.append(self.aggregate_name)

    def add_to_group(self, group):
        group.add_member(self.aggregate_name)
        self.info.append(group.code)

    # Info
    def add_info(self, info):
        self.info.append(info)

    def is_threat(self):
        return "threat" in self.info

    # Pictures
    def take_pictures(self, cam, CAM_I, hardware):
        capture_photos(self.aggregate_name, cam, CAM_I, hardware)

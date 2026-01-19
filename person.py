from capturing import capture_photos
import pickle
from utils import *

class Person:
    def __init__(self, aggregate_name, info=[], encodings=[]):
        self.aggregate_name = aggregate_name
        self.first_name, self.last_name = self.get_separate_names()
        self.info = info
        self.encodings = encodings

    # Data Management
    @staticmethod
    def load_people_from_file(people_arr):
        print("[INFO] loading people...")
        with open(PEOPLE_DATA_FILE, "rb") as f:
            people_data = pickle.loads(f.read())

        for person in people_data["people"]:
            people_arr.append(Person(person["name"], person["info"]))

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
                person.encodings = person_dict["encodings"]
            else:
                person.encodings = person.encodings + person_dict["encodings"]

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
    def get_person(people, name):
        for person in people:
            if person.has_same_name(name):
                return person
        
        return None

    def print_info(self):
        print(f"Name:{self.get_full_name_text()}")
        print(f"Info: {self.info}")

    # Titles

    # Pictures
    def take_pictures(self, cam, CAM_I, hardware):
        capture_photos(self.aggregate_name, cam, CAM_I, hardware)

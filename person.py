from capturing import capture_photos
import pickle
from utils import *

class Person:
    def __init__(self, aggregate_name, titles=[], encodings=[]):
        self.aggregate_name = aggregate_name
        self.first_name, self.last_name = self.get_separate_names()
        self.titles = titles
        self.encodings = encodings

    # File Managment
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
            matching_i, person = Person.get_person(known_people, name)
            if not person:
                print("There were images saved for someone who wasn't yet saved, so I added them.")
                matching_i = len(known_people)
                known_people.append(Person(name))

            if override:
                known_people[matching_i].set_encodings(person_dict["encodings"])
            else:
                known_people[matching_i].add_encodings(person_dict["encodings"])

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
        for person_i, person in enumerate(people):
            if person.has_same_name(name):
                return person_i, person
        
        return -1, None

    # Titles

    # Pictures
    def take_pictures(self, cam, CAM_I, hardware):
        capture_photos(self.aggregate_name, cam, CAM_I, hardware)

    # Encodings
    def set_encodings(self, new_encodings):
        self.encodings = new_encodings

    def add_encodings(self, new_encodings):
        self.encodings = self.encodings + new_encodings
        
    # def get_dict(self):
    #     dict = {"name": self.aggregate_name}
    #     for title in self.titles:
    #         dict[title] = True
    #
    #     return dict

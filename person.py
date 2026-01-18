from utils import *

PEOPLE_DATA_FILE_PATH = "people.pickle"

class Person:
    def __init__(self, aggregate_name, titles=[], encodings=[]):
        self.aggregate_name = aggregate_name
        self.first_name, self.last_name = self.get_separate_name()
        self.titles = titles
        self.encodings = encodings

    @staticmethod
    def get_aggregate_name(first_name, last_name):
        return f"{first_name.lower()}_{last_name.lower()}"

    def get_separate_name(self):
        full_name = self.aggregate_name.split("_")
        return full_name[0], full_name[1]

    def add_encodings(self, new_encodings):
        self.encodings = self.encodings + new_encodings
        
    def get_dict(self):
        dict = {"name": self.aggregate_name}
        for title in self.titles:
            dict[title] = True

        return dict

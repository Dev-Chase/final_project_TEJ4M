import cv2
import face_recognition
from imutils import paths
from pathlib import Path
import pickle
from utils import *


# Imagining that there are two pickle files:
# One that contains the data for the people themselves
#   - each name has its own dict with optional titles and other info
#   - format is like this for the file itself {"people": [{name: {titles}}]}

# NOTE: THIS IS THE ONE WE'RE WORKING WITH IN THIS FILE *THIS ALONE*
# One that contains the encodings for the people (associated with a name)
#   - each name has a list of associated encodings
#   - format is like this for the file itself {"encodings": [{"name": [encodings]}]}

def train_person(name, person_dir):
    # print(f"Processing images for {name}")
    person_dict = {"name": name, "encodings": []}

    person_images = list(paths.list_images(person_dir))
    for (i, image_path) in enumerate(person_images):
        print(f"[INFO] processing image {i + 1} for {name}")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to load image")

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        image_encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in image_encodings:
            person_dict["encodings"].append(encoding)

    return person_dict


# TODO: fix whole UUID system. Find a wholistic solution and write it all down before implementing it

# TODO: consider using separate pickle file for id->names instead of dict of people with associated encodings and an id and name
def train_model():
    print("[INFO] start processing faces...")
    encodings_data = {"people": []}
    people_data = {}
    if Path(PEOPLE_DATA_FILE_PATH).is_file():
        with open(PEOPLE_DATA_FILE_PATH, "rb") as f:
            people_data = pickle.loads(f.read())

    dataset_path = Path("dataset")
    for person_path in dataset_path.iterdir():
        if person_path.is_dir():
            name = person_path.name
            person_dict = train_person(name, person_path)
            encodings_data["people"].append(person_dict)
            people_data[person_dict["id"]]["name"] = name

    print("[INFO] serializing encodings...")
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(encodings_data))

    print("[INFO] Training complete. Encodings saved to 'encodings.pickle'")

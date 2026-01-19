import cv2
import face_recognition
from imutils import paths
from pathlib import Path
import pickle
from utils import *


# Imagining that there are two pickle files:
# One that contains the data for the people themselves
#   - each name has its own dict with optional titles and other info
#   - format is like this for the file itself {"people": [{"name": name, "info":{titles/info}}]}

# NOTE: THIS IS THE ONE WE'RE WORKING WITH IN THIS FILE *THIS ALONE*
# One that contains the encodings for the people (associated with a name)
#   - each name has a list of associated encodings
#   - format is like this for the file itself {"encodings": [{"name": name, "encodings":  [encodings]}]}

def train_person(person_path):
    # print(f"Processing images for {name}")
    name = person_path.name
    person_dict = {"name": name, "encodings": []}

    person_images = list(paths.list_images(person_path))
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

def train_model():
    print("[INFO] start processing faces...")
    encodings_data = {"encodings": []}

    dataset_dir = "dataset"
    create_folder(dataset_dir)
    dataset_path = Path(dataset_dir)
    for person_path in dataset_path.iterdir():
        if person_path.is_dir():
            person_dict = train_person(person_path)
            encodings_data["encodings"].append(person_dict)

    print("[INFO] serializing encodings...")
    with open(ENCODINGS_FILE, "wb") as f:
        f.write(pickle.dumps(encodings_data))

    print(f"[INFO] Training complete. Encodings saved to '{ENCODINGS_FILE}'")

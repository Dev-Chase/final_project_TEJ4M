import cv2
import face_recognition
from imutils import paths
from pathlib import Path
import pickle
import uuid

# people_ids = {}
# dataset_path = Path("dataset")
# for person in dataset_path.iterdir():
#     name = person.name
#     id = uuid.uuid4()
#     people_ids[name] = id
#     if person.is_dir():
#         images = list(paths.list_images(person))
#         print(f"Name: {person.name}")
# print(people_ids)
#

# TODO: consider using separate pickle file for id->names instead of encoding associated with an id and name
def train_model():
    print("[INFO] start processing faces...")
    known_encodings = []
    known_names = []
    known_ids = []

    people_ids = {}
    dataset_path = Path("dataset")
    for person in dataset_path.iterdir():
        if person.is_dir():
            name = person.name
            id = uuid.uuid4()
            people_ids[id] = name
            person_images = list(paths.list_images(person))

            for (i, image_path) in enumerate(person_images):
                print(f"[INFO] processing image {i + 1} for {name}")
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError("Failed to load image")

                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb, model="hog")
                encodings = face_recognition.face_encodings(rgb, boxes)

                for encoding in encodings:
                    known_encodings.append(encoding)
                    known_names.append(name)
                    known_ids.append(id)

    print("[INFO] serializing encodings...")
    data = {"encodings": known_encodings, "names": known_names, "ids": known_ids}
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))

    print("[INFO] Training complete. Encodings saved to 'encodings.pickle'")

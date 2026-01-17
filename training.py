import cv2
import face_recognition
from imutils import paths
from pathlib import Path
import pickle
import uuid

# TODO: consider using separate pickle file for id->names instead of dict of people with associated encodings and an id and name
def train_model():
    print("[INFO] start processing faces...")
    encodings_data = {"people": []}
    # people_data = {}

    dataset_path = Path("dataset")
    for person in dataset_path.iterdir():
        if person.is_dir():
            name = person.name
            id = uuid.uuid4()
            person_dict = { "id": id, "name": name, "encodings": [] }

            person_images = list(paths.list_images(person))
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

            encodings_data["people"].append(person_dict)

    print("[INFO] serializing encodings...")
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(encodings_data))

    print("[INFO] Training complete. Encodings saved to 'encodings.pickle'")

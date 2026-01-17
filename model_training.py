import os
from imutils import paths
from pathlib import Path
import face_recognition
import pickle
import cv2

# TODO: consider finding a way to only train new pictures instead of everything
def train_model():
    print("[INFO] start processing faces...")
    imagePaths = list(paths.list_images("dataset"))
    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):
        pathlib_path = Path(imagePath)
        print(f"[INFO] processing image {i + 1}/{len(imagePaths)} (for {pathlib_path.parent.name})")
        name = imagePath.split(os.path.sep)[-2]
        
        image = cv2.imread(imagePath)
        if image is None:
            raise ValueError("Failed to load image")

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)

    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))

    print("[INFO] Training complete. Encodings saved to 'encodings.pickle'")

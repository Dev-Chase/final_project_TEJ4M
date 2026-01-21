from google.cloud import firestore
from utils import *
import os

CLOUD_PROJECT_KEY_FILE = "cloud_project_key.json"

class Cloud():
    def __init__(self):
        if os.path.exists(CLOUD_PROJECT_KEY_FILE):
            print("Connecting to Google Cloud")
            self.db = firestore.Client.from_service_account_json(CLOUD_PROJECT_KEY_FILE)
        else:
            print("Unable to connect to Google Cloud, since no credential file is present")
            self.db = None

    def log_attendance(self, attendance_info):
        if self.db:
            print("Saving attendance sheet to Google Cloud")
            attendance_info["upload_time"] = firestore.SERVER_TIMESTAMP
            self.db.collection("attendance_sheets").add(attendance_info)
        else:
            print("I can't save an attendance sheet since I'm not connected to Google Cloud")

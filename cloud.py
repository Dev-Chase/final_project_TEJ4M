from utils import *
from google.cloud import firestore

CLOUD_PROJECT_KEY_FILE = "cloud_project_key.json"

class Cloud():
    def __init__(self):
        print("Connecting to Google Cloud")
        self.db = firestore.Client.from_service_account_json(CLOUD_PROJECT_KEY_FILE)

    def log_attendance(self, attendance_info):
        print("Saving attendance sheet to Google Cloud")
        self.db.collection("attendance_sheets").add(attendance_info)

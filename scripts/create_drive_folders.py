#!/usr/bin/env python3
"""
Google Drive Folder Creator
Creates organized folder structure for all 6 courses in Google Drive.

Prerequisites:
  1. pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
  2. Create OAuth credentials at console.cloud.google.com → APIs → Drive API
  3. Download credentials.json and put it in this scripts/ folder
  4. Run this script — it will open browser for auth on first run

Folder structure created:
  CSE Exam Season 2026/
  ├── CSE713_AI/
  │   ├── Lecture Materials/
  │   ├── Past Papers/
  │   └── My Notes/
  ├── CSE717_InfoSec/ (same structure)
  ... etc
"""

import os
import pickle
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPTS_DIR / "credentials.json"
TOKEN_FILE = SCRIPTS_DIR / "token.pickle"

COURSES = [
    ("CSE713_AI", "Artificial Intelligence"),
    ("CSE717_InfoSec", "Information Security"),
    ("CSE711_Compiler", "Compiler"),
    ("CSE719_Distributed", "Distributed & Cloud Computing"),
    ("CSE715_Graphics", "Computer Graphics"),
    ("CSE700_Thesis", "Thesis"),
]

SUBFOLDERS = ["Lecture Materials", "Past Papers", "My Notes"]

def get_drive_service():
    try:
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        print("Installing Google API libraries...")
        os.system("pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib -q")
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request

    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print("SETUP NEEDED:")
                print("")
                print("1. Go to: console.cloud.google.com")
                print("2. Create a project → Enable Google Drive API")
                print("3. Credentials → Create OAuth 2.0 Client ID (Desktop app)")
                print("4. Download credentials.json")
                print(f"5. Put it at: {CREDENTIALS_FILE}")
                print("6. Run this script again")
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("drive", "v3", credentials=creds)

def create_folder(service, name: str, parent_id: str = None) -> str:
    """Create a Google Drive folder, return its ID."""
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    # Check if already exists
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    existing = results.get("files", [])

    if existing:
        return existing[0]["id"]

    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Google Drive Folder Creator")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    service = get_drive_service()
    if not service:
        return

    print("Creating root folder...")
    root_id = create_folder(service, "CSE Exam Season 2026")
    print(f"✓ Root: CSE Exam Season 2026 (ID: {root_id})")
    print("")

    for course_code, course_name in COURSES:
        folder_name = f"{course_code} — {course_name}"
        course_id = create_folder(service, folder_name, root_id)
        print(f"✓ {folder_name}")

        for subfolder in SUBFOLDERS:
            sub_id = create_folder(service, subfolder, course_id)
            print(f"     └── {subfolder}")

    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Done. Find your folders at: drive.google.com")
    print("Root folder: 'CSE Exam Season 2026'")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    main()

# youtube_upload.py
import os
import json
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

logger = logging.getLogger(__name__)

# These should be set as GitHub Secrets and available at runtime via env vars in Actions
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES
    )
    # Force refresh to obtain access token
    request = google.auth.transport.requests.Request()
    creds.refresh(request)
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    return youtube

def upload_video(file_path: str, title: str, description: str, tags: list = None, privacy="public"):
    tags = tags or ["AI","shorts","SmartAIHacks"]
    youtube = get_authenticated_service()
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logger.info("Uploaded %d%%", int(status.progress() * 100))
    logger.info("Upload Complete: %s", response.get("id"))
    return response

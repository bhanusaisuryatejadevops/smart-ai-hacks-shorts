import os
import logging
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

def is_youtube_ready():
    return all([os.getenv("YOUTUBE_CLIENT_ID"), os.getenv("YOUTUBE_CLIENT_SECRET"), os.getenv("YOUTUBE_REFRESH_TOKEN")])

def get_youtube_client():
    if not is_youtube_ready():
        raise RuntimeError("YouTube credentials not configured (YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN).")
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    youtube = build("youtube", "v3", credentials=creds)
    return youtube

def upload_video(file_path: str, title: str, description: str = "", privacy: str = "private", retries: int = 3):
    youtube = get_youtube_client()
    body = {
        "snippet": {"title": title[:100], "description": description, "categoryId": "28"},
        "status": {"privacyStatus": privacy}
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                logger.info("Upload progress: %s%%", int(status.progress() * 100))
        except HttpError as e:
            if e.resp.status in (500,502,503,504):
                logger.warning("Server error %s - retrying...", e.resp.status)
                time.sleep(5)
                continue
            if e.resp.status == 403:
                logger.error("403 Forbidden - YouTube API may not be enabled for your project or credentials lack scopes.")
                raise
            raise
    logger.info("Upload complete: %s", response.get("id"))
    return response

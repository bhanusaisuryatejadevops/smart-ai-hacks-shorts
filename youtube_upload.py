# youtube_upload.py
import os
import logging
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_youtube_client():
    """Initialize YouTube API client using credentials from environment variables."""
    try:
        creds = Credentials(
            token=None,
            refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
            client_id=os.getenv("YOUTUBE_CLIENT_ID"),
            client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
            token_uri="https://oauth2.googleapis.com/token"
        )
        youtube = build("youtube", "v3", credentials=creds)
        return youtube
    except Exception as e:
        logger.exception("Failed to initialize YouTube client: %s", e)
        raise

def upload_video(file_path: str, title: str, description: str, privacy: str = "private", retries: int = 3):
    """Upload video to YouTube with retries and error handling."""
    youtube = get_youtube_client()
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "28",  # 28 = Science & Technology
        },
        "status": {
            "privacyStatus": privacy
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        response = None
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    logger.info("Upload progress: %d%%", int(status.progress() * 100))
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    # retry on server errors
                    logger.warning("Server error %d, retrying...", e.resp.status)
                    time.sleep(5)
                else:
                    raise
        logger.info("Upload successful! Video ID: %s", response.get("id"))
        return response
    except HttpError as e:
        if e.resp.status == 403:
            logger.error(
                "403 Forbidden - YouTube Data API v3 might be disabled for your project. "
                "Enable it here: https://console.developers.google.com/apis/api/youtube.googleapis.com/overview"
            )
        else:
            logger.exception("Failed to upload video: %s", e)
        raise
    except Exception as e:
        logger.exception("Unexpected error during upload: %s", e)
        raise

if __name__ == "__main__":
    # quick test
    file_path = "assets/output/short_test.mp4"
    if os.path.exists(file_path):
        upload_video(file_path, title="Test Upload", description="Testing YouTube Upload Script")
    else:
        logger.warning("Test video does not exist: %s", file_path)

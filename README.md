# YouTube Auto AI Shorts (private repo)

Automated pipeline that:
- Fetches trending AI topics (news / reddit / twitter)
- Generates a 30–45s viral script
- Generates female voice-over (nova-2)
- Auto-generates AI-futuristic background images and animates them
- Creates a 9:16 short video (1080x1920)
- Uploads to YouTube automatically

**Runs 3x/day via GitHub Actions**.

---

## Secrets (set in GitHub repo Settings → Secrets → Actions)
- `OPENAI_API_KEY` — OpenAI API key
- `YOUTUBE_CLIENT_ID` — OAuth2 client id for YouTube
- `YOUTUBE_CLIENT_SECRET` — OAuth2 client secret
- `YOUTUBE_REFRESH_TOKEN` — OAuth2 refresh token for the channel (one-time)
- `GOOGLE_API_KEY` — (optional) if you use some Google APIs for thumbnails
- `CHANNEL_TITLE` — your channel title (used in metadata)

**How to get YOUTUBE_REFRESH_TOKEN (one-time manual):**
1. Use Google OAuth playground or local script to obtain refresh token with `https://www.googleapis.com/auth/youtube.upload` scope.
2. Store the refresh token into GitHub Secrets.

---

## How to use
1. Create a private GitHub repository and add this folder structure and files.
2. Add GitHub Secrets listed above.
3. Push to `main`.
4. GitHub Actions will run the workflow and create/upload 3 videos per day.

---

## Notes
- All video/audio files are written to `assets/` and `assets/output/`.
- The code is written to be free-tier friendly (uses OpenAI free-tier where available).
- You must supply the required API secrets. No paid services are required beyond any optional APIs you decide to use.

If anything fails in Actions, the logs will show step-by-step outputs. Share logs if you want me to debug.

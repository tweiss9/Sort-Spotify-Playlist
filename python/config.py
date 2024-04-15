import os
from dotenv import load_dotenv

load_dotenv()
scope = "user-library-read user-read-private playlist-read-private playlist-modify-private playlist-modify-public"
client_id = os.environ.get("SPOTIFY_WEBSITE_SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_WEBSITE_SPOTIFY_CLIENT_SECRET")
redirect_uri = os.environ.get("SPOTIFY_WEBSITE_SPOTIFY_REDIRECT_URI")
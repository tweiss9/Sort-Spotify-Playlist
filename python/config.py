import os

scope = "user-library-read playlist-modify-private playlist-modify-public"
client_id = os.environ.get("PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read playlist-modify-private playlist-modify-public"
client_id = os.environ.get("PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

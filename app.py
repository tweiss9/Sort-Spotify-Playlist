import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, redirect, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 
app.static_folder = 'static'

# Spotify API credentials
scope = "user-library-read playlist-modify-private playlist-modify-public"
client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Login route
@app.route("/login")
def login():
    scope = "playlist-read-private"
    auth_url = SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    ).get_authorize_url()
    return redirect(auth_url)

# Callback route
@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    ).get_access_token(code)
    session["token_info"] = token_info
    return redirect("/playlists")

# Playlists route
@app.route("/playlists")
def playlists():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/login")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))
    playlists = sp.current_user_playlists()

    return render_template("playlists.html", playlists=playlists)

if __name__ == "__main__":
    app.run(debug=True)

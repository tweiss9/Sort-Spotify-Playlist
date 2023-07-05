import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, redirect, request, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("PROJECT_SPOTIFY_FLASK_SECRET_KEY")
app.static_folder = 'static'

# Spotify API credentials
scope = "user-library-read playlist-modify-private playlist-modify-public"
client_id = os.environ.get("PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_SECRET")
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


@app.route("/playlists")
def playlists():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/login")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

    playlists = sp.current_user_playlists()['items']

    user_playlists = [
        playlist for playlist in playlists if playlist['owner']['id'] == sp.me()['id']]

    return render_template("playlists.html", playlists=user_playlists)


@app.route("/playlist/<playlist_id>")
def playlist_detail(playlist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))
    playlist = sp.playlist(playlist_id)
    songs = playlist['tracks']['items']

    formatted_songs = []
    for song in songs:
        song_info = {
            'name': song['track']['name'],
            'album': song['track']['album']['name'],
            'album_cover': song['track']['album']['images'][0]['url']
        }
        formatted_songs.append(song_info)

    return render_template("playlist_detail.html", playlist_name=playlist['name'], songs=formatted_songs, playlist_cover=playlist['images'][0]['url'])


if __name__ == "__main__":
    app.run(debug=True)

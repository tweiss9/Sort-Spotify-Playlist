from flask import Flask, render_template, redirect, request, session
from spotipy.oauth2 import SpotifyOAuth
from python.config import sp, scope, client_id, client_secret, redirect_uri
from spotipy.exceptions import SpotifyException
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("PROJECT_SPOTIFY_FLASK_SECRET_KEY")

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
    sp_oauth = SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )
    token_info = sp_oauth.get_cached_token()
    session["token_info"] = token_info
    return redirect("/playlists")

# Playlists route
@app.route("/playlists")
def playlists():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/login")
    
    playlists = sp.current_user_playlists()['items']

    user_playlists = [
        playlist for playlist in playlists if playlist['owner']['id'] == sp.me()['id']]

    for playlist in user_playlists:
        playlist['track_count'] = sp.playlist_tracks(
            playlist['id'], fields='total')['total']

    return render_template("playlists.html", playlists=user_playlists)

# Playlist detail route
@app.route("/playlist/<playlist_id>")
def playlist_detail(playlist_id):
    session['playlist_id'] = playlist_id

    try:
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

    except SpotifyException as e:
        if e.http_status == 404:
            return render_template("playlist_not_found.html")

        # Handle other SpotifyException here

    # Handle other exceptions or errors here

    return render_template("error.html")  # Fallback error page
@app.route("/playlist/<playlist_id>")
def get_playlist_id():
    playlist_id = session.get('playlist_id')
    return playlist_id

@app.route("/execute_python", methods=["POST"])
def execute_python():
    python_file = request.json["python_file"]
    try:
        print(f"Executing {python_file}...")
        file_path = f"python/{python_file}"
        with open(file_path) as f:
            code = compile(f.read(), file_path, 'exec')
            exec(code, globals())
        return "Python file executed successfully."
    except Exception as e:
        return f"An error occurred: {e}"
if __name__ == "__main__":
    app.run(debug=True)

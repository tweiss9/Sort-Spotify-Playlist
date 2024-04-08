from datetime import datetime
from flask_compress import Compress
from flask import Flask, Response, make_response, render_template, redirect, request
from spotipy.exceptions import SpotifyException
from python.config import sp, sp_oauth
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("PROJECT_SPOTIFY_FLASK_SECRET_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    return redirect("/playlists")

@app.route("/playlists")
def playlists():
    try:
        if sp_oauth.is_token_expired(sp_oauth.get_cached_token()):
            return redirect("/login")

        user_playlists = []
        fetched_playlists = []
        offset = 0
        limit = 50

        while True:
            response = sp.current_user_playlists(offset=offset, limit=limit)
            fetched_playlists.extend(response["items"])
            total_playlists = response["total"]
            offset += limit
            if offset >= total_playlists:
                break

        user_playlists = [
            playlist for playlist in fetched_playlists 
            if (
                playlist['owner']['id'] == sp.me()['id'] and
                not playlist["collaborative"] and
                playlist["tracks"]["total"] > 0
            )
        ]

        response = make_response(render_template(
            "playlists.html", playlists=user_playlists))
        return response
    except SpotifyException as e:
        if e.http_status == 404:
            return render_template("playlist_404.html")
        else:
            return render_template("spotify_error.html")
    except Exception as e:
        return server_error(e)

@app.route("/playlist/<playlist_id>")
def playlist_detail(playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
        songs = playlist["tracks"]["items"]
        formatted_songs = []

        for song in songs:
            try:
                release_date_str = song["track"]["album"]["release_date"]
                if release_date_str.startswith("0"):
                    release_date = None
                else:
                    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").strftime("%m/%d/%Y")
            except ValueError:
                try:
                    release_date_str = song["track"]["album"]["release_date"]
                    if release_date_str.startswith("0"):
                        release_date = None
                    else:
                        release_date = datetime.strptime(release_date_str, "%Y-%m").strftime("%m/%Y")
                except ValueError:
                    release_date_str = song["track"]["album"]["release_date"]
                    if release_date_str.startswith("0"):
                        release_date = None
                    else:
                        release_date = datetime.strptime(release_date_str, "%Y").strftime("%Y")
            song_info = {
                "name": song["track"]["name"],
                "artist": song["track"]["artists"][0]["name"],
                "release_date": release_date,
                "album_cover": song["track"]["album"]["images"][0]["url"] if song["track"]["album"]["images"] else None,
            }

            formatted_songs.append(song_info)

        response = make_response(render_template(
            "playlist_detail.html",
            playlist_name=playlist["name"],
            songs=formatted_songs,
            playlist_cover=playlist["images"][0]["url"] if playlist["images"] else None,
        ))
        return response
    except SpotifyException as e:
        if e.http_status == 404:
            return render_template("playlist_404.html")
        else:
            return render_template("spotify_error.html")
    except Exception as e:
        print("Error:", e)
        return server_error(Exception)

@app.route("/execute_python", methods=["POST"])
def execute_python():
    python_file = request.json["python_file"]
    playlist_id = request.json["playlist_id"]
    sorting_type = request.json["sorting_type"]
    is_reverse = request.json["is_reverse"]
    is_new = request.json["is_new"]

    try:
        file_path = f"python/{python_file}"
        with open(file_path) as f:
            code = compile(f.read(), file_path, 'exec')
            exec(code, globals(), {'playlist_id': playlist_id, 'sorting_type': sorting_type,
                'is_reverse': is_reverse, 'is_new': is_new})
            return Response(status=200)
    except FileNotFoundError as e:
        return page_not_found(e)
    except Exception as e:
        return server_error(e)

@app.errorhandler(404)
def page_not_found(error):
    error_message = str(error)
    return render_template('404.html', error_message=error_message), 404

@app.errorhandler(500)
def server_error(error):
    error_message = str(error)
    return render_template('500.html', error_message=error_message), 500

@app.route('/500')
def error_500():
    return render_template('500.html')

if __name__ == "__main__":
    app.run(debug=True)

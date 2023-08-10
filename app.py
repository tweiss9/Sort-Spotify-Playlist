from datetime import datetime
from flask_compress import Compress
from flask import Flask, Response, make_response, render_template, redirect, request, session
from spotipy.exceptions import SpotifyException
from python.config import sp, cache, sp_oauth
from python.caching import fetch_and_cache_playlists, generate_etag, generate_last_modified
# from waitress import serve
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("PROJECT_SPOTIFY_FLASK_SECRET_KEY")

cache.init_app(app)


@app.before_request
def initialize_cache():
    if session.get("token_info") and session["token_info"]["access_token"]:
        if not cache.get("playlists"):
            fetch_and_cache_playlists()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    token_info = sp_oauth.get_cached_token()
    session["token_info"] = token_info
    return redirect("/playlists")


@app.route("/playlists")
def playlists():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/login")

    user_id = cache.get("user_id") or ""

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

    user_playlists = [playlist for playlist in fetched_playlists if (playlist["owner"]["id"] == user_id) and (
        not playlist["collaborative"]) and (playlist["tracks"]["total"] > 0)]

    cached_playlists = cache.get("playlists") or []
    cached_user_playlists = cache.get("user_playlists") or []

    if fetched_playlists != cached_playlists or user_playlists != cached_user_playlists:
        cache.set("playlists", fetched_playlists)
        cache.set("user_playlists", user_playlists)

    etag = request.headers.get("If-None-Match")
    last_modified = request.headers.get("If-Modified-Since")

    current_etag = generate_etag(user_playlists)
    current_last_modified = generate_last_modified(user_playlists)

    if etag == current_etag and last_modified == current_last_modified:
        return Response(status=304)

    response = make_response(render_template(
        "playlists.html", playlists=user_playlists))
    response.set_etag(current_etag)
    response.headers["Last-Modified"] = current_last_modified
    return response


@app.route("/playlist/<playlist_id>")
def playlist_detail(playlist_id):
    session["playlist_id"] = playlist_id

    try:
        playlist = sp.playlist(playlist_id)
        songs = playlist["tracks"]["items"]
        formatted_songs = []

        for song in songs:
            release_date = datetime.strptime(song["track"]["album"]["release_date"], "%Y-%m-%d").strftime("%m/%d/%Y")

            song_info = {
                "name": song["track"]["name"],
                "artist": song["track"]["artists"][0]["name"],
                "release_date": release_date,
                "album_cover": song["track"]["album"]["images"][0]["url"],
            }
            formatted_songs.append(song_info)

        return render_template(
            "playlist_detail.html",
            playlist_name=playlist["name"],
            songs=formatted_songs,
            playlist_cover=playlist["images"][0]["url"],
        )

    except SpotifyException as e:
        if e.http_status == 404:
            return render_template("playlist_404.html")
        else:
            return render_template("spotify_error.html")
    except Exception:
        return server_error(Exception)


@app.route("/execute_python", methods=["POST"])
def execute_python():
    python_file = request.json["python_file"]
    sorting_type = request.json["sorting_type"]
    is_reverse = request.json["is_reverse"]
    is_new = request.json["is_new"]

    try:
        file_path = f"python/{python_file}"
        with open(file_path) as f:
            code = compile(f.read(), file_path, 'exec')
            exec(code, globals(), {'sorting_type': sorting_type,
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
    Compress(app)

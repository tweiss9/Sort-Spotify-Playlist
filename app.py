from datetime import datetime
from flask import Flask, Response, jsonify, make_response, render_template, redirect, request, session
import requests
from spotipy.exceptions import SpotifyException
from python.config import client_id, client_secret, redirect_uri, scope
from werkzeug.utils import secure_filename
import spotipy
import os
from waitress import serve

app = Flask(__name__, static_folder="public/static", template_folder="public/templates")
app.secret_key = os.environ.get("SPOTIFY_FLASK_SECRET_KEY")
SAFE_SCRIPT_DIRECTORY = os.path.join(os.getcwd(), "python")

def is_safe_path(basedir, path, follow_symlinks=True):
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    return os.path.abspath(path).startswith(basedir)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    try:
        session.clear()
        sp_oauth = spotipy.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    except Exception:
        return server_error()
    
@app.route("/logout")
def logout():
    token_info = session.get('token_info', None)
    if token_info:
        access_token = token_info['access_token']
        requests.post('https://accounts.spotify.com/api/revoke', data={'token': access_token})
        session.clear()
        try:
            os.remove(".cache")
        except OSError:
            pass
    response = jsonify({'status': 'success'})
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.set_cookie('session', '', expires=0)
    return response, 200

@app.route("/callback")
def callback():
    try:
        code = request.args.get('code')
        sp_oauth = spotipy.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            token_info = sp_oauth.get_access_token(code)
        elif sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
        spotify_user = spotipy.Spotify(auth=token_info['access_token'])
        user_id = spotify_user.me()['id']
        session['user_id'] = user_id
    except Exception:
        return server_error()
    return redirect("/playlists")

@app.route("/playlists")
def playlists():
    try:
        sp_oauth = spotipy.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
        token_info = session.get('token_info', None)
        if not token_info or sp_oauth.is_token_expired(token_info):
            return redirect("/login")
        spotify_user = spotipy.Spotify(auth=token_info['access_token'])

        current_user_id = spotify_user.me()['id']
        if session.get('user_id') != current_user_id:
            return redirect("/login")
        user_playlists = []
        fetched_playlists = []
        offset = 0
        limit = 50

        while True:
            response = spotify_user.current_user_playlists(offset=offset, limit=limit)
            fetched_playlists.extend(response["items"])
            total_playlists = response["total"]
            offset += limit
            if offset >= total_playlists:
                break
            
        user_playlists = [
            playlist for playlist in fetched_playlists 
            if (
                playlist['owner']['id'] == current_user_id and
                not playlist["collaborative"] and
                playlist["tracks"]["total"] > 0
            )
        ]
        response = make_response(render_template(
            "playlists.html", playlists=user_playlists))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except SpotifyException as e:
        if e.http_status == 404:
            return render_template("error/playlist_404.html")
        else:
            return render_template("error/spotify_error.html")
    except Exception:
        return server_error()

@app.route("/playlist/<playlist_id>")
def playlist_detail(playlist_id):
    try:
        sp_oauth = spotipy.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
        token_info = session.get('token_info', None)
        if not token_info or sp_oauth.is_token_expired(token_info):
            return redirect("/login")
        spotify_user = spotipy.Spotify(auth=token_info['access_token'])
        playlist = spotify_user.playlist(playlist_id)
        songs = playlist["tracks"]["items"]
        formatted_songs = []

        for song in songs:
            track = song["track"]
            album = track["album"]
            release_date_str = album["release_date"]
            
            if release_date_str.startswith("0"):
                release_date = None
            else:
                try:
                    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").strftime("%m/%d/%Y")
                except ValueError:
                    try:
                        release_date = datetime.strptime(release_date_str, "%Y-%m").strftime("%m/%Y")
                    except ValueError:
                        release_date = datetime.strptime(release_date_str, "%Y").strftime("%Y")

            artist = track["artists"][0]
            album_cover = album["images"][0]["url"] if album["images"] else None
            
            song_info = {
                "name": track["name"],
                "artist": artist["name"],
                "release_date": release_date,
                "album_cover": album_cover,
            }
            formatted_songs.append(song_info)

        response = make_response(render_template(
            "playlist_detail.html",
            playlist_name=playlist["name"],
            songs=formatted_songs,
            playlist_cover=playlist["images"][0]["url"] if playlist["images"] else None,
        ))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except SpotifyException as e:
        if e.http_status == 400:
            return render_template("error/playlist_404.html")
        else:
            return render_template("error/spotify_error.html")
    except Exception:
        return server_error()

@app.route("/execute_python", methods=["POST"])
def execute_python():
    try:
        data = request.json
        python_file = data["python_file"]
        playlist_id = data["playlist_id"]
        sorting_type = data["sorting_type"]
        is_reverse = data["is_reverse"]
        is_new = data["is_new"]
        safe_filename = secure_filename(python_file)
        file_path = os.path.join(SAFE_SCRIPT_DIRECTORY, safe_filename)
    
        if not is_safe_path(SAFE_SCRIPT_DIRECTORY, file_path):
            return jsonify({"error": "Invalid file path"}), 400
        
        with open(file_path) as f:
            code = compile(f.read(), file_path, 'exec')
            exec(code, globals(), {'playlist_id': playlist_id, 'sorting_type': sorting_type,
                'is_reverse': is_reverse, 'is_new': is_new})
            return Response(status=200)
    except FileNotFoundError:
        return page_not_found()
    except Exception:
        return server_error()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error/500.html'), 500

@app.route('/playlist/500')
def error_500():
    return render_template('error/500.html')

if __name__ == "__main__":
    serve(app, host='127.0.0.1', port=5000)

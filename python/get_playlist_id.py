from flask import session
def get_playlist_id():
    playlist_id = session.get("playlist_id")
    return playlist_id
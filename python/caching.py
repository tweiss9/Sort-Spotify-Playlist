from datetime import datetime
import hashlib
from python.config import sp, cache


def fetch_and_cache_playlists():
    user_id = sp.me()["id"]
    cache.set("user_id", user_id)

    fetched_playlists = sp.current_user_playlists(limit=50)["items"]
    cached_playlists = cache.get("playlists") or []

    new_playlists = [
        playlist for playlist in fetched_playlists if playlist not in cached_playlists]

    updated_playlists = [
        playlist for playlist in fetched_playlists if playlist in cached_playlists]

    deleted_playlists = [
        playlist for playlist in cached_playlists if playlist not in fetched_playlists]

    cache.set("playlists", fetched_playlists)

    updated_user_playlists = [
        playlist for playlist in cached_playlists if playlist not in deleted_playlists]
    updated_user_playlists.extend(new_playlists)
    updated_user_playlists.extend(updated_playlists)
    cache.set("user_playlists", updated_user_playlists)

    playlist_ids = [playlist["id"] for playlist in fetched_playlists]
    track_counts = batch_get_track_counts(playlist_ids)
    cache.set("track_counts", track_counts)


def batch_get_track_counts(playlist_ids):
    track_counts = {}

    for playlist_id in playlist_ids:
        response = sp.playlist_tracks(playlist_id)
        count = response["total"]
        track_counts[playlist_id] = count

    return track_counts


def generate_last_modified(playlists):
    if isinstance(playlists, dict):
        last_modified = playlists.get("last_modified")
    else:
        last_modified = None

    if last_modified:
        return last_modified

    # Set a default last modified timestamp for cases when playlists is not available
    default_last_modified = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    return default_last_modified


def generate_etag(playlists):
    playlists_str = str(playlists)
    etag = hashlib.md5(playlists_str.encode()).hexdigest()
    return etag

from app import get_playlist_id
from python.config import sp


def release_date():
    print("Hello World!")
    playlistId = get_playlist_id()
    print(playlistId)

    # Retrieve all tracks from the specified playlist
    playlist_tracks = []
    results = sp.playlist_tracks(playlist_id=playlistId, limit=100)
    playlist_tracks.extend(results["items"])

    while results["next"]:
        results = sp.next(results)
        playlist_tracks.extend(results["items"])

    # Sort tracks by release date
    sorted_tracks = sorted(playlist_tracks, key=lambda x: (
        x["track"]["album"]["release_date"]), reverse=True)

    # Create a new playlist for the sorted tracks
    new_playlist_name = "Sorted Playlist"
    new_playlist_description = "Sorted playlist of a specific playlist"
    new_playlist = sp.user_playlist_create(user=sp.me(
    )["id"], name=new_playlist_name, public=False, description=new_playlist_description)
    new_playlist_id = new_playlist["id"]

    # Add the sorted tracks to the new playlist in batches
    batch_size = 100
    for i in range(0, len(sorted_tracks), batch_size):
        batch_uris = [track["track"]["uri"]
                      for track in sorted_tracks[i:i+batch_size]]
        sp.playlist_add_items(playlist_id=new_playlist_id, items=batch_uris)
    print("Done!")

release_date()

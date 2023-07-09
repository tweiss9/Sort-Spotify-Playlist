from requests import request
from app import get_playlist_id
from python.config import sp


def sorting_algorithm():
    print("Hello World!")
    playlist_id = get_playlist_id()
    print(playlist_id)
    sorting_type = request.json["sorting_type"]
    print("sorting_type: " + sorting_type)
    is_reverse = request.json["is_reverse"]
    print("is_reverse: " + str(is_reverse))
    is_new = request.json["is_new"]
    print("is_new: " + str(is_new))

    # Retrieve the playlist name
    playlist = sp.playlist(playlist_id=playlist_id)
    playlist_name = playlist["name"]
    
    # Retrieve all tracks from the specified playlist
    playlist_tracks = []
    results = sp.playlist_tracks(playlist_id=playlist_id, limit=100)
    playlist_tracks.extend(results["items"])

    while results["next"]:
        results = sp.next(results)
        playlist_tracks.extend(results["items"])

    # Sort tracks by release date
    if sorting_type == "release_date":
        sorted_tracks = sorted(playlist_tracks, key=lambda x: (
            x["track"]["album"]["release_date"]), reverse=is_reverse)
    elif sorting_type == "track_name":
        sorted_tracks = sorted(playlist_tracks, key=lambda x: (
            x["track"]["name"].lower()), reverse=is_reverse)
    elif sorting_type == "artist_name":
        sorted_tracks = sorted(playlist_tracks, key=lambda x: (
            x["track"]["artists"][0]["name"].lower()), reverse=is_reverse)
    else:
        print("Invalid sorting type")
        return

    # Create a new playlist for the sorted tracks
    if is_new == True:
        new_playlist_name = f"Sorted {playlist_name} by {sorting_type}"
        new_playlist_description = f"Sorted playlist of {playlist_name} by {sorting_type}"
        new_playlist = sp.user_playlist_create(user=sp.me(
        )["id"], name=new_playlist_name, public=False, description=new_playlist_description)
        new_playlist_id = new_playlist["id"]

        # Add the sorted tracks to the new playlist in batches
        batch_size = 100
        for i in range(0, len(sorted_tracks), batch_size):
            batch_uris = [track["track"]["uri"]
                        for track in sorted_tracks[i:i+batch_size]]
            sp.playlist_add_items(playlist_id=new_playlist_id, items=batch_uris)

        print("Done Creating!")
    else:
        # Create a temporary playlist for sorted tracks
        temp_playlist_name = "Temp Playlist"
        temp_playlist_description = "Temporary playlist for sorting"
        temp_playlist = sp.user_playlist_create(user=sp.me()["id"], name=temp_playlist_name, public=False, description=temp_playlist_description)
        temp_playlist_id = temp_playlist["id"]
        print("Temporary playlist created")

        # Add the sorted tracks to the temporary playlist in batches
        batch_size = 100
        for i in range(0, len(sorted_tracks), batch_size):
            batch_uris = [track["track"]["uri"] for track in sorted_tracks[i:i+batch_size]]
            sp.playlist_add_items(playlist_id=temp_playlist_id, items=batch_uris)

        # Retrieve all tracks from the temporary playlist
        temp_playlist_tracks = []
        results = sp.playlist_tracks(temp_playlist_id, fields="items(track(uri)),next")
        temp_playlist_tracks.extend(results["items"])

        while results["next"]:
            results = sp.next(results)
            temp_playlist_tracks.extend(results["items"])

        # Remove all tracks from the existing playlist
        for i in range(0, len(playlist_tracks), batch_size):
            batch_uris = [track["track"]["uri"] for track in playlist_tracks[i:i+batch_size]]
            sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_id, items=batch_uris)

        # Add the tracks from the temporary playlist to the existing playlist in batches
        for i in range(0, len(temp_playlist_tracks), batch_size):
            batch_uris = [track["track"]["uri"] for track in temp_playlist_tracks[i:i+batch_size]]
            sp.playlist_add_items(playlist_id=playlist_id, items=batch_uris)

        # Unfollow and delete the temporary playlist
        sp.user_playlist_unfollow(user=sp.me()["id"], playlist_id=temp_playlist_id)
        print("Done Updating!")

sorting_algorithm()

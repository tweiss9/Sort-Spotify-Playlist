function redirectToPlaylistDetail(playlistId) {
    var url =
      "{{ url_for('playlist_detail', playlist_id='__placeholder__') }}";
    url = url.replace("__placeholder__", playlistId);
    window.location.href = url;
  }
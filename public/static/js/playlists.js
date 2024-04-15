function redirectToPlaylistDetail(playlistId) {
  window.location.href = "/playlist/" + playlistId;
}

function logOut() {
  $.ajax({
    url: '/logout',
    type: 'GET',
    success: function(response) {
      if (response.status === 'success') {
        window.location.href = "/";
      }
    }
  });
}
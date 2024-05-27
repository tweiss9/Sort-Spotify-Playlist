function redirectToPlaylistDetail(playlistId) {
  window.location.href = "/playlist/" + playlistId;
}

function logOut() {
  $.ajax({
    url: '/logout',
    type: 'GET',
    success: function(response) {
      if (response.status === 'success') {
        document.cookie = "session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        window.location.href = "/";
      }
    }
  });
}
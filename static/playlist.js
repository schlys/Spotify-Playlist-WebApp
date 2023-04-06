//-------------------------------------------------------------------------------------------------------------------------------------------------------

// calls the function to add playlist to spotify
function add() {
    fetch('/add_playlist', {
        method: 'POST'
    }).then(response => {
        if (response.ok) document.getElementById('add').innerHTML = '<p class="display-4 added">Playlist Added to Spotify</p>';
    })
}
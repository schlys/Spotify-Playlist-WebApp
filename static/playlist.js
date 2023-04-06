//------------------------------------------------------------------------------------------------------------------------------------------------------

// generates the playlist on the results screen
function onload() {
    $.getJSON("/get_playlist",
        function(data) {
            // var display = data.display
            // var type = display.type
            // var top = document.getElementById('descrip')

            // if (type === 'text') {
            //     top.innerHTML = `Playlist based on ${display.text}`
            // } else if (type === 'track') {
            //     top.innerHTML = `
            //         <span style="float: left">Playlist based on</span>
            //         <img id="cover" class="track_pic" src="${display.image}" alt="cover" hspace="10px" style="float: left;width:50px;height:50px;">
            //         <p>
            //             <strong>${display.name}</strong><br>
            //             <span>${display.artists}</span>
            //         </p>
            //     `
            // } else {
            //     top.innerHTML = `
            //         <span style="float: left">Playlist based on</span>
            //         <img id="cover" class="track_pic" src="${display.image}" alt="cover" hspace="10px" style="float: left;width:50px;height:50px;">
            //         <p><strong>${display.name}</strong></p>
            //     `
            // }

            for (let i=0; i<data.playlist.tracks.length; i++) {
                var track = data.playlist.tracks[i].track

                const div = document.createElement('div')
                div.className = 'list'
                div.innerHTML = `
                    <img class="track_pic" src="${track.image}" alt="cover" hspace="10px" style="float: left;width:50px;height:50px;">
                    <p>
                        <a href="${track.link}" target="_blank" class="display-4 track_link"><strong>${track.name}</strong><br></a>
                        <span class="display-4" style="font-size:80%">${track.artists}</span>
                    </p>
                `
                document.getElementById('playlist').appendChild(div)
            }

        })
}
window.addEventListener("load", onload, false)

//-------------------------------------------------------------------------------------------------------------------------------------------------------

// calls the function to add playlist to spotify
function add() {
    fetch('/add_playlist', {
        method: 'POST'
    }).then(response => {
        if (response.ok) document.getElementById('add').innerHTML = '<p class="display-4 added">Playlist Added to Spotify</p>';
    })
}
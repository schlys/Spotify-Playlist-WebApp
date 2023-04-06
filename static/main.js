//-------------------------------------------------------------------------------------------------------------

//update currently playing track
function update_track() {
    fetch('/update', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then((response) => {
        return response.json();
    }).then((data) => {
        track = data.track_data;
        var button = document.getElementById("pause_play");
        if (data.none == "0" && track.playing == true) {
            document.getElementById("name").innerHTML = track.name
            document.getElementById("cover").style.display = "inline"
            document.getElementById("cover").src = track.image
            document.getElementById("artists").innerHTML = track.artists + " 🎶 " + track.album
            document.getElementById("link").href = track.link
            button.name = "pause";
            button.src = `${window.pause}`;
        } else {
            button.name = "play";
            button.src = `${window.play}`;
        }
    });
}
setInterval('update_track()', 1000)

//----------------------------------------------------------------------------------------------------------------

//controls the playlist options
function playlist() {
    document.getElementById('spinner').style.visibility = 'visible';
    document.getElementById('error').innerHTML = '';
    var option = $('input[name=choices]:checked').attr('id');
    var size = document.getElementById('size');
    var written = document.getElementById('writtenoption');
    var text = '';

    if (written.style.visibility == 'visible') {
        text = written.value;
    }

    if (parseInt(size.value) >= 20 && parseInt(size.value) <= 200) {
        fetch('/make_playlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                option: option,
                size: size.value,
                text: text
            })
        }).then((response) => {
            if (response.ok) window.location.href = response.url;
            else {
                document.getElementById('error').innerHTML = 'Error creating playlist';
                document.getElementById('spinner').style.visibility = 'hidden';
                fetch('/playlists', {
                    method: 'POST'
                })
            }
        })
    } else {
        document.getElementById('spinner').style.visibility = 'hidden';
        document.getElementById('error').innerHTML = 'Please enter a valid playlist size';
    }

}

//-------------------------------------------------------------------------------------------------------------

//controls the player
function player (id, option) {
    if (id == "pause_play") {
        var button = document.getElementById("pause_play");
            if (button.name == "pause") {
                button.name = "play";
                button.src = `${window.play}`;
                option = "2";
            } else {
                button.name = "pause";
                button.src = `${window.pause}`;
                option = "3";
            }
    }

    fetch('/player', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            option: option,
        })
    })
}


// shows input box to type option
function write_option (option, show) {
    document.getElementById('error').innerHTML = '';
    var el = document.getElementById("writtenoption");
    if (show) {
        el.style.visibility = 'visible';
        el.placeholder = 'Enter ' + option;
    } else {
        el.style.visibility = 'hidden';
    }
}


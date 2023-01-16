//-------------------------------------------------------------------------------------------------------------
//update currently playing track

function update_track() {
    $.getJSON("/update",
        function(data) {
            //$("name").text(data.name)
            var button = document.getElementById("pause_play");
            if (data.none == "0" && data.playing == true) {
                document.getElementById("name").innerHTML = data.name
                document.getElementById("cover").style.display = "inline"
                document.getElementById("cover").src = data.image
                document.getElementById("artists").innerHTML = data.artists + " 🎶 " + data.album
                document.getElementById("link").href = data.link
                button.name = "pause";
                button.src = "https://cdn3.iconfinder.com/data/icons/line/36/pause-256.png";
            } else {
                button.name = "play";
                button.src = "https://cdn3.iconfinder.com/data/icons/line/36/play-256.png";
            }
        }
    );
}
setInterval('update_track()', 1000)

//----------------------------------------------------------------------------------------------------------------
//controls the playlist options

function playlist() {
    var option = $('input[name=choices]:checked').attr('id');
    var size = document.getElementById('size');
    var written = document.getElementById('writtenoption');
    var text = '';

    if (written.style.visibility == 'visible') {
        text = written.value;
    }

    if (parseInt(size) >= 20 || parseInt(size) <= 200) {
        $.ajax({
            type: "post",
            url: "/make_playlist",
            data: {
                option: option,
                size: size.value,
                text: text
            },
            success: function(response) {
                window.location.href = response.redirect;
            },
            error: function() {
                $.ajax({
                    type: 'post',
                    url: '/playlists',
                    data: {}
                })
            }
        })
    } else {
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
                button.src = "https://cdn3.iconfinder.com/data/icons/line/36/play-256.png";
                option = "2";
            } else {
                button.name = "pause";
                button.src = "https://cdn3.iconfinder.com/data/icons/line/36/pause-256.png";
                option = "3";
            }
    }
    $.ajax({
        type:"post",
        url: "/player",
        data: {
            option: option
        }
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


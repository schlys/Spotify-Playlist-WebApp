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

$(document).ready(function() {
    const wrapper = document.getElementById("options")
    wrapper.addEventListener('keydown', (event) => {
        const isCorrect = event.target.nodeName === 'INPUT'
        if (!isCorrect || event.code != "Enter") {
            return
        }
        document.getElementById('status').innerHTML = '<strong style="color:green">CREATING PLAYLIST...</strong>'
        var option = ""
        var id = event.target.id

        if (id === "song") {
            option = 'track'
        } else if (id === "artist") {
            option = 'artist'
        } else {
            option = 'genre'
        }
        $.ajax({
            type:"post",
            url: "/make_playlist",
            data: {
                option: option,
                text: document.getElementById(id).value,
                size: document.getElementById('size').value
            },
            success: function(response) {
                window.location.href = response.redirect
            },
            error: function() {
                document.getElementById('status').innerHTML = '<strong style="color:red">ERROR CREATING PLAYLIST</strong>'
                $.ajax({
                    type: 'post',
                    url: '/playlists',
                    data: {}
                })
            }
        })
    })
})

function playlist(option) {
    document.getElementById('status').innerHTML = '<strong style="color:green">CREATING PLAYLIST...</strong>'
    $.ajax({
        type: "post",
        url: "/make_playlist",
        data: {
            option: option,
            size: document.getElementById('size').value
        },
        success: function(response) {
            window.location.href = response.redirect
        },
        error: function() {
            document.getElementById('status').innerHTML = '<strong style="color:red">ERROR CREATING PLAYLIST</strong>'
            $.ajax({
                type: 'post',
                url: '/playlists',
                data: {}
            })
        }
    })
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



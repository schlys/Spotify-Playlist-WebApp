from flask import Flask, render_template, request, redirect, jsonify, url_for
import controller, flask

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
           response = controller.getUser()
           return redirect(response)
    else:
        return render_template('home.html')



@app.route('/callback/', methods=['POST', 'GET'])
def options():
    if 'error' in request.args:
        return redirect(flask.url_for('home'))

    controller.getUserToken(request.args['code'])
    return redirect(flask.url_for('playlists'))


@app.route('/update/', methods=['POST', 'GET'])
def update():
    controller.refreshToken()

    track = controller.getCurrentTrack()
    if track:
        return jsonify(none='0',
            link=track['link'],
            name=track['name'],
            artists=track['artists'],
            image=track['image'],
            album=track['album'],
            playing=track['playing']
            )
    return jsonify(none='1')



@app.route('/player/', methods=['POST', 'GET'])
def player():
    controller.refreshToken()
    print(request.form.get('option') + '-----------------------')
    controller.playback(int(request.form.get('option')))
    return jsonify(test='0')



@app.route('/playlists/', methods=['POST', 'GET'])
def playlists():
    controller.refreshToken()
    controller.clearList()
    if request.method == 'GET':
        return render_template('options.html')
    elif request.method == 'POST':
        return jsonify(cleared='1')




@app.route('/make_playlist/', methods=['POST', 'GET'])
def make_playlist():
    controller.refreshToken()

    size = int(request.form.get('size'))
    option = str(request.form.get('option'))
    text = request.form.get('text')

    print(f'playlist size: {size}')
    print(f'playlist option: {option}')
    print(f'text: {text}')

    if size >= 20 and size <= 200:
        controller.makePlaylist(size, option, text)
        return jsonify({'redirect': url_for('results')})
    return None
 


@app.route('/results/', methods=['POST', 'GET'])
def results():
    return render_template('results.html')



@app.route('/get_playlist/', methods=['POST', 'GET'])
def get_playlist():
    controller.refreshToken()
    js, name = controller.getList()
    return jsonify({'playlist':js, 'display':name})



@app.route('/add_playlist/', methods=['POST', 'GET'])
def add_playlist():
    controller.refreshToken()
    controller.addList()
    return jsonify(added='')


if __name__ == '__main__':
      app.run()

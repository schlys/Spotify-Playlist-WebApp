from flask import Flask, render_template, request, redirect, jsonify, url_for
import controller, flask, requests, json

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
    controller.getUserToken(request.args['code'])
    return redirect(flask.url_for('playlists'))


@app.route('/update/', methods=['POST', 'GET'])
def update():
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
    print(request.form.get('option') + '-----------------------')
    controller.playback(int(request.form.get('option')))
    return jsonify(test='0')



@app.route('/playlists/', methods=['POST', 'GET'])
def playlists():
    controller.clearList()
    if request.method == 'GET':
        return render_template('options.html')
    elif request.method == 'POST':
        return jsonify(cleared='1')




@app.route('/make_playlist/', methods=['POST', 'GET'])
def make_playlist():
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
    js, name = controller.getList()
    return jsonify({'playlist':js, 'display':name})



@app.route('/add_playlist/', methods=['POST', 'GET'])
def add_playlist():
    controller.addList()
    return jsonify(yeet='yeet')


if __name__ == '__main__':
      app.run()

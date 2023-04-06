from flask import Flask, render_template, request, redirect, jsonify, url_for, session
from functools import wraps
import playlist_gen.controller as controller, secrets, json

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect(url_for('home'))
  return wrap


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
           response = controller.getUser()
           return redirect(response)
    else:
        return render_template('home.html')



@app.route('/callback', methods=['POST', 'GET'])
def options():
    if 'error' in request.args or 'code' not in request.args:
        return redirect(url_for('home'))

    controller.getUserToken(request.args['code'])
    return redirect(url_for('playlists'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    controller.refreshToken()

    track = controller.getCurrentTrack()
    if track:
        return {'none': '0', 'track_data': track}
    return {'none': '1'}



@app.route('/player', methods=['POST', 'GET'])
def player():
    controller.refreshToken()
    option = request.json.get('option')
    print(option + '-----------------------')
    controller.playback(int(option))
    return jsonify(test='200')



@app.route('/playlists', methods=['POST', 'GET'])
def playlists():
    controller.refreshToken()
    controller.clearList()
    if request.method == 'GET':
        return render_template('options.html')
    elif request.method == 'POST':
        return jsonify(cleared='200')




@app.route('/make_playlist', methods=['POST', 'GET'])
def make_playlist():
    controller.refreshToken()

    size = int(request.json.get('size'))
    option = str(request.json.get('option'))
    text = request.json.get('text')

    print(f'playlist size: {size}')
    print(f'playlist option: {option}')
    print(f'text: {text}')

    controller.makePlaylist(size, option, text)
    return redirect(url_for('results'))
 


@app.route('/results', methods=['POST', 'GET'])
def results():
    controller.refreshToken()
    tracks, name = controller.getList()
    return render_template('results.html', items={'playlist':tracks, 'display':name})



@app.route('/add_playlist', methods=['POST', 'GET'])
def add_playlist():
    controller.refreshToken()
    controller.addList()
    return jsonify(added='200')


if __name__ == '__main__':
      app.run(debug=True)

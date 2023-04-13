from flask import Flask, render_template, request, redirect, jsonify, url_for, session
from functools import wraps
from playlist_gen.models import User
import playlist_gen.spotifyAPI as spot_api, secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    return redirect(url_for('home'))
  return wrap


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
           User().end_session()
           spotify_auth = spot_api.getAuth()
           return redirect(spotify_auth)
    return render_template('home.html')



@app.route('/callback', methods=['POST', 'GET'])
def options():
    if 'error' in request.args or 'code' not in request.args:
        return redirect(url_for('home'))

    User().start_session(request.args['code'])
    return redirect(url_for('playlists'))


@app.route('/update', methods=['POST', 'GET'])
@login_required
def update():
    User().refresh_token()
    track = User().get_current_track()
    if track:
        return {'none': '0', 'track_data': track}
    return {'none': '1'}



@app.route('/player', methods=['POST', 'GET'])
@login_required
def player():
    User().refresh_token()
    option = request.json.get('option')
    print(option + '-----------------------')
    User().playback(int(option))
    return jsonify(test='200')



@app.route('/playlists', methods=['POST', 'GET'])
@login_required
def playlists():
    User().refresh_token()
    User().clear_playlist()
    if request.method == 'GET':
        return render_template('options.html')
    elif request.method == 'POST':
        return jsonify(cleared='200')




@app.route('/make_playlist', methods=['POST', 'GET'])
@login_required
def make_playlist():
    User().refresh_token()

    size = int(request.json.get('size'))
    option = str(request.json.get('option'))
    text = request.json.get('text')

    print(f'playlist size: {size}')
    print(f'playlist option: {option}')
    print(f'text: {text}')

    User().make_playlist(size, option, text)
    return redirect(url_for('results'))
 


@app.route('/results', methods=['POST', 'GET'])
@login_required
def results():
    User().refresh_token()
    name, tracks = User().get_playlist()
    return render_template('results.html', items={'playlist':tracks, 'display':name})



@app.route('/add_playlist', methods=['POST', 'GET'])
@login_required
def add_playlist():
    User().refresh_token()
    User().playlist_to_spotify()
    return jsonify(added='200')


if __name__ == '__main__':
      app.run(debug=True)

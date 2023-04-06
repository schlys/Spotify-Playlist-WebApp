from flask import session
import playlist_gen.spotifyAPI as spot_api
import playlist_gen.playlists as p
import time

PLAYLIST_OPTIONS = {
    'curr': p.curr_track_playlist,
    'song': p.track_playlist,
    'genre': p.genre_playlist,
    'artist': p.artist_playlist,
    'rand': p.random_playlist
}

class User:

    def start_session(self, code):
        session['playlist'] = {}
        session['token_data'] = spot_api.getToken(code)
        session['logged_in'] = True

    def end_session(self):
        session.clear()

    def refresh_token(self):
        if time.time() > session['token_data']['expiration']:
            print('refreshing')
            session['token_data'] = spot_api.refreshAuth()

    def get_current_track(self):
        return spot_api.getCurrTrack(session['token_data']['auth_head'])
    
    def playback(self, option):
        return spot_api.player(option, session['token_data']['auth_head'])
    
    def make_playlist(self, size, option, text):
        session['playlist'] = PLAYLIST_OPTIONS[option](size, session['token_data']['auth_head'], text)

    def get_playlist(self):
        return session['playlist']['display'], session['playlist']['tracks']
    
    def playlist_to_spotify(self):
        spot_api.makePlaylist(session['playlist']['display']['text'], session['playlist']['uris'], session['token_data']['auth_head'])

    def clear_playlist(self):
        session['playlist'].clear()
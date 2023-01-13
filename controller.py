import spotifyAPI as api
import playlists as p
import os

#Add your client ID
CLIENT_ID = os.environ.get('CLIENT_ID')

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

#Port and callback url can be changed or left to localhost:5000
PORT = '5000'
CALLBACK_URL = os.environ.get('CALLBACK_URL')

#Add needed scope from spotify user
SCOPE = 'user-read-private user-read-email user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private'

#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
TOKEN_DATA = []

PLAYLIST_OPTIONS = {
    'curr_track': p.currTrackPlaylist,
    'track': p.trackPlaylist,
    'genre': p.genrePlaylist,
    'artist': p.artistPlaylist,
    'random': p.randomPlaylist
}

def getUser():
    return api.getAuth(CLIENT_ID, CALLBACK_URL, SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = api.getToken(code, CLIENT_ID, CLIENT_SECRET, CALLBACK_URL)

# def refreshToken(time):
#     time.sleep(time)
#     TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA

def getCurrentTrack():
    return api.getCurrTrack(TOKEN_DATA[1])

def playback(option):
    return api.player(option, TOKEN_DATA[1])

def makePlaylist(size, option, text):
    PLAYLIST_OPTIONS[option](size, TOKEN_DATA[1], text)

def getList():
    return p.getPlaylist()

def clearList():
    p.playlistReset()

def addList():
    p.addToSpotify(TOKEN_DATA[1])


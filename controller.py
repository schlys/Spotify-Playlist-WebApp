from spotifyAPI import getAuth, getToken, getCurrTrack, player
from playlists import genrePlaylist, currTrackPlaylist, artistPlaylist, trackPlaylist, randomPlaylist, getPlaylist, playlistReset, addToSpotify
import os

#Add your client ID
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

#Port and callback url can be changed or left to localhost:5000
PORT = '5000'
CALLBACK_URL = 'http://samch.pythonanywhere.com/callback/'

#Add needed scope from spotify user
SCOPE = 'user-read-private user-read-email user-library-modify playlist-read-private user-library-read playlist-read-collaborative streaming user-read-currently-playing user-follow-modify playlist-modify-private user-top-read user-read-recently-played playlist-modify-public user-read-playback-state'
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
TOKEN_DATA = []

PLAYLIST_OPTIONS = {
    'curr_track': currTrackPlaylist,
    'track': trackPlaylist,
    'genre': genrePlaylist,
    'artist': artistPlaylist,
    'random': randomPlaylist
}

def getUser():
    return getAuth(CLIENT_ID, CALLBACK_URL, SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, CALLBACK_URL)

# def refreshToken(time):
#     time.sleep(time)
#     TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA

def getCurrentTrack():
    return getCurrTrack(TOKEN_DATA[1])

def playback(option):
    return player(option, TOKEN_DATA[1])

def makePlaylist(size, option, text):
    PLAYLIST_OPTIONS[option](size, TOKEN_DATA[1], text)

def getList():
    return getPlaylist()

def clearList():
    playlistReset()

def addList():
    addToSpotify(TOKEN_DATA[1])


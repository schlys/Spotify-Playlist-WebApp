import math, random, playlist_gen.spotifyAPI as spotifyAPI
from random_word import RandomWords
r = RandomWords()

PLAYLIST = []
PLAYLIST_URIS = []
NAME = {}

def playlistHelper(size, head, track_id, artist_id, rec_mult, artist_mult):
    artist = spotifyAPI.getArtists(artist_id, head)
    genres = artist['genres']

    rec_amt = math.floor(size * rec_mult)
    pop_tracks = spotifyAPI.getRecommendedTracks(artist_id, genres, track_id, 100, 56, head)
    unpop_tracks = spotifyAPI.getRecommendedTracks(artist_id, genres, track_id, 55, 0, head)
    all_rec_tracks = pop_tracks + unpop_tracks
    random.shuffle(all_rec_tracks)

    artist_amt = math.floor(size * artist_mult)
    albums = spotifyAPI.getAlbums(artist_id, head)
    related_artists = spotifyAPI.getRelatedArtists(artist_id, head)

    print(f"Amount of popular tracks: {len(pop_tracks)}")
    print(f"Amount of less popular tracks: {len(unpop_tracks)}")

    i = 0
    j = 0
    count = 1
    while len(PLAYLIST_URIS) < size:
        track = ''
        image = ''
        not_in = True
        
        if i < rec_amt and i < len(all_rec_tracks):
            track = all_rec_tracks[i]
            image = track['album']['images'][0]['url']
            i += 1
        elif j < artist_amt:
            if albums:
                album = albums[random.randint(0, len(albums) - 1)]
                album_tracks = spotifyAPI.getAlbumTracks(album['id'], head)
                track = album_tracks[random.randint(0, len(album_tracks) - 1)]
                not_in = track['uri'] not in PLAYLIST_URIS
                image = album['images'][0]['url']
                j += 1
        else:
            if related_artists:
                rel_artist = related_artists[random.randint(0, len(related_artists) - 1)]
                top_tracks = spotifyAPI.getPopTracks(rel_artist['id'], head)
                track = top_tracks[random.randint(0, len(top_tracks) - 1)]
                not_in = track['uri'] not in PLAYLIST_URIS
                image = track['album']['images'][0]['url']
        if not_in:
            addToPlaylist(track, count, image)
            count +=1

def genrePlaylist(size, head, genre):
    global NAME
    NAME = {'type': 'text', 'text': genre}
    tracks = spotifyAPI.searchGenre(genre, head, 'track')
    artists = spotifyAPI.searchGenre(genre, head, 'artist')
    random.shuffle(tracks)

    track_amt = math.floor(size * .125)

    if tracks and artists:
        i = 0
        count = 1
        while len(PLAYLIST_URIS) < size:
            track = ''
            not_in = True

            if i < track_amt and i < len(tracks):
                track = tracks[i]
                i += 1
            else:
                artist = artists[random.randint(0, len(artists) - 1)]
                top_tracks = spotifyAPI.getPopTracks(artist['id'], head)
                track = top_tracks[random.randint(0, len(top_tracks) - 1)]

            not_in = track['uri'] not in PLAYLIST_URIS
            image = track['album']['images'][0]['url']

            if not_in:
                addToPlaylist(track, count, image)
                count += 1

def currTrackPlaylist(size, head, text):
    global NAME
    track = spotifyAPI.getCurrTrack(head)
    NAME = {
            'type': 'track', 
            'name': track['name'], 
            'artists': track['artists'], 
            'image': track['image'],
            'text': track['name']
        }
    playlistHelper(size, head, track['id'], track['artist_id'], .7, .05)

def artistPlaylist(size, head, text):
    global NAME
    artist = spotifyAPI.getTrackOrArtist(text, head, 'artist')
    top_tracks = spotifyAPI.getPopTracks(artist['id'], head)
    track_id = top_tracks[random.randint(0, len(top_tracks) - 1)]['id']
    NAME = {
            'type': 'artist', 
            'name': artist['name'], 
            'image': artist['image'],
            'text': artist['name']
        }
    playlistHelper(size, head, track_id, artist['id'], .4, .3)

def trackPlaylist(size, head, text):
    global NAME
    track = spotifyAPI.getTrackOrArtist(text, head, 'track')
    NAME = {
            'type': 'track', 
            'name': track['name'], 
            'artists': track['artists'], 
            'image': track['image'],
            'text': track['name']
        }
    playlistHelper(size, head, track['id'], track['artist_id'], .7, .05)

def randomPlaylist(size, head, text):
    global NAME
    words = []
    count = 1

    while len(PLAYLIST_URIS) < size:
        word = r.get_random_word(hasDictionaryDef='true', includePartOfSpeech='noun,verb', minCorpusCount=5)
        print(f"Random word is {word}")
        word_track = spotifyAPI.getTrackOrArtist(word, head, 'track')
        
        if word_track and word != None:
            genres = spotifyAPI.getArtists(word_track['artist_id'], head)['genres']
            rec_tracks = spotifyAPI.getRecommendedTracks(word_track['artist_id'], genres, word_track['id'], 100, 0, head)
            
            if rec_tracks and len(rec_tracks) > 0:
                words.append(word)
                i=0
                while i < math.floor(size * .25) and len(PLAYLIST_URIS) < size and i < len(rec_tracks):
                    track = rec_tracks[i]
                    image = track['album']['images'][0]['url']
                    not_in = track['uri'] not in PLAYLIST_URIS
                    if not_in:
                        addToPlaylist(track, count, image)
                        count += 1
                    i +=1
    NAME = {'type': 'text', 'text': ', '.join(words)}

def getPlaylist():
    return PLAYLIST, NAME

def playlistReset():
    PLAYLIST.clear() 
    PLAYLIST_URIS.clear()
    NAME.clear()

def addToSpotify(head):
    spotifyAPI.makePlaylist(NAME['text'], PLAYLIST_URIS, head)

def addToPlaylist(track, count, image):
    PLAYLIST_URIS.append(track['uri'])
    artist_list = track['artists']
    artists_name = ', '.join([artist['name'] for artist in artist_list])

    PLAYLIST.append({
        'name': track['name'],
        'artists': artists_name,
        'image': image,
        'link': track['external_urls']['spotify']
    })
    print(f"{count}. {track['name']}, {artists_name}")


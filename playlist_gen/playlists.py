import math, random, playlist_gen.spotifyAPI as spotifyAPI
from random_word import RandomWords
r = RandomWords()


def playlist_helper(size, head, track_id, artist_id, rec_mult, artist_mult):
    playlist = []
    playlist_uris = []

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
    while len(playlist_uris) < size:
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
                not_in = track['uri'] not in playlist_uris
                image = album['images'][0]['url']
                j += 1
        else:
            if related_artists:
                rel_artist = related_artists[random.randint(0, len(related_artists) - 1)]
                top_tracks = spotifyAPI.getPopTracks(rel_artist['id'], head)
                track = top_tracks[random.randint(0, len(top_tracks) - 1)]
                not_in = track['uri'] not in playlist_uris
                image = track['album']['images'][0]['url']
        if not_in:
            add_to_playlist(track, count, image, playlist, playlist_uris)
            count +=1
    return playlist, playlist_uris



def genre_playlist(size, head, genre):
    playlist = []
    playlist_uris = []

    display = {'type': 'text', 'text': genre}
    tracks = spotifyAPI.searchGenre(genre, head, 'track')
    artists = spotifyAPI.searchGenre(genre, head, 'artist')
    random.shuffle(tracks)

    track_amt = math.floor(size * .125)

    if tracks and artists:
        i = 0
        count = 1
        while len(playlist_uris) < size:
            track = ''
            not_in = True

            if i < track_amt and i < len(tracks):
                track = tracks[i]
                i += 1
            else:
                artist = artists[random.randint(0, len(artists) - 1)]
                top_tracks = spotifyAPI.getPopTracks(artist['id'], head)
                track = top_tracks[random.randint(0, len(top_tracks) - 1)]

            not_in = track['uri'] not in playlist_uris
            image = track['album']['images'][0]['url']

            if not_in:
                add_to_playlist(track, count, image)
                count += 1
    return to_json(display, playlist, playlist_uris)



def curr_track_playlist(size, head, text):
    track = spotifyAPI.getCurrTrack(head)
    display = {
            'type': 'track', 
            'name': track['name'], 
            'artists': track['artists'], 
            'image': track['image'],
            'text': track['name']
        }
    playlist, playlist_uris = playlist_helper(size, head, track['id'], track['artist_id'], .7, .05)
    return to_json(display, playlist, playlist_uris)



def artist_playlist(size, head, text):
    artist = spotifyAPI.getTrackOrArtist(text, head, 'artist')
    top_tracks = spotifyAPI.getPopTracks(artist['id'], head)
    track_id = top_tracks[random.randint(0, len(top_tracks) - 1)]['id']
    display = {
            'type': 'artist', 
            'name': artist['name'], 
            'image': artist['image'],
            'text': artist['name']
        }
    playlist, playlist_uris = playlist_helper(size, head, track_id, artist['id'], .4, .3)
    return to_json(display, playlist, playlist_uris)



def track_playlist(size, head, text):
    track = spotifyAPI.getTrackOrArtist(text, head, 'track')
    display = {
            'type': 'track', 
            'name': track['name'], 
            'artists': track['artists'], 
            'image': track['image'],
            'text': track['name']
        }
    playlist, playlist_uris = playlist_helper(size, head, track['id'], track['artist_id'], .7, .05)
    return to_json(display, playlist, playlist_uris)



def random_playlist(size, head, text):
    playlist = []
    playlist_uris = []
    words = []
    count = 1

    while len(playlist_uris) < size:
        word = r.get_random_word(hasDictionaryDef='true', includePartOfSpeech='noun,verb', minCorpusCount=5)
        print(f"Random word is {word}")
        word_track = spotifyAPI.getTrackOrArtist(word, head, 'track')
        
        if word_track and word != None:
            genres = spotifyAPI.getArtists(word_track['artist_id'], head)['genres']
            rec_tracks = spotifyAPI.getRecommendedTracks(word_track['artist_id'], genres, word_track['id'], 100, 0, head)
            
            if rec_tracks and len(rec_tracks) > 0:
                words.append(word)
                i=0
                while i < math.floor(size * .25) and len(playlist_uris) < size and i < len(rec_tracks):
                    track = rec_tracks[i]
                    image = track['album']['images'][0]['url']
                    not_in = track['uri'] not in playlist_uris
                    if not_in:
                        add_to_playlist(track, count, image)
                        count += 1
                    i +=1
    display = {'type': 'text', 'text': ', '.join(words)}
    return to_json(display, playlist, playlist_uris)



def to_json(display, playlist, uris):
    return {
        'display': display,
        'tracks': playlist,
        'uris': uris
    }



def add_to_playlist(track, count, image, playlist, playlist_uris):
    playlist_uris.append(track['uri'])
    artist_list = track['artists']
    artists_name = ', '.join([artist['name'] for artist in artist_list])

    playlist.append({
        'name': track['name'],
        'artists': artists_name,
        'image': image,
        'link': track['external_urls']['spotify']
    })
    print(f"{count}. {track['name']}, {artists_name}")


import base64, json, requests, time

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token'
RESPONSE_TYPE = 'code'
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''
PLAYER_URLS = ['https://api.spotify.com/v1/me/player/next',
                'https://api.spotify.com/v1/me/player/previous',
                'https://api.spotify.com/v1/me/player/pause',
                'https://api.spotify.com/v1/me/player/play'
            ]

def getAuth(client_id, redirect_uri, scope):
    data = f"{SPOTIFY_URL_AUTH}client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}&show_dialog=true"
    return data

def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        'grant_type': 'authorization_code',
        'code' : code,
        'redirect_uri': redirect_uri
    }

    headers = getAuthHeaders(client_id, client_secret)

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)

    return handleToken(json.loads(post.text))

def refreshAuth(client_id, client_secret):
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : REFRESH_TOKEN
    }

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=getAuthHeaders(client_id, client_secret))
   
    return handleToken(json.loads(post_refresh.text))

def getAuthHeaders(client_id, client_secret):
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    return {
        'Content-Type' : HEADER,
        'Authorization' : f"Basic {client_creds_b64.decode()}"
    }

def handleToken(response):
    global REFRESH_TOKEN
    auth_head =  {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(response['access_token'])
        }
    
    if 'refresh_token' in response:
        REFRESH_TOKEN = response['refresh_token']
    
    return [response['access_token'], auth_head, response['scope'], response['expires_in'] + time.time()]

def getCurrTrack(head):
    response = requests.get('https://api.spotify.com/v1/me/player?market=US', headers = head)
    if response.ok:
        resp_json = response.json()
        artists = resp_json['item']['artists']
        artists_name = ', '.join([artist['name'] for artist in artists])
        link = ''
        image = ''
        if resp_json['item']['id']:
            link = resp_json['item']['external_urls']['spotify']
            image = resp_json['item']['album']['images'][0]['url']
        else:
            link = 'none'
            image = 'https://cdn140.picsart.com/303222029812211.png?type=webp&to=min&r=640'
        info = {
            'id': resp_json['item']['id'],
            'uri': resp_json['item']['uri'],
            'artist_id': resp_json['item']['artists'][0]['id'],
            'name': resp_json['item']['name'],
            'artists':  artists_name,
            'link': link,
            'image': image,
            'album': resp_json['item']['album']['name'],
            'playing': resp_json['is_playing']
        }
        return info
    return None

def getTrackOrArtist(text, head, kind):
    response = requests.get(f"https://api.spotify.com/v1/search?q={text}&type={kind}&market=US", headers=head)
    if response.ok:
        info = {}
        resp_json = response.json()
        if kind == 'track' and len(resp_json['tracks']['items']) > 0:
            track = resp_json['tracks']['items'][0]
            artists = track['artists']
            artists_name = ', '.join([artist['name'] for artist in artists])
            info = {
                'id': track['id'],
                'uri': track['uri'],
                'artist_id': track['artists'][0]['id'],
                'name': track['name'],
                'artists':  artists_name,
                'link': track['external_urls']['spotify'],
                'image': track['album']['images'][0]['url'],
                'album': track['album']['name']
            }
        elif kind == 'artist' and len(resp_json['artists']['items']) > 0:
            artist = resp_json['artists']['items'][0]
            info = {
                'id': artist['id'],
                'uri': artist['uri'],
                'name': artist['name'],
                'image': artist['images'][0]['url'],
                'link': artist['external_urls']['spotify'],
                'genres': artist['genres']
            }
        return info
    return None

def searchGenre(genre, head, kind):
    response = requests.get(f"https://api.spotify.com/v1/search?q=genre%3A{genre}&type={kind}&market=US&limit=50", headers = head)
    if response.ok:
        resp_json = response.json()
        if kind == 'track':
            return resp_json['tracks']['items']
        else:
            return resp_json['artists']['items']
    return None

def getArtists(artist_id, head):
    response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers = head)
    if response.ok:
        resp_json = response.json()
        info = {
            'genres': resp_json['genres'],
            'artist_id': resp_json['id']
        }
        return info
    return None

def getRecommendedTracks(artists, genres, tracks, max_pop, min_pop, head):
    if len(genres) > 3:
        genres = [genres[0], genres[1], genres[2]]
    genres_string = ','.join(genres)
    response = requests.get(f"https://api.spotify.com/v1/recommendations?limit=100&market=US&seed_artists={artists}&seed_genres={genres_string}&seed_tracks={tracks}&max_popularity={max_pop}&min_popularity={min_pop}", headers = head)
    if response.ok:
        resp_json = response.json()
        return resp_json['tracks']
    return None

def getAlbums(artist_id, head):
    response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single&market=US&limit=25", headers = head)
    if response.ok:
        resp_json = response.json()
        return resp_json['items']
    return None

def getAlbumTracks(album_id, head):
    response = requests.get(f"https://api.spotify.com/v1/albums/{album_id}/tracks?market=US", headers = head)
    if response.ok:
        resp_json = response.json()
        return resp_json['items']
    return None

def getRelatedArtists(artist_id, head):
    response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/related-artists", headers = head)
    if response.ok:
        resp_json = response.json()
        return resp_json['artists']
    return None

def getPopTracks(artist_id, head):
    response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US", headers = head)
    if response.ok:
        resp_json = response.json()
        return resp_json['tracks']
    return None


def player(option, head):
    if option < 2:
        requests.post(PLAYER_URLS[option], headers = head)
    else:
        requests.put(PLAYER_URLS[option], headers = head)

def makePlaylist(name, track_uris, head):
    user_resp = requests.get("https://api.spotify.com/v1/me", headers = head)
    user_id = user_resp.json()['id']
    create = requests.post(f"https://api.spotify.com/v1/users/{user_id}/playlists", data = json.dumps({
        'name': f"playlist based on {name}",
        'description': 'created by http://samch.pythonanywhere.com',
        'public': True
    }), headers = head)
    playlist_id = create.json()['id']
    if len(track_uris) < 100:
        uris = ','.join(track_uris)
        requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={uris}", headers = head)
    else:
        half = len(track_uris)//2
        first = track_uris[:half]
        second = track_uris[half:]
        first_uris = ','.join(first)
        second_uris = ','.join(second)

        requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={first_uris}", headers = head)
        requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={second_uris}", headers = head)

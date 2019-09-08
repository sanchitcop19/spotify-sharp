import sys
import spotipy

if len(sys.argv) >= 2 and sys.argv[1] == "local":
    from query_id import *
    from config import *
    from playlist import *
else:
    from .query_id import *
    from .config import *
    from .playlist import *

def add_top(artist, token):
    spotify = spotipy.Spotify(auth = token)
    response = query(spotify, artist)
    artist_info = response['artists']['items'][0]
    # TODO: handle empty result
    artist_id = artist_info['id']
    artist_title = artist_info['name']
    artist_name = artist_title
    artist_title = '+'.join(word.capitalize() for word in artist_title.split())
    # TODO: If 'error' in response playlist not created
    playlist_id = add_top_playlist(spotify, artist_name)
    try:
        add_top_tracks(spotify, artist_id, playlist_id)
        save_playlist(playlist_id)
    except Exception as e:
        print(e)
        delete_playlist(spotify, playlist_id)
    return

def add_all(artist, token):
    spotify = Spotify(auth = token)
    response = query(spotify, artist)
    artist_info = response['artists']['items'][0]
    # TODO: handle empty result
    artist_id = artist_info['id']
    artist_title = artist_info['name']
    artist_name = artist_title
    artist_title = '+'.join(word.capitalize() for word in artist_title.split())
    # TODO: If 'error' in response playlist not created
    playlist_id = add_all_playlist(spotify, artist_name)
    try:
        add_all_tracks(spotify, artist_id, playlist_id)
        save_playlist(playlist_id)
    except Exception as e:
        print(e)
        delete_playlist(spotify, playlist_id)
    return

def add_bpm(bpm, token):
    spotify = Spotify(auth = token)
    playlist_id = add_bpm_playlist(spotify, bpm)
    try:
        num_tracks = add_bpm_tracks(spotify, playlist_id, bpm)
        save_playlist(playlist_id)
        return True, num_tracks
    except Exception as e:
        print(e)
        delete_playlist(spotify, playlist_id)
        return False, 0

if __name__ == "__main__":

    artist = sys.argv[1]
    #main(artist)
    add_all(artist, None)

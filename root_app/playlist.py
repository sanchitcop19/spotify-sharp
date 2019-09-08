import os
import pickle
import sys
if len(sys.argv) >= 2 and sys.argv[1] == "local":
    from config import *
    from wrappers import *
else:
    from .config import *
    from .wrappers import current_user_all_saved_tracks

def add_top_playlist(spotify, artist_name):
    """
    :param spotify: The main spotify object used to make requests
    :param artist_name: The name of the artist whose top tracks are being added
    :returns: ID of the playlist created
    """
    response = spotify.user_playlist_create(spotify.me()["id"], f"Best of {artist_name}", True, f"Top tracks by {artist_name}")
    return response['id']

def add_bpm_playlist(spotify, bpm):
    """
    :param spotify: The main spotify object used to make requests
    :returns: ID of the playlist created
    """
    response = spotify.user_playlist_create(spotify.me()["id"], f"{bpm} BPM")
    me = spotify.me()
    return response['id']

def add_all_playlist(spotify, artist_name):
    """
    :param spotify: The main spotify object used to make requests
    :param artist_name: The name of the artist, all of whose tracks are being added
    :returns: ID of the playlist created
    """
    response = spotify.user_playlist_create(spotify.me()["id"], f"All of {artist_name}")
    return response['id']

def add_top_tracks(spotify, artist_id, playlist_id):
    """
    :param spotify: The main spotify object used to make requests
    :param artist_id: Spotify ID of the artist whose top tracks are queried
    :returns: ID of the playlist to which the top tracks are being added
    """
    top_tracks = spotify.artist_top_tracks(artist_id)
    top_tracks = [track['id'] for track in top_tracks['tracks']]
    spotify.user_playlist_add_tracks(spotify.me()["id"], playlist_id, top_tracks)


def save_playlist(playlist_id):
    """
    Save playlist IDs to avoid querying them again
    :param playlist_id: ID of the playlist being saved
    """
    playlists = set()
    if os.path.exists("playlists.pickle"):
        with open("playlists.pickle", "rb") as file:
            playlists = pickle.load(file)
        if not playlists:
            print("Could not load playlists")
    playlists.add(playlist_id)
    #TODO: check if these are being written somewhere

def delete_playlist(spotify, playlist_id):
    """
    Delete playlist, usually used if there was an exception
    :param spotify: The main spotify object used to make requests
    :param playlist_id: ID of the playlist being deleted
    """
    spotify.user_playlist_unfollow(spotify.me()["id"], playlist_id)

def add_all_tracks(spotify, artist, playlist):
    """
    Add all tracks by an artist to the playlist specified
    :param spotify: The main spotify object used to make requests
    :param playlist: ID of the playlist being deleted
    """
    store = set()
    def remove_duplicates(album):
        if album['name'] not in store:
            return True
        else:
            store.add(album['name'])
            return False

    response = spotify.artist_albums(artist, album_type = 'album', limit = 50)

    _albums = [album for album in response['items']]
    albums = []

    for album in _albums:
        if album['name'].lower() not in store:
            albums.append(album)
            store.add(album['name'].lower())

    album_tracks = [spotify.album_tracks(album['id'])['items'] for album in albums]

    tracks = [track['id'] for album in album_tracks for track in album]
    _tracks = [tracks[i:i + ADD_TRACKS_LIMIT] for i in range(0, len(tracks), ADD_TRACKS_LIMIT)]
    for tracks in _tracks:
        spotify.user_playlist_add_tracks(spotify.me()["id"], playlist, tracks)

def add_bpm_tracks(spotify, playlist, bpm):
    tracks = None
    ROOT = ROOT_NAME
    import pickle
    if len(sys.argv) >= 2 and sys.argv[1] == "local":
        ROOT = ''

    #TODO: cache user saved tracks
    me = spotify.me()
    id = me["id"]
    tracks = current_user_all_saved_tracks(spotify)
    #with open(ROOT + "saved_tracks.json", "r") as file:
    #    tracks = pickle.load(file)[str(me["id"])]
    import json
    store = {}
    with open(ROOT + "saved_tracks.json", "r") as file:
        store = json.load(file)
    if id not in store:
        with open(ROOT + "saved_tracks.json", "w") as file:
            store[me["id"]] = tracks
            json.dump(store, file, indent=4)

    analysis = {}

    with open(ROOT + "analysis.json", "r") as file:
        analysis = json.load(file)
        for track in tracks:
            if track not in analysis:
                analysis[track] = spotify.audio_analysis(track)["track"]["tempo"]

    with open(ROOT + "analysis.json", "w") as file:
        json.dump(analysis, file, indent=4)

    all_tracks = [track for track in tracks if (abs(analysis[track] - bpm) <= TOLERANCE_TEMPO)]

    if all_tracks:
        start = ADD_TRACKS_LIMIT
        stop = 2*ADD_TRACKS_LIMIT

        spotify.user_playlist_add_tracks(spotify.me()["id"], playlist, all_tracks[:ADD_TRACKS_LIMIT])
        while start < len(all_tracks):
            spotify.user_playlist_add_tracks(spotify.me()["id"], playlist, all_tracks[start:stop])
            start += ADD_TRACKS_LIMIT
            stop += ADD_TRACKS_LIMIT
    return len(all_tracks)



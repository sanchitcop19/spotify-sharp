def current_user_all_saved_tracks(spotify):

    offset = 0
    saved_tracks = []
    tracks = spotify.current_user_saved_tracks(limit=50, offset=offset)
    while tracks['next']:
        saved_tracks.extend([track["track"]["id"] for track in tracks["items"]])
        offset += 50
        tracks = spotify.current_user_saved_tracks(limit=50, offset=offset)
    saved_tracks.extend([track["track"]["id"] for track in tracks["items"]])
    return saved_tracks
import json

def handle_nan(value):
    # if the value is NaN replace it with None (for valid JSON)
    if isinstance(value, float) and (value != value): 
        return None
    return value


def track_ids_to_data(track_data, track_ids):
    data = []
    if not isinstance(track_ids, list):
        track_ids = [track_ids]

    for track_id in track_ids:
        track_info = track_data.loc[track_id]
        
        data.append({
            "id": track_id,
            "title": handle_nan(track_info[("track", "title")]),
            "artist": handle_nan(track_info[("artist", "name")]),
            "runtime": handle_nan(track_info[("track", "duration")]),
            "albumCover": handle_nan(track_info[("track", "track_image_file")]),
            "link": handle_nan(track_info[("track","track_url")]),
            "artistLink": handle_nan(track_info[("track", "artist_url")]),
            "album": handle_nan(track_info[("album", "title")]),
            "albumLink": handle_nan(track_info[("track", "album_url")]),
            "topGenre": handle_nan(track_info[("track", "genre_top")])
        })
    
    if len(data) == 1:
        return json.dumps(data[0], default=str)
    return json.dumps(data, default=str)

def album_ids_to_data(album_data, album_ids):
    data = []

    if not isinstance(album_ids, list):
        album_ids = [album_ids]

    for album_id in album_ids:
        album_info = album_data.loc[album_id]

        data.append({
            "id": album_id,
            "title": handle_nan(album_info[("album_title")]),
            "artist": handle_nan(album_info[("artist_name")]),
            "releaseDate": handle_nan(album_info[("album_date_released")]),
            "albumCover": handle_nan(album_info[("album_image_file")]),
            "noOfTracks": handle_nan(album_info[("album_tracks")]),
            "link": handle_nan(album_info[("album_url")])
        })
    
    if len(data) == 1:
        return json.dumps(data[0], default=str)
    return json.dumps(data, default=str)

def artist_ids_to_data(artist_data, artist_ids):
    data = []
    if not isinstance(artist_ids, list):
        artist_ids = [artist_ids]
    for artist_id in artist_ids:
        artist_info = artist_data.loc[artist_id]

        data.append({
            "id": artist_id,
            "name": handle_nan(artist_info[("artist_name")]),
            "artistImage" : handle_nan(artist_info[("artist_image_file")]),
            "link": handle_nan(artist_info[("artist_url")]),
        })
    if len(data) == 1:
        return json.dumps(data[0], default=str)
    return json.dumps(data, default=str)
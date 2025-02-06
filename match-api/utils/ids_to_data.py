import json

def handle_nan(value):
    # if the value is NaN replace it with None (for valid JSON)
    if isinstance(value, float) and (value != value): 
        return None
    return value

def album_ids_to_data(album_data, album_ids):
    data = []
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

    return json.dumps(data, default=str)

def track_ids_to_data(track_data, track_ids):
    data = []

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

    return json.dumps(data, default=str)


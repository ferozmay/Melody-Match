import json

def album_ids_to_data(album_data, album_ids):
    data = []
    for album_id in album_ids:
        album_info = album_data.loc[album_id]

        data.append({
            "id": album_id,
            "title": album_info[("album_title")],
            "artist": album_info[("")],
            "releaseDate": album_info[("album_date_released")],
            "albumCover": album_info[("album_image_file")],
            "noOfTracks": album_info[("album_tracks")],
            "link": album_info[("album_url")]
        })

    return json.dumps(data, default=str)

def track_ids_to_data(track_data, track_ids):
        data = []

        for track_id in track_ids:
            track_info = track_data.loc[track_id]
            
            data.append({
                "id": track_id,
                "title": track_info[("track", "title")],
                "artist": track_info[("artist", "name")],
                "runtime": track_info[("track", "duration")],
                "albumCover": track_info[("track", "track_image_file")],
                "link": track_info[("track","track_url")],
                "artistLink": track_info[("track", "artist_url")],
                "album": track_info[("album", "title")],
                "albumLink": track_info[("track", "album_url")]
            })

        return json.dumps(data, default=str)

    
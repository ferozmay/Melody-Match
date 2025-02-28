from index.store_load import load_data
import numpy as np
import json


def handle_nan(value):
    # if the value is NaN replace it with None (for valid JSON)
    if isinstance(value, float) and (value != value): 
        return None
    return value


class Index:
    def load_index(self):
        self.track_data, self.album_data, self.artist_data, self.doclengths_track_data, self.doclengths_album_data, self.doclengths_artist_data, self.index = load_data()

    def track_ids_to_data(self, track_ids, include_similar=False):
        track_data = self.track_data
        data = []
        single = False
        if not isinstance(track_ids, list):
            track_ids = [track_ids]
            single = True
        for track_id in track_ids:
            if track_id not in track_data.index:
                continue
            track_info = track_data.loc[track_id]
            similar_songs = []
            if include_similar:
                similar_songs = json.loads(self.track_ids_to_data(track_data.iloc[:10].index.tolist()))
            
            data.append({
                "id": track_id,
                "title": handle_nan(track_info[("track", "title")]),
                "artist": handle_nan(track_info[("artist", "name")]),
                "runtime": handle_nan(track_info[("track", "duration")]),
                "albumCover": handle_nan(track_info[("track", "track_image_file")]),
                "link": handle_nan(track_info[("track", "track_url")]),
                "artistLink": handle_nan(track_info.get(("track", "artist_url"))),
                "album": handle_nan(track_info[("album", "title")]),
                "albumLink": handle_nan(track_info.get(("track", "album_url"))),
                "topGenre": handle_nan(track_info.get(("track", "genre_top"))),
                "similarSongs": similar_songs
            })
        
        if single:
            return json.dumps(data[0], default=str)
        return json.dumps(data, default=str)

    def album_ids_to_data(self, album_ids, include_tracks=False):
        album_data = self.album_data
        data = []
        single = False
        if not isinstance(album_ids, list):
            album_ids = [album_ids]
            single = True

        for album_id in album_ids:
            if album_id not in album_data.index:
                continue
            album_info = album_data.loc[album_id]
            album_tracks = []
            if include_tracks:
                album_tracks = json.loads(
                    self.track_ids_to_data(album_info[("track_ids")]))

            data.append({
                "id": album_id,
                "title": handle_nan(album_info[("album_title")]),
                "artist": handle_nan(album_info[("artist_name")]),
                "releaseDate": handle_nan(album_info[("album_date_released")]),
                "albumCover": handle_nan(album_info[("album_image_file")]),
                "noOfTracks": handle_nan(album_info[("album_tracks")]),
                "link": handle_nan(album_info[("album_url")]),
                "songs": album_tracks
            })

        if single:
            return json.dumps(data[0], default=str)
        return json.dumps(data, default=str)

    def artist_ids_to_data(self, artist_ids, include_tracks=False, include_albums=False):
        artist_data = self.artist_data
        data = []
        single = False
        if not isinstance(artist_ids, list):
            single = True
            artist_ids = [artist_ids]
        for artist_id in artist_ids:
            if artist_id not in artist_data.index:
                continue
            artist_info = artist_data.loc[artist_id]
            albums = []
            songs = []
            if include_albums:
                albums = json.loads(self.album_ids_to_data(
                    artist_info[("album_ids")], include_tracks=True))
            if include_tracks:
                songs = json.loads(self.track_ids_to_data(
                    artist_info[("track_ids")]))
            data.append({
                "id": artist_id,
                "name": handle_nan(artist_info[("artist_name")]),
                "artistImage": handle_nan(artist_info[("artist_image_file")]),
                "link": handle_nan(artist_info[("artist_url")]),
                "songs": songs,
                "albums": albums
            })
        if single:
            return json.dumps(data[0], default=str)
        return json.dumps(data, default=str)
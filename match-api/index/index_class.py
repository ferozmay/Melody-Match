from index.store_load import load_data, store_data
import numpy as np
import json
<<<<<<< HEAD
from utils import parse_id
import ast


similar_songs_dict = {}

with open("data/stored_data/fma_sim_dict.json", "r") as f:
    similar_songs_dict = json.load(f)
=======
import pandas as pd
>>>>>>> 7c0501d4ada6e57b1628f8fe08fb75d59d63e9a4


def handle_nan(value):
    # if the value is NaN replace it with None (for valid JSON)
    if isinstance(value, float) and (value != value): 
        return None
    return value

def is_fma(track_id):
    _id = parse_id(track_id)
    if isinstance(_id, int):
        return True
    return False


class Index:
    def build_index(self):
        store_data()

    def load_index(self):
        self.track_data, self.album_data, self.artist_data, self.doclengths_track_data, self.doclengths_album_data, self.doclengths_artist_data, self.index = load_data()
    
    def get_similar_songs(self, song_id):
        scored_songs = similar_songs_dict.get(str(song_id), [])
        similar_song_ids = [int(song[0]) for song in scored_songs]
        return similar_song_ids

    def track_ids_to_data(self, track_ids, include_similar=False):
        track_data = self.track_data
        data = []
        single = False

        # First ensure we have scalar values
        if isinstance(track_ids, pd.Series):
            track_ids = track_ids.tolist()  # Convert Series to list
            
        if not isinstance(track_ids, list):
            track_ids = [track_ids]
            single = True

        for track_id in track_ids:
            # [track_data["flag"] == flag]
            if track_id not in track_data.index:
                continue

            track_info = track_data.loc[track_id]
            similar_songs = []
            if include_similar:
                if is_fma(track_id):
                    similar_songs = json.loads(self.track_ids_to_data(self.get_similar_songs(track_id)))
                else:
                    items = ast.literal_eval(self.track_data.loc[track_id, ("track", "similars")])
                    similar_songs = list(items.keys())
                    similar_songs = json.loads(self.track_ids_to_data(similar_songs))
                    # similar_songs = self.track_data.loc[track_id][["track", "similars"]]
            genres = track_info[("track", "genres_string")]
            data.append({
                "id": track_id,
                "title": handle_nan(track_info[("track", "title")]),
                "artist": handle_nan(track_info[("artist", "name")]),
                "runtime": handle_nan(track_info[("track", "duration")]),
                "albumCover": handle_nan(track_info[("track", "track_image_file")]),
                "link": handle_nan(track_info[("track", "track_url")]),
                "artistLink": handle_nan(track_info.get(("track", "artist_url"))),
                "artistId": handle_nan(track_info.get(("artist", "id"))),
                "album": handle_nan(track_info[("album", "title")]),
                "albumLink": handle_nan(track_info.get(("track", "album_url"))),
                "genres": genres,
                "albumId": handle_nan(track_info[("album", "id")]),
                "artistId": handle_nan(track_info[("artist", "id")]),
                "similarSongs": similar_songs
            })
        
        if single:
            if data:
                return json.dumps(data[0], default=str)
            return None
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
                album_tracks = json.loads(self.track_ids_to_data(album_info[("track_ids")]))
            
            # # turn album gernres dictionary (id: frequency) into a list of genre ids
            # album_genres = album_info[("album_genres")]
            # album_genres = [genre_id for genre_id, _ in album_genres.items()]
            # # turn genre ids into genre names
            # album_info["album_genres"] = self.genre_ids_to_words(album_genres)
            
            
            data.append({
                "id": album_id,
                "title": handle_nan(album_info[("album_title")]),
                "artist": handle_nan(album_info[("artist_name")]),
                "releaseDate": handle_nan(album_info[("album_date_released")]),
                "albumCover": handle_nan(album_info[("album_image_file")]),
                "noOfTracks": handle_nan(album_info[("album_tracks")]),
                "link": handle_nan(album_info[("album_url")]),
                "genres:": album_info["album_genres_string"],
                "songs": album_tracks,
            })

        if single:
            if data:
                return json.dumps(data[0], default=str)
            return None
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
                "albums": albums,
                "bio": handle_nan(artist_info[("artist_bio")])
            })
        if single:
            if data:
                return json.dumps(data[0], default=str)
            return None
        return json.dumps(data, default=str)

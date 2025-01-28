import numpy as np
import pandas as pd
import ast
import json
from utils.text_processing import process_text


class TrackIndex:
    def load_index(self):
        # Load the data
        self.track_data = pd.read_csv('data/fma_metadata/tracks.csv', index_col=0, header=[0, 1])

        # Drop tracks with no titles
        nan_track_titles = self.track_data[self.track_data[("track", "title")].isna()].index
        self.track_data.drop(nan_track_titles, inplace=True)

        # Process the titles
        track_titles = self.track_data[("track", "title")].apply(process_text)
        # create the index from processed titles {title: track_id}
        self.titles_index = dict(zip(track_titles, self.track_data.index))


    def search(self, query):
        query = process_text(query)
        track_ids = []
        for title in self.titles_index.keys():
            if query in title:
                track_ids.append(self.titles_index[title])
        return track_ids


    def track_ids_to_data(self, track_ids):
        # Load the data
        data = []
        for track_id in track_ids:
            track_info = self.track_data.loc[track_id]
            if track_info[("artist", "website")]:
                print(track_info[("artist", "website")])
                data.append({
                    "id": track_id,
                    "title": track_info[("track", "title")],
                    "artist": track_info[("artist", "name")],
                    "runtime": track_info[("track", "duration")],
                    "albumCover": "https://pure-music.co.uk/wp-content/uploads/2019/04/Thriller-Album-Cover.png",
                    "link": track_info[("artist", "website")] or "",
                })
            else:
                data.append({
                    "id": track_id,
                    "title": track_info[("track", "title")],
                    "artist": track_info[("artist", "name")],
                    "runtime": track_info[("track", "duration")],
                    "albumCover": "https://pure-music.co.uk/wp-content/uploads/2019/04/Thriller-Album-Cover.png",
                })
        return json.dumps(data, default=str)

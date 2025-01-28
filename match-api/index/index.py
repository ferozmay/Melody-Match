import numpy as np
import pandas as pd
import ast
from utils.text_processing import process_text


class TrackIndex:
    def load_index(self):
        # Load the data
        track_data = pd.read_csv('data/fma_metadata/tracks.csv', index_col=0, header=[0, 1])

        # Drop tracks with no titles
        nan_track_titles = track_data[track_data[("track", "title")].isna()].index
        track_data.drop(nan_track_titles, inplace=True)

        # Process the titles
        track_titles = track_data[("track", "title")].apply(process_text)
        # create the index from processed titles {title: track_id}
        self.titles_index = dict(zip(track_titles, track_data.index))


    def search(self, query):
        query = process_text(query)
        track_ids = []
        for title in self.titles_index.keys():
            if query in title:
                track_ids.append(self.titles_index[title])
        return track_ids

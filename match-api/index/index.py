import numpy as np
import pandas as pd
import ast
import json
from utils.text_processing import process_text
import urllib.parse
from index.clean_store_load import load_track_data

class TrackIndex:
    def load_index(self):
        self.track_data, self.titles_index = load_track_data()

    def load_index_slow(self):
        self.track_data_slow = pd.read_csv('data/fma_metadata/tracks.csv', index_col=0, header=[0, 1])

        # Drop tracks with no titles
        nan_track_titles = self.track_data_slow[self.track_data_slow[("track", "title")].isna()].index
        self.track_data_slow.drop(nan_track_titles, inplace=True)

        # Process the titles
        track_titles = self.track_data_slow[("track", "title")].apply(process_text)
        # create the index from processed titles {title: track_id}
        self.titles_index_slow = dict(zip(track_titles, self.track_data_slow.index))
    
    def search(self, query):
        query = process_text(query)
        track_ids = []
        for title in self.titles_index.keys():
            if query in title:
                track_ids.append(self.titles_index[title])
        return track_ids

    def get_google_search_link(song, artist, album):
        google_search = f"Free Music Archive {song} {artist} {album}"
        encoded_search = urllib.parse.quote_plus(google_search)
        return f"https://www.google.com/search?q={encoded_search}"


    def track_ids_to_data(self, track_ids):
        # Load the data
        data = []
        for track_id in track_ids:
            track_info = self.track_data.loc[track_id]
            artist_website = track_info[("artist", "website")]
            # for each of the query results, we create a hyperlink indicating what teh google search for the result would look like
            # this can replace the artist_website if we want or not - can definitely replace for those without a website
            google_search = TrackIndex.get_google_search_link(track_info[("track", "title")], track_info[("artist", "name")], track_info[("album", "title")] )
            # Check if artist_website is nan and handle it
            if isinstance(artist_website, float) and np.isnan(artist_website):
                artist_website = google_search
            data.append({
                "id": track_id,
                "title": track_info[("track", "title")],
                "artist": track_info[("artist", "name")],
                "runtime": track_info[("track", "duration")],
                "albumCover": "https://pure-music.co.uk/wp-content/uploads/2019/04/Thriller-Album-Cover.png",
                "link": google_search, # temporarily using the google search instead of the artist website 
            })
        return json.dumps(data, default=str)

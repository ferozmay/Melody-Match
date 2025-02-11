from index.store_load import load_data

class Index:
    def load_index(self):
        self.track_data, self.album_data, self.artist_data, self.doclengths_track_data, self.doclengths_album_data, self.doclengths_artist_data, self.index = load_data()
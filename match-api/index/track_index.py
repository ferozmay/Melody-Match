from index.clean_store_load import load_track_data

class TrackIndex:
    def load_track_index(self):
        self.track_data, self.index = load_track_data()
from index.clean_store_load import load_album_data

class AlbumIndex:
    
    def load_album_index(self):
        self.album_data, self.album_titles = load_album_data()
    
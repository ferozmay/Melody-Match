import pickle
import pandas as pd
from index.data_cleaning import clean_and_make_data
from index.data_processing import process_data
from index.inverted_index import create_inverted_index

"""This module serves two purpouses:
1. When executed it makes all the data frames we will be using and builds the inverted index. It does this by executing functions imported from 
data_cleaning.py, data_processing.py and inverted_index.py. It then stores the data frames and the inverted index as binary in the data/stored_data folder.
2. It also contains the function load_data() which loads the data frames and the inverted index from the data/stored_data folder. This function is
used to efficiently load the stored data when the app is started from file. This loading is done in the index class."""

def store_data():
    """Executes the function compositions from the data_cleaning and inverted_index modules: namely it executes in sequence clean_and_make_data(),
    process_data() and create_inverted_index(). It then stores the data frames and the inverted index as binary. For most efficient storage the 
    function stores the data frames in a single hdf5 file where each data frame is associated with a key and the inverted index is pickled."""

    # clean and make data
    track_data, album_data, artist_data, genres_data = clean_and_make_data()
    # bundle dfs together
    entire_dfs = (track_data, album_data, artist_data, genres_data)
    # preprocess dfs
    pp_track_data, pp_album_data, pp_artist_data, doclengths_track_data, doclengths_album_data, doclengths_artist_data = process_data(entire_dfs)
    # bundle preprocessed dfs together
    entire_pp_dfs = (pp_track_data, pp_album_data, pp_artist_data)
    entire_doclengths_dfs = (doclengths_track_data, doclengths_album_data, doclengths_artist_data)
    # # create inverted index
    inverted_index = create_inverted_index(entire_pp_dfs)
    # create lists of keys for each data frame we will store
    entire_df_keys = ['track_data_df', 'album_data_df', 'artist_data_df', 'genres_data_df']
    entire_pp_df_keys = ['pp_track_data_df', 'pp_album_data_df', 'pp_artist_data_df']
    entire_doclengths_df_keys = ['doclengths_track_data_df', 'doclengths_album_data_df', 'doclengths_artist_data_df']
    #loop over data frame and key pairs when storing to single hdf5 file
    for df, key  in zip(entire_dfs, entire_df_keys):
        df.to_hdf('data/stored_data/dataframes.h5', key=key , mode='a')
    for df, key in zip(entire_pp_dfs, entire_pp_df_keys):
        df.to_hdf('data/stored_data/dataframes.h5', key=key , mode='a')
    for df, key in zip(entire_doclengths_dfs, entire_doclengths_df_keys):
        df.to_hdf('data/stored_data/dataframes.h5', key=key , mode='a')

    # pickle the inverted index
    with open("data/stored_data/inverted_index.pkl", "wb") as f:
        pickle.dump(inverted_index, f)

def load_data():
    """Loads the data frames and the inverted index from the data/stored_data folder. We only load the necessary ones."""

    # we are now loading teh tracks, artists, albums dfs and the doclengths dfs for ranking
    track_data = pd.read_hdf('data/stored_data/dataframes.h5', key='track_data_df')
    album_data = pd.read_hdf('data/stored_data/dataframes.h5', key='album_data_df')
    artist_data = pd.read_hdf('data/stored_data/dataframes.h5', key='artist_data_df')
    doclengths_track_data = pd.read_hdf('data/stored_data/dataframes.h5', key='doclengths_track_data_df')
    doclengths_album_data = pd.read_hdf('data/stored_data/dataframes.h5', key='doclengths_album_data_df')
    doclengths_artist_data = pd.read_hdf('data/stored_data/dataframes.h5', key='doclengths_artist_data_df')
    with open("data/stored_data/inverted_index.pkl", "rb") as f:
        inverted_index = pickle.load(f)
    return track_data, album_data, artist_data, doclengths_track_data, doclengths_album_data, doclengths_artist_data, inverted_index


if __name__ == "__main__":
    store_data()
    print("Data stored successfully!")

import pickle
import pandas as pd
from index.data_preprocessing.data_cleaning import clean_and_make_data
from index.data_preprocessing.data_processing import process_data
from index.inverted_index import create_inverted_index
import json

"""This module serves two purpouses:
1. Loads, preprocesses dataframes, builds inverted index. Saves dfs and the inverted index as binary in the data/stored_data folder.

2. defines load_data(), loads the dfs and the inverted index from data/stored_data folder. 
Used to efficiently load the stored data 
This loading is done in the index class."""

def store_data():
    """
    1. clean_and_make_data(),
    2. process_data()
    3. create_inverted_index(). 
    Save dfs and the inverted index as binary. 
    For efficient storage stores the dfs in a single hdf5 file
    Each df is associated with a key and the inverted index is pickled."""

    # clean and make data
    track_data, album_data, artist_data, genres_data = clean_and_make_data()

    # bundle dfs together
    entire_dfs = (track_data, album_data, artist_data, genres_data)
    # preprocess dfs
    pp_track_data, pp_album_data, pp_artist_data, doclengths_track_data, doclengths_album_data, doclengths_artist_data = process_data(entire_dfs)
    # bundle preprocessed dfs together
    entire_pp_dfs = (pp_track_data, pp_album_data, pp_artist_data)
    print('pp_dfs loaded')
    print(pp_track_data.head())
    print(pp_track_data.tail())
    print(pp_artist_data.head())
    print(pp_artist_data.tail())
    entire_doclengths_dfs = (doclengths_track_data, doclengths_album_data, doclengths_artist_data)
    # create inverted index
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
    with open ("data/stored_data/inverted_index.pkl", "wb") as f:
        pickle.dump(inverted_index, f)

def load_data():
    """Loads the data frames and the inverted index. We only load the necessary ones."""

    # we are now loading teh tracks, artists, albums dfs and the doclengths dfs for ranking
    track_data = pd.read_hdf('data/stored_data/dataframes.h5', key='track_data_df')
    album_data = pd.read_hdf('data/stored_data/dataframes.h5', key='album_data_df')
    artist_data = pd.read_hdf('data/stored_data/dataframes.h5', key='artist_data_df')
    doclengths_track_data = pd.read_hdf('data/stored_data/dataframes.h5', key='doclengths_track_data_df')
    doclengths_album_data = pd.read_hdf('data/stored_data/dataframes.h5', key='doclengths_album_data_df')
    doclengths_artist_data = pd.read_hdf('data/stored_data/dataframes.h5', key='doclengths_artist_data_df')
    
    with open("data/stored_data/inverted_index.pkl", "rb") as f:
        inverted_index = pickle.load(f)
    # lyrics_index = None
    with open("data/stored_data/lyrics_inverted_word.pkl", "rb") as g:
        lyrics_index = pickle.load(g)

    return track_data, album_data, artist_data, doclengths_track_data, doclengths_album_data, doclengths_artist_data, inverted_index, lyrics_index


if __name__ == "__main__":
    store_data()
    print("Data stored successfully!")

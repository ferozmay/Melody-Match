import pandas as pd
from utils.text_processing import process_text
import pickle
from collections import defaultdict
import numpy as np

# This is a module to compartmentalise the process of cleaning, storing and loading data for different csv files that we want to process before using them in the index
# Running this python file from the match-api directory will:
# Clean and store the data in the data directory, so will avoid being pushed to GitHub
# The stored data can then be loaded more efficiently in the index.py module

def clean_track_data():
    track_data = pd.read_csv('data/fma_metadata/tracks.csv', index_col=0, header=[0, 1])

    # load raw tracks
    raw_tracks = pd.read_csv('data/fma_metadata/raw_tracks.csv')

    # get only the relevant columns from the raw data
    raw_tracks = raw_tracks[["track_id", "track_url", "track_image_file", "artist_url", "album_url"]]
    raw_tracks.set_index("track_id", inplace=True)
    
    # convert raw dfs to a multi-index format
    raw_tracks.columns = pd.MultiIndex.from_tuples([("track", col) for col in raw_tracks.columns])

    # merge with track_data
    track_data = track_data.merge(raw_tracks, left_index=True, right_index=True, how="left")

    # drop tracks with no titles
    nan_track_titles = track_data[track_data[("track", "title")].isna()].index
    track_data.drop(nan_track_titles, inplace=True)

    # process track titles
    track_titles = track_data[("track", "title")].apply(process_text)

    # fix image urls
    track_data[("track", "track_image_file")] = track_data.index.map(lambda x: fix_album_cover_url(track_data, x))

    return track_data, track_titles

def clean_album_data():

    album_data = pd.read_csv('data/fma_metadata/raw_albums.csv', index_col=0, header=[0, 1])

    # drop albums with no titles
    nan_track_titles = album_data[album_data[("album_title")].isna()].index
    album_data.drop(nan_track_titles, inplace=True)

    # process album titles
    album_titles = album_data[("album_title")].apply(process_text)

    # fix image urls
    album_data[("album_image_file")] = album_data.index.map(lambda x: fix_album_cover_url(album_data, x))

    return album_data, album_titles
    
def create_inverted_index(data_df, titles_df):
    token_instances = []
    for track_id, title in zip(data_df.index, titles_df):
        words = title.split()  # tokenize title into words
        for position, word in enumerate(words, start=1):
            token_instances.append((word, track_id, position))
    
    inverted_index = {}
    
    for term, track_id, position in token_instances:

        if term not in inverted_index:
            inverted_index[term] = {'doc_freq': 0, 'docs': {}}

        # +1 doc_freq when we encounter the term in a new title
        if track_id not in inverted_index[term]['docs']:
            inverted_index[term]['doc_freq'] += 1

        # store the position of the term in the title
        if track_id not in inverted_index[term]['docs']:
            inverted_index[term]['docs'][track_id] = []
        inverted_index[term]['docs'][track_id].append(position)

    return inverted_index

def fix_album_cover_url(data_df, track_or_album_id, album=False):

    if not album:
        track_info = data_df.loc[track_or_album_id]
        album_cover_path = track_info[("track", "track_image_file")]
    else:
        album_info = data_df.loc[track_or_album_id]
        album_cover_path = album_info[("album_image_file")]

    placeholder = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"

    
    if isinstance(album_cover_path, float) and np.isnan(album_cover_path):
        return placeholder

    if 'albums' in album_cover_path:
        actual_url = album_cover_path.replace("file/images/albums/", "image/?file=images%2Falbums%2F")
        actual_url = actual_url + "&width=290&height=290&type=album"
    elif 'tracks' in album_cover_path:
        actual_url = album_cover_path.replace("file/images/tracks/", "image/?file=images%2Ftracks%2F")
        actual_url = actual_url + "&width=290&height=290&type=track"
    else:
        return placeholder
    return actual_url


def store_track_data():
    track_data, track_titles = clean_track_data()
    inverted_index = create_inverted_index(track_data, track_titles)
    track_data.to_hdf('data/stored_data/tracks_titles.h5', key='track_titles_df', mode='w')
    with open("data/stored_data/track_inverted_index.pkl", "wb") as f:
        pickle.dump(inverted_index, f)

def load_track_data():
    track_data = pd.read_hdf('data/stored_data/tracks_titles.h5', key='track_titles_df')
    with open("data/stored_data/track_inverted_index.pkl", "rb") as f:
        inverted_index = pickle.load(f)
    return track_data, inverted_index

def store_album_data():
    album_data, album_titles = clean_album_data()
    inverted_index = create_inverted_index(album_data, album_titles)
    album_data.to_hdf('data/stored_data/albums_titles.h5', key='album_titles_df', mode='w')
    with open("data/stored_data/album_inverted_index.pkl", "wb") as f:
        pickle.dump(inverted_index, f)

def load_album_data():
    album_data = pd.read_hdf('data/stored_data/albums_titles.h5', key='album_titles_df')
    with open("data/stored_data/album_inverted_index.pkl", "rb") as f:
        inverted_index = pickle.load(f)
    return album_data, inverted_index

if __name__ == "__main__":
    store_track_data()
    store_album_data()
    print("Data stored successfully!")



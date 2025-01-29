import pandas as pd
from utils.text_processing import process_text
import pickle

# This is a module to compartmentalise the process of cleaning, storing and loading data for different csv files that we want to process before using them in the index
# Running this python file from the match-api directory will:
# Clean and store the data in the data directory, so will avoid being pushed to GitHub
# The stored data can then be loaded more efficiently in the index.py module

def clean_track_data():
    track_data = pd.read_csv('data/fma_metadata/tracks.csv', index_col=0, header=[0, 1])

    # Drop tracks with no titles
    nan_track_titles = track_data[track_data[("track", "title")].isna()].index
    track_data.drop(nan_track_titles, inplace=True)

    # Process the titles
    track_titles = track_data[("track", "title")].apply(process_text)
    # create the index from processed titles {title: track_id}
    titles_index = dict(zip(track_titles, track_data.index))
    return track_data, titles_index

def store_track_data():
    track_data, titles_index = clean_track_data()
    track_data.to_hdf('data/stored_data/tracks_titles.h5', key='track_titles_df', mode='w')
    with open("data/stored_data/titles_index.pkl", "wb") as f:
        pickle.dump(titles_index, f)

def load_track_data():
    track_data = pd.read_hdf('data/stored_data/tracks_titles.h5', key='track_titles_df')
    with open("data/stored_data/titles_index.pkl", "rb") as f:
        titles_index = pickle.load(f)
    return track_data, titles_index

if __name__ == "__main__":
    store_track_data()
    print("Data stored successfully!")



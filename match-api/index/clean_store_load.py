import pandas as pd
from utils.text_processing import process_text
import pickle
from collections import defaultdict
import numpy as np
import ast

# This is a module to compartmentalise the process of cleaning, storing and loading data for different csv files that we want to process before using them in the index
# Running this python file from the match-api directory will:
# Clean and store the data in the data directory, so will avoid being pushed to GitHub
# The stored data can then be loaded more efficiently in the index.py module

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


def clean_track_data():
    track_data = pd.read_csv('data/fma_metadata/tracks.csv', index_col=0, header=[0, 1]) # warning: code later relies on the track id being the index

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

    # fix image urls
    track_data[("track", "track_image_file")] = track_data.index.map(lambda x: fix_album_cover_url(track_data, x))

    # convert genres which are actually strings of the form '[12, 34]' to what they should be which is lists of the form
    # [12, 34] - there are definitely many columns we need to do this to , this is just the only one used so far 
    track_data[('track', 'genres')] = track_data[('track', 'genres')].apply(ast.literal_eval)

    return track_data

def clean_genres_data():
    genres_data = pd.read_csv('data/fma_metadata/genres.csv', index_col=0)
    
    # add genre colors in case we want at some stage
    raw_genres = pd.read_csv('data/fma_metadata/raw_genres.csv', index_col=0)
    raw_genres = raw_genres[[("genre_color")]]
    
    genres_data = genres_data.merge(raw_genres, left_index=True, right_index=True, how="left")

    return genres_data


def make_album_data(track_data):

    album_data = pd.read_csv('data/fma_metadata/raw_albums.csv')
    
    # fix image urls
    album_data[("album_image_file")] = album_data.index.map(lambda x: fix_album_cover_url(album_data, x, True))

    # make a copy of the track data we care about
    # I haven't used the genres_all and genre_top columns but they may be useful to add into the album data
    temp_track_data = track_data[[('album', 'title'), ('track', 'title'), ('track', 'genres'), ('track', 'genres_all'), ('track', 'genre_top')]].copy()

    # group the track data by albums, and gather the songs on each album and the genres of each song
    track_ids = temp_track_data.groupby(('album', 'title')).apply(lambda x: list(x.index), include_groups = False).reset_index(name=('track', 'ids'))

    # group track_data by ('album', 'title') and aggregate track ids and genres into lists
    grouped_track_data = temp_track_data.groupby(('album', 'title')).agg({
        ('track', 'genres'): lambda x: [genre for genre_list in list(x) for genre in genre_list] # flatten the list of lists, since we only care about an album's genre, thus we don't need to know which songs were a certain genre
        # we don't get a set of genres since we want to know how many times a genre appears so we can classify later
    }).reset_index()

    # flatten the mulit-index columns to single indexes
    grouped_track_data.columns = ['_'.join(col) for col in grouped_track_data.columns]
    track_ids.columns = ['_'.join(col) for col in track_ids.columns]
    
    # merge the two grouped dataframes
    grouped_track_data = grouped_track_data.merge(track_ids, left_on='album_title', right_on='album_title', how='left')
    
    # merge to the entire album data frame
    album_data = album_data.merge(grouped_track_data, left_on = 'album_title', right_on='album_title', how='left')

    # after gathering the tracks genres we attempt to classify the album's genre
    album_data['album_genres'] = album_data['track_genres'].apply(create_genre_dict)

    # resetting the index to be the album id (this bit is optional and should be changed if causing problems)
    album_data.set_index('album_id', inplace=True)
    
    return album_data


def make_artist_data(track_data):
    artist_data = pd.read_csv('data/fma_metadata/raw_artists.csv')

    # fix image urls
    # INSERT

    # make a copy of the track data we care about
    temp_track_data = track_data[[('artist', 'name'), ('track', 'title'), ('track', 'genres'), ('track', 'genres_all'), ('track', 'genre_top'), ('album', 'id')]].copy()

    # group the track data by artist, and gather the songs by each artist and the genres of each song
    track_ids = temp_track_data.groupby(('artist', 'name')).apply(lambda x: list(x.index), include_groups = False).reset_index(name=('track', 'ids'))

    # group track_data by ('artist', 'name') and aggregate track ids, album ids and genres of tracks into lists (since genres of albums are jsut derived from songs, no point including)
    grouped_track_data = temp_track_data.groupby(('artist', 'name')).agg({
        ('track', 'genres'): lambda x: [genre for genre_list in list(x) for genre in genre_list] , # once again we only care about the genres from the perspective of classifying the artists genre, so what song is which genre is irrelevant
        ('album', 'id'): lambda x: list(set(x)) # we only count each album once for the artist
    }).reset_index()


    # flatten the mulit-index columns to single indexes
    grouped_track_data.columns = ['_'.join(col) for col in grouped_track_data.columns]
    track_ids.columns = ['_'.join(col) for col in track_ids.columns]

    # merge the two grouped dataframes
    grouped_track_data = grouped_track_data.merge(track_ids, left_on='artist_name', right_on='artist_name', how='left')
    grouped_track_data = grouped_track_data[['artist_name', 'track_genres', 'track_ids', 'album_id']].rename(columns={'album_id': 'album_ids'})

    # merge to the entire artist data frame
    artist_data = artist_data.merge(grouped_track_data, left_on = 'artist_name', right_on='artist_name', how='left')

    # after gathering the tracks genres we attempt to classify the artist's genre
    artist_data['artist_genres'] = artist_data['track_genres'].apply(create_genre_dict)

    # resetting the index to be the artist id (optional)
    artist_data.set_index('artist_id', inplace=True)
    
    return artist_data

def create_genre_dict(genre_list, threshold=0.3):

    if not isinstance(genre_list, list):
        return {}
    if not genre_list:
        return {}
    genre_count = {genre: genre_list.count(genre) for genre in set(genre_list)}
    total_count = len(genre_list)
    
    # filter out genres that do not appear more than the threshold amount of times - setting 30% as default for artists and albums
    genre_dict = {genre: round(count / total_count, 2) for genre, count in genre_count.items() if count / total_count >= threshold}
    
    return genre_dict


def process_track_data(track_data, token_genres_dict):
    # process track titles
    pp_track_data = track_data[[('track', 'title'), ('track', 'genres'), ('track', 'tags')]].copy()

    # flatten multi-index columns - since the preprocessed track data df will only contain track info
    pp_track_data.columns = ['_'.join(col) for col in pp_track_data.columns]

    # this line could also be done with the original data frame instead, so may change to there at some stage
    # is essentially just putting the list of genres for a track in a dict with the genre as a key and teh value being the fraction of genres (ie if 3 genres for track just 1/3)
    pp_track_data[('track_genres')] = pp_track_data[('track_genres')].apply(lambda x : create_genre_dict(x, threshold = 0.0))
    
    # converting the integer representation of genres to token representation
    pp_track_data[('track_genres')] = pp_track_data['track_genres'].apply(lambda track_genres_list: {token_genres_dict[genre]: count for genre, count in track_genres_list.items()})

    # preprocess the other two columns
    pp_track_data[('track_title')] = pp_track_data[('track_title')].apply(process_text)
    pp_track_data[('track_tags')] = pp_track_data[('track_tags')].apply(process_text)

    return pp_track_data

def process_album_data(album_data, token_genres_dict):
    # process album titles
    pp_album_data = album_data[[('album_title'), ('album_genres'),('tags')]].copy()
    pp_album_data = pp_album_data.rename(columns={'tags': 'album_tags'})
    
    # convert the integer representation of genres to token representation, each albums genre(s) were in a dict, now that dict has different keys
    pp_album_data[('album_genres')] = pp_album_data[('album_genres')].apply(lambda album_genres_dict: {token_genres_dict[genre]: count for genre, count in album_genres_dict.items()})   
    
    # preprocess the other two columns
    pp_album_data[('album_title')] = pp_album_data[('album_title')].apply(process_text)
    pp_album_data[('album_tags')] = pp_album_data[('album_tags')].apply(process_text)

    return pp_album_data


def process_artist_data(artist_data, token_genres_dict):
    # process artist names
    pp_artist_data = artist_data[[('artist_name'), ('artist_genres'), ('tags')]].copy()
    pp_artist_data = pp_artist_data.rename(columns={'tags': 'artist_tags'})

    # convert the integer representation of genres to token representation
    pp_artist_data[('artist_genres')] = pp_artist_data[('artist_genres')].apply(lambda artist_genres_dict: {token_genres_dict[genre]: count for genre, count in artist_genres_dict.items()})

    # preprocess the other two columns
    pp_artist_data[('artist_name')] = pp_artist_data[('artist_name')].apply(process_text)
    pp_artist_data[('artist_tags')] = pp_artist_data[('artist_tags')].apply(process_text)

    # pp_artist_data = pp_artist_data.map(process_text)
    return pp_artist_data

def clean_and_make_data():
    track_data = clean_track_data()
    genres_data = clean_genres_data()
    album_data = make_album_data(track_data)
    artist_data = make_artist_data(track_data)
    return track_data, album_data, artist_data, genres_data

def process_data(entire_dfs):
    track_data, album_data, artist_data, genres_data = entire_dfs
    pp_genres_data = genres_data[('title')].apply(process_text)
    genres_dict = pp_genres_data.to_dict()
    pp_track_data = process_track_data(track_data, genres_dict)
    pp_album_data = process_album_data(album_data, genres_dict)
    pp_artist_data = process_artist_data(artist_data, genres_dict)
    
    return pp_track_data, pp_album_data, pp_artist_data, pp_genres_data

def initialize_inverted_index_entry():
    return {
        'Track': {
            'Name': {'doc_freq': 0, 'doc_ids': {}},
            'Genre': {'doc_freq': 0, 'doc_ids': {}},
            'Tag': {'doc_freq': 0, 'doc_ids': []}
        },
        'Album': {
            'Name': {'doc_freq': 0, 'doc_ids': {}},
            'Genre': {'doc_freq': 0, 'doc_ids': {}},
            'Tag': {'doc_freq': 0, 'doc_ids': []}
        },
        'Artist': {
            'Name': {'doc_freq': 0, 'doc_ids': {}},
            'Genre': {'doc_freq': 0, 'doc_ids': {}},
            'Tag': {'doc_freq': 0, 'doc_ids': []}
        }
        }

def add_to_inverted_index(inverted_index, term, object_type, document_type, doc_id, position=None, weight=None):
    # handle the different object types: a track, an album and artist
    # handle the different document types: a name (document is the entire name for the object), a genre (document is the list of genres for the object), a tag (document is the list of tags for the object)
    # initilaise, or add to index
    if term not in inverted_index:
        inverted_index[term] = initialize_inverted_index_entry()
    
    if doc_id not in inverted_index[term][object_type][document_type]['doc_ids']:
        inverted_index[term][object_type][document_type]['doc_freq'] += 1
        if document_type == 'Name':
            inverted_index[term][object_type][document_type]['doc_ids'][doc_id] = []
        if document_type == 'Genre':
            inverted_index[term][object_type][document_type]['doc_ids'][doc_id] = weight
        if document_type == 'Tag':
            inverted_index[term][object_type][document_type]['doc_ids'].append(doc_id)
    if document_type == 'Name':
        inverted_index[term][object_type][document_type]['doc_ids'][doc_id].append(position)


def create_inverted_index(entire_dfs, entire_pp_dfs):
    track_data, album_data, artist_data, genres_data = entire_dfs
    pp_track_data, pp_album_data, pp_artist_data, pp_genres_data = entire_pp_dfs
    inverted_index = dict()

    for index, row in pp_track_data.iterrows():
        
        for position, term in enumerate(row['track_title'].split(), start=1):
            add_to_inverted_index(inverted_index, term, 'Track', 'Name', index, position=position)
        
        # Process track genres
        for genre, weight in row['track_genres'].items():
            add_to_inverted_index(inverted_index, genre, 'Track', 'Genre', index, weight=weight)
        
        # Process track tags
        for tag in row['track_tags'].split():
            add_to_inverted_index(inverted_index, tag, 'Track', 'Tag', index)

    for index, row in pp_album_data.iterrows():
        
        for position, term in enumerate(row['album_title'].split(), start=1):
            add_to_inverted_index(inverted_index, term, 'Album', 'Name', index, position=position)
        
        # Process album genres
        for genre, weight in row['album_genres'].items():
            add_to_inverted_index(inverted_index, genre, 'Album', 'Genre', index, weight=weight)
        
        # Process album tags
        for tag in row['album_tags'].split():
            add_to_inverted_index(inverted_index, tag, 'Album', 'Tag', index)
    
    for index, row in pp_artist_data.iterrows():
        
        for position, term in enumerate(row['artist_name'].split(), start=1):
            add_to_inverted_index(inverted_index, term, 'Artist', 'Name', index, position=position)
        
        # Process artist genres
        for genre, weight in row['artist_genres'].items():
            add_to_inverted_index(inverted_index, genre, 'Artist', 'Genre', index, weight=weight)
        
        # Process artist tags
        for tag in row['artist_tags'].split():
            add_to_inverted_index(inverted_index, tag, 'Artist', 'Tag', index)
    return inverted_index


def store_data():
    track_data, album_data, artist_data, genres_data = clean_and_make_data()
    entire_dfs = (track_data, album_data, artist_data, genres_data)
    pp_track_data, pp_album_data, pp_artist_data, pp_genres_data = process_data(entire_dfs)
    entire_pp_dfs = (pp_track_data, pp_album_data, pp_artist_data, pp_genres_data)
    inverted_index = create_inverted_index(entire_dfs, entire_pp_dfs)
    entire_df_keys = ['track_data_df', 'album_data_df', 'artist_data_df', 'genres_data_df']
    entire_pp_df_keys = ['pp_track_data_df', 'pp_album_data_df', 'pp_artist_data_df', 'pp_genres_data_df']
    for df, key  in zip(entire_dfs, entire_df_keys):
        df.to_hdf('data/stored_data/dataframes.h5', key=key , mode='a')
    for df, key in zip(entire_pp_dfs, entire_pp_df_keys):
        df.to_hdf('data/stored_data/dataframes.h5', key=key , mode='a')
    with open("data/stored_data/inverted_index.pkl", "wb") as f:
        pickle.dump(inverted_index, f)

def load_data():
    track_data = pd.read_hdf('data/stored_data/dataframes.h5', key='track_data_df')
    album_data = pd.read_hdf('data/stored_data/dataframes.h5', key='album_data_df')
    artist_data = pd.read_hdf('data/stored_data/dataframes.h5', key='artist_data_df')
    with open("data/stored_data/inverted_index.pkl", "rb") as f:
        inverted_index = pickle.load(f)
    return track_data, album_data, artist_data, inverted_index

def load_album_data():
    pass

def display_csv():
    track_data = pd.read_csv('data/fma_metadata/raw_albums.csv')
    print(track_data.columns)
    # print(track_data[('artist_name')])
    # print(len(set(track_data[('genre_handle', 'Avant-Garde')].apply(process_text))) == len(set(track_data[('genre_handle', 'Avant-Garde')].apply(process_text))))
    # print(track_data[[('track', 'tags'), ('artist', 'tags'), ('album', 'tags')]].apply(set).apply(len))
    print(track_data.head())	



if __name__ == "__main__":
    store_data()
    print("Data stored successfully!")

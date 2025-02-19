import pandas as pd
from utils.text_processing import process_text
from index.data_cleaning import create_genre_dict

# the use of 'pp_' is just to differentiate that data frame as being the preprocessed version of the original, only needed for making the inverted index

"""This module has two purposes:
1. To create the inverted index we need to preprocess all of the documents in our collection to use create tokens to use as keys. This means that for the 9 different document types 
(corresponding to the combinations of a track, album or artist with a name, list of genres or list of tags) we need to preprocess the words in the document.
2. For the BM25 ranking algorithm we also need to keep track of the length of eveyr document and the average length of a document. Since this length is measure after preprocessing,
we simply keep track of this by making a data frame containing the relevant figures for all track ids, aritst ids and album ids. 
"""

# Part 1 - Preprocess the data frames
def process_data(entire_dfs):
    """This function is simply a compostion of the preprocessing functions to make it easier to import and run in another module.
    This function expects a tuple of 4 cleaned data frames and is written to be executed after clean_and_make_data from data_cleaning.py and to take the return values of this function.
    It also gets the document lengths for each document type and returns these as a data frame"""
    track_data, album_data, artist_data, genres_data = entire_dfs
    genres_dict = genres_df_to_dict(genres_data)
    pp_track_data = process_track_data(track_data, genres_dict)
    pp_album_data = process_album_data(album_data, genres_dict)
    pp_artist_data = process_artist_data(artist_data, genres_dict)
    doclengths_track_data = get_doc_lengths(pp_track_data)
    doclengths_album_data = get_doc_lengths(pp_album_data)
    doclengths_artist_data = get_doc_lengths(pp_artist_data)
    return pp_track_data, pp_album_data, pp_artist_data, doclengths_track_data, doclengths_album_data, doclengths_artist_data

def genres_df_to_dict(genres_df):
    """This function takes in the genres df and returns a dictionary that maps the genre id to the preprocessed genre name.
    The return value of this funciton is the mapping used in the process_track_data, process_album_data and process_artist_data functions."""
    genres_dict =  genres_df[('title')].apply(process_text).to_dict()

    # this line is simply to add another key value pair so that when we unpack the dictionary that maps genre ids to frequencies and convert it to one that maps genre names to frequencies, the total key is preserved
    genres_dict['total'] = 'total'
    return genres_dict

def process_track_data(track_data, token_genres_dict):
    """This function takes in the large tracks df and creates a copy with just the columns that contain the track name/title, the genres associated with the track and the tags associated with the track.
    Following the idea of using a dictionary to hold genres and their frequencies, this function maps the list of genres for tracks to a dictionary. We keep track of the importance of a genre to a track using the total
    value of genres. We will later use these to rank the relevance of items to a paritcular query. A new column is made for this dict, in the filtered copy of tracks df using the create_genre_dict function.
    Since genres in this dictinoary are actually referred ot using their genre id rather than the word itself, this function also takes in the token_genres_dict dictionary that maps each genre id to the preprocessed genre name.
    Then the the other two columns containg the tags and the track titles are preprocessed.
    """
    # process track titles
    pp_track_data = track_data[[('track', 'title'), ('track', 'genres'), ('track', 'tags')]].copy(deep = True)

    # flatten multi-index columns - since the preprocessed track data df will only contain track info
    pp_track_data.columns = ['_'.join(col) for col in pp_track_data.columns]

    # this line could also be done with the original data frame instead, so may change to there at some stage
    # is essentially just putting the list of genres for a track in a dict with the genre as a key and the value being the frequency of the genres ( will jsut be 1 for all) and the number of genres has key 'total'
    pp_track_data[('track_genres')] = pp_track_data[('track_genres')].apply(lambda x : create_genre_dict(x, threshold = 0.0))
    
    # converting the integer representation of genres to token representation
    pp_track_data[('track_genres')] = pp_track_data['track_genres'].apply(lambda track_genres_list: {token_genres_dict[genre]: count for genre, count in track_genres_list.items()})

    # preprocess the other two columns
    pp_track_data[('track_title')] = pp_track_data[('track_title')].apply(process_text)
    pp_track_data[('track_tags')] = pp_track_data[('track_tags')].apply(process_text)

    # to maintain consistency with later steps we have to rename the columns in the preprocessed df
    # the inverted index uses the term name for a track's title, so to simplify matters later (namely when we are ranking results) we rename the column
    pp_track_data = pp_track_data.rename(columns={'track_title': 'track_name'})

    return pp_track_data

def process_album_data(album_data, token_genres_dict):
    """This function is similar to process_track_data, it takes in the albums df and the mapping of genre ids to genre names, and returns a df with entries containg preprocessed documents associated with each album."""

    # process album titles
    pp_album_data = album_data[[('album_title'), ('album_genres'),('tags')]].copy(deep=True)
    pp_album_data = pp_album_data.rename(columns={'tags': 'album_tags'})
    
    # convert the integer representation of genres to token representation, each albums genre(s) were in a dict, now that dict has different keys
    pp_album_data[('album_genres')] = pp_album_data[('album_genres')].apply(lambda album_genres_dict: {token_genres_dict[genre]: count for genre, count in album_genres_dict.items()})   
    
    # preprocess the other two columns
    pp_album_data[('album_title')] = pp_album_data[('album_title')].apply(process_text)
    pp_album_data[('album_tags')] = pp_album_data[('album_tags')].apply(process_text)


    # to maintain consistency we chaneg the word title to name in the album data too
    pp_album_data = pp_album_data.rename(columns={'album_title': 'album_name'})

    return pp_album_data


def process_artist_data(artist_data, token_genres_dict):
    """This function is similar to process_track_data and process_album_data, it takes in the artists df and the mapping of genre ids to genre names, and returns a df with entries containing preprocessed documents associated with each artist."""

    # process artist names
    pp_artist_data = artist_data[[('artist_name'), ('artist_genres'), ('tags')]].copy()
    pp_artist_data = pp_artist_data.rename(columns={'tags': 'artist_tags'})

    # convert the integer representation of genres to token representation
    pp_artist_data[('artist_genres')] = pp_artist_data[('artist_genres')].apply(lambda artist_genres_dict: {token_genres_dict[genre]: count for genre, count in artist_genres_dict.items()})

    # preprocess the other two columns
    pp_artist_data[('artist_name')] = pp_artist_data[('artist_name')].apply(process_text)
    pp_artist_data[('artist_tags')] = pp_artist_data[('artist_tags')].apply(process_text)

    return pp_artist_data


def get_doc_lengths(pp_data):
    """This function takes in a preprocessed data frame and gets the length of each entry in the data frame, since the entries correpsond to documents.
    It also calculates the average length of a document for each document type (the average over each column)."""
    pp_data_copy = pp_data.copy()
    pp_data_copy.iloc[:,0] = pp_data_copy.iloc[:,0].apply(lambda x: len(x.split()))
    pp_data_copy.iloc[:,1] = pp_data_copy.iloc[:,1].apply(lambda x: x.get('total', 0))
    pp_data_copy.iloc[:,2] = pp_data_copy.iloc[:,2].apply(lambda x: len(x.split()))

    # get the average length of a document for each document type
    avg_lengths = pp_data_copy.mean()
    pp_data_copy.loc['avg'] = avg_lengths
    return pp_data_copy

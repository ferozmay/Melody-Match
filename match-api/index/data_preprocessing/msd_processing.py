import pandas as pd
from utils.text_processing import process_text


def process_msd_data(entire_dfs):
    """This function is simply a compostion of the preprocessing functions to make it easier to import and run in another module.
    This function expects a tuple of 4 cleaned data frames and is written to be executed after clean_and_make_data from data_cleaning.py and to take the return values of this function.
    It also gets the document lengths for each document type and returns these as a data frame"""
    track_data, album_data, artist_data = entire_dfs
    pp_track_data = process_track_data(track_data)
    pp_album_data = process_album_data(album_data)
    pp_artist_data = process_artist_data(artist_data)
    doclengths_track_data = get_doc_lengths(pp_track_data)
    doclengths_album_data = get_doc_lengths(pp_album_data)
    doclengths_artist_data = get_doc_lengths(pp_artist_data)
    return pp_track_data, pp_album_data, pp_artist_data, doclengths_track_data, doclengths_album_data, doclengths_artist_data


def process_track_data(track_data):
    # process track titles
    pp_track_data = track_data[[
        ('track', 'title'), ('track', 'genres'), ('track', 'tags')]].copy(deep=True)

    # flatten multi-index columns - since the preprocessed track data df will only contain track info
    pp_track_data.columns = ['_'.join(col) for col in pp_track_data.columns]

    # this line could also be done with the original data frame instead, so may change to there at some stage
    # is essentially just putting the list of genres for a track in a dict with the genre as a key and the value being the frequency of the genres ( will jsut be 1 for all) and the number of genres has key 'total'
    # pp_track_data[('track_genres')] = pp_track_data[('track_genres')].apply(lambda x : create_genre_dict(x, threshold = 0.0))

    # # converting the integer representation of genres to token representation
    # pp_track_data[('track_genres')] = pp_track_data['track_genres'].apply(lambda track_genres_list: {token_genres_dict[genre]: count for genre, count in track_genres_list.items()})

    # preprocess the other two columns
    pp_track_data[('track_title')] = pp_track_data[(
        'track_title')].apply(process_text)
    # pp_track_data[('track_tags')] = pp_track_data[(
    #     'track_tags')].apply(process_text)

    # to maintain consistency with later steps we have to rename the columns in the preprocessed df
    # the inverted index uses the term name for a track's title, so to simplify matters later (namely when we are ranking results) we rename the column
    pp_track_data = pp_track_data.rename(columns={'track_title': 'track_name'})

    return pp_track_data


def process_album_data(album_data):
    """This function is similar to process_track_data, it takes in the albums df and the mapping of genre ids to genre names, and returns a df with entries containg preprocessed documents associated with each album."""

    # process album titles
    pp_album_data = album_data[[
        ('album_title'), ('tags')]].copy(deep=True)
    pp_album_data = pp_album_data.rename(columns={'tags': 'album_tags'})

    # convert the integer representation of genres to token representation, each albums genre(s) were in a dict, now that dict has different keys
    # pp_album_data[('album_genres')] = pp_album_data[('album_genres')].apply(lambda album_genres_dict: {
    #     token_genres_dict[genre]: count for genre, count in album_genres_dict.items()})

    # preprocess the other two columns
    pp_album_data[('album_title')] = pp_album_data[(
        'album_title')].apply(process_text)
    # pp_album_data[('album_tags')] = pp_album_data[(
    #     'album_tags')].apply(process_text)

    # to maintain consistency we chaneg the word title to name in the album data too
    pp_album_data = pp_album_data.rename(columns={'album_title': 'album_name'})

    return pp_album_data


def process_artist_data(artist_data):
    """This function is similar to process_track_data and process_album_data, it takes in the artists df and the mapping of genre ids to genre names, and returns a df with entries containing preprocessed documents associated with each artist."""

    # process artist names
    pp_artist_data = artist_data[[
        ('artist_name')]].copy()
    pp_artist_data = pp_artist_data.rename(columns={'tags': 'artist_tags'})

    # convert the integer representation of genres to token representation
    # pp_artist_data[('artist_genres')] = pp_artist_data[('artist_genres')].apply(lambda artist_genres_dict: {
    #     token_genres_dict[genre]: count for genre, count in artist_genres_dict.items()})

    # preprocess the other two columns
    pp_artist_data[('artist_name')] = pp_artist_data[(
        'artist_name')].apply(process_text)
    # pp_artist_data[('artist_tags')] = pp_artist_data[(
    #     'artist_tags')].apply(process_text)

    return pp_artist_data


def get_doc_lengths(pp_data):
    """This function takes in a preprocessed data frame and gets the length of each entry in the data frame, since the entries correpsond to documents.
    It also calculates the average length of a document for each document type (the average over each column)."""
    pp_data_copy = pp_data.copy()
    pp_data_copy.iloc[:, 0] = pp_data_copy.iloc[:, 0].apply(
        lambda x: len(x.split()))
    pp_data_copy.iloc[:, 1] = pp_data_copy.iloc[:, 1].apply(
        lambda x: x.get('total', 0))
    pp_data_copy.iloc[:, 2] = pp_data_copy.iloc[:, 2].apply(
        lambda x: len(x.split()))

    # get the average length of a document for each document type
    avg_lengths = pp_data_copy.mean()
    pp_data_copy.loc['avg'] = avg_lengths
    return pp_data_copy

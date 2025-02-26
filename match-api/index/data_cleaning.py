import numpy as np, pandas as pd, ast

"""This is a module for cleaning the FMA data. Essentially, it loads the data from fma_metadata folder into data frames. It also adds some columns that would be useful for the data frames
and fixes any issues for columns that the enry is not usable. In essence it is preparing the data we have gotten from the FMA, so that we can make an inverted index with it and display data on the front end."""


def clean_and_make_data():
    """This function is simply a composition of the main functions in this module, to make it easier to import and run the functions of this module."""
    track_data = clean_track_data()
    genres_data = clean_genres_data()
    album_data = make_album_data(track_data)
    artist_data = make_artist_data(track_data)
    return track_data, album_data, artist_data, genres_data


def clean_track_data():
    """This function loads the tracks.csv and raw_tracks.csv files into data frames. The index of the tracks df is a track id and columns correspond to different pieces of info assocaited 
    with that track. The tracks df has the majority of information, so we extract additional columns from the raw_tracks df and merge these with the tracks df. The columns of the tracks df 
    have two levels, or are of mulit-index format. The is to access a column we need to specify whether we are looking for a track, artist or album and then to specify what we are looking 
    for e.g. ('track', 'title'). The merged df has this same format. We then drop tracks with no titles, fix the image urls and make the list of genres for a track usable. The final df is returned."""
    
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
    """This function loads the genres.csv and raw_genres.csv files into data frames. Both dfs have similar information, but the raw_genres df has colours for each genre which we may find useful.
    So we merge the two dfs and return the merged df."""
    
    genres_data = pd.read_csv('data/fma_metadata/genres.csv', index_col=0)
    
    # add genre colors in case we want at some stage
    raw_genres = pd.read_csv('data/fma_metadata/raw_genres.csv', index_col=0)
    raw_genres = raw_genres[[("genre_color")]]
    
    genres_data = genres_data.merge(raw_genres, left_index=True, right_index=True, how="left")

    return genres_data


def make_album_data(track_data):
    """
    Loads raw_albums.csv as df.
    Takes in tracks_df from the clean_track_data()
    The album image url is fixed.
    
    Add information to albums_df from tracks_df.
    In the tracks_df, each track_id (that is on an album) with an album, and with a list of genres. 
    
    Goal: album_df should have a list of track_ids and a list of genres for each album.
    
    We achieve this by grouping a copy of the 
    1. Group track_df by album_id and gather the track_ids for each album.
    2. Group track_df by album_id and gather the genres for each album.
    3. Merge the two grouped dataframes.
    4. Merge the merged dataframe with the albums_df.
    5. Create a dictionary for each album key
    
    When we do this grouping we aggregate the track ids (the indices of the tracks df) and the genre ids assocaited with each album id.
    We then flatten the index of these grouped dfs, merge them and then merge them with the albums df. 
    When we aggregate the genres over all tracks, we ensure that we don't use a set, so that we can keep track of the frequency that a genre occurs on the album (ie the number of tracks on the album classified as that genre).
    We then create a dictionary for each album. This dictionary uses as keys genre ids and as a value the corresponding frequency that genre occured in the total count of genres of tracks. We also keep track of the number of genres
    ie the document length, since we will use this for ranking. For example if every song on an album with 10 tracks is classified as only hip hop then the dictionary would be {hip-hop_id: 10, 'total': 10}. 
    But if half the songs were tagged as hip hop and half as jazz OR if all the songs were tagged as hip hop and jazz, the dictionary would be either {hip-hop_id: 5, jazz_id: 5, 'total': 10} or {hip-hop_id: 10, jazz_id: 10, 'total': 20}. 
    When ranking the importance of certain terms for an album's genre document, keeping track of both the frequency AND the total will be important, so an album isn't favoured when ranking merelybecause it labels songs with more genres
    
    The last subtle point is that we only consider cases where a genre makes up at least 30% of the overall count. This way each album is classified as at most 3 genres. While this threshold is arbitrary it seems reasonable
    and prevents us from wasting time labelling an entire album as a specific genre when only one song on it is of that genre. This should help make searching more efficient but we can change if we like.
    Finally, the index of the albums df is then reset to the album id and the df is returned."""
    
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
    """This function loads the raw_artists.csv file into a df. Like the make_album_data function above this function also takes the tracks df as input from the clean_track_data function.
    The function aims to associate with each artist a list of tracks by that artist, a list of albums by that artist and a list of genres that represet that artist's music.
    It is very similar to the make_album_data function, the tracks df is grouped by artist id, and the album ids, track ids and genres per track are aggregated. The grouped dfs are merged 
    with the artists df. Lastly the artist is classified by the same function as before, creating a dictionary of genres. The only additional step is that the artist image url is fixed at the end."""

    artist_data = pd.read_csv('data/fma_metadata/raw_artists.csv')


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
    
    # fix image urls
    artist_data[("artist_image_file")] = artist_data.index.map(lambda x: fix_artist_image_url(artist_data, x))
    return artist_data


def fix_album_cover_url(data_df, track_or_album_id, album=False):
    """This function fixes album covers that are associated with either a track or an album by changing the link to a working link (although the link is not always working which will need to be checked for).
    If there is not a link to change then the placeholde image is returned. This should be changed slightly so that links that produce a 404 error are swapped for the placeholder."""
    if not album:
        track_info = data_df.loc[track_or_album_id]
        album_cover_path = track_info[("track", "track_image_file")]
    else:
        album_info = data_df.loc[track_or_album_id]
        album_cover_path = album_info[("album_image_file")]

    # placeholder = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"
    placeholder = None

    
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

def fix_artist_image_url(data_df, artist_id):
    """This function fixes the artist image url, by the saem method as fix_album_cover_url. It returns a placeholder image if the artist hasn't provided an image."""
    artist_info =  data_df.loc[artist_id]
    artist_image_path = artist_info[("artist_image_file")]

    placeholder = None
    # 'https://vevmo.com/sites/default/files/upload/woman-question-mark_0.jpg'

    if isinstance(artist_image_path, float) and np.isnan(artist_image_path):
        return placeholder

    if 'artists' in artist_image_path:
        actual_url = artist_image_path.replace("file/images/artists/", "image/?file=images%2Fartists%2F")
        actual_url = actual_url + "&width=290&height=290&type=artist"
    
    else:
        return placeholder
    return actual_url


def create_genre_dict(genre_list, threshold=0.3):
    """This function creates a dictionary from a list of lists of genre ids whereby a key,value pair is a genre id and the frequency that the genre occured over all the lists if the lists were flattened. 
    For eg if the list is  [[12, 35, 17], [35], [19, 35, 12]] then the dictionary will be {35: 3 , 12; 2 , 17: 1. 19 : 1, 'total': 7}. For more details on why this is useful see the make_album_data function."""
    if not isinstance(genre_list, list):
        return {}
    if not genre_list:
        return {}
    

    genre_dict = {genre: genre_list.count(genre) for genre in set(genre_list) if genre_list.count(genre)/len(genre_list) >= threshold}
    genre_dict['total'] = len(genre_list)
    
    
    return genre_dict

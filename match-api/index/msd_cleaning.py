import pandas as pd
import numpy as np


def clean_and_make_msd_data():
    df = pd.read_csv('data/msd_metadata/msd.csv')
    track_data = create_track_data_multiindex(df)
    album_data = create_album_data(df)
    artist_data = create_artist_data(df)
    return track_data, album_data, artist_data


def create_track_data_multiindex(df):
    """
    Convert a single-index DataFrame (with columns like 'artist_name', 'track_id', etc.)
    into a multi-index DataFrame with groups such as 'track', 'artist', and 'album'.
    """
    # Define a mapping from the original column names to (group, attribute) tuples.
    mapping = {
        'year': ('track', 'year'),
        'idx_artist_mbtags': ('artist', 'mbtags'),
        'track_7digitalid': ('track', '7digitalid'),
        'title': ('track', 'title'),
        'song_id': ('track', 'song_id'),
        'song_hotttnesss': ('track', 'hotttnesss'),
        'release_7digitalid': ('album', 'id'),
        'release': ('album', 'title'),
        'idx_similar_artists': ('artist', 'similar_artists'),
        'idx_artist_terms': ('artist', 'terms'),
        'artist_playmeid': ('artist', 'playmeid'),
        'artist_name': ('artist', 'name'),
        'artist_mbid': ('artist', 'mbid'),
        'artist_longitude': ('artist', 'longitude'),
        'artist_location': ('artist', 'location'),
        'artist_latitude': ('artist', 'latitude'),
        'artist_id': ('artist', 'id'),
        'artist_hotttnesss': ('artist', 'hotttnesss'),
        'artist_familiarity': ('artist', 'familiarity'),
        'artist_7digitalid': ('artist', '7digitalid'),
        'analyzer_version': ('track', 'analyzer_version'),
        'track_id': ('track', 'id'),
        'time_signature_confidence': ('track', 'time_signature_confidence'),
        'time_signature': ('track', 'time_signature'),
        'tempo': ('track', 'tempo'),
        'start_of_fade_out': ('track', 'start_of_fade_out'),
        'mode_confidence': ('track', 'mode_confidence'),
        'mode': ('track', 'mode'),
        'loudness': ('track', 'loudness'),
        'key_confidence': ('track', 'key_confidence'),
        'key': ('track', 'key'),
        'idx_tatums_start': ('track', 'tatums_start'),
        'idx_tatums_confidence': ('track', 'tatums_confidence'),
        'idx_segments_timbre': ('track', 'segments_timbre'),
        'idx_segments_start': ('track', 'segments_start'),
        'idx_segments_pitches': ('track', 'segments_pitches'),
        'idx_segments_loudness_start': ('track', 'segments_loudness_start'),
        'idx_segments_loudness_max_time': ('track', 'segments_loudness_max_time'),
        'idx_segments_loudness_max': ('track', 'segments_loudness_max'),
        'idx_segments_confidence': ('track', 'segments_confidence'),
        'idx_sections_start': ('track', 'sections_start'),
        'idx_sections_confidence': ('track', 'sections_confidence'),
        'idx_beats_start': ('track', 'beats_start'),
        'idx_beats_confidence': ('track', 'beats_confidence'),
        'idx_bars_start': ('track', 'bars_start'),
        'idx_bars_confidence': ('track', 'bars_confidence'),
        'energy': ('track', 'energy'),
        'end_of_fade_in': ('track', 'end_of_fade_in'),
        'duration': ('track', 'duration'),
        'danceability': ('track', 'danceability'),
        'audio_md5': ('track', 'audio_md5'),
        'analysis_sample_rate': ('track', 'analysis_sample_rate'),
        'genres': ('track', 'genres'),
        'similars': ('track', 'similars'),
        'tags': ('track', 'tags'),
        'album_url': ('track', 'track_image_file')
    }

    df.set_index('track_id', inplace =True)
    
    # Create new column names using the mapping; if a column is not found in the mapping,
    # default it to the 'track' group.
    new_columns = []
    for col in df.columns:
        new_columns.append(mapping.get(col, ('track', col)))

    df.columns = pd.MultiIndex.from_tuples(new_columns)

        # Apply the function to the (track, genres) column of your dataframe.
    df[('track', 'genres')] = df[('track', 'genres')].apply(process_genres)

    
    df_genres = pd.read_csv("data/fma_metadata/genres.csv")

    genre_mapping = dict(
        zip(df_genres['title'].str.strip(), df_genres['genre_id']))

    def map_genres_to_ids(genre_str):
        if pd.isna(genre_str):
            return []
        # Split on commas and strip whitespace
        genres = [g.strip() for g in genre_str.split(",")]
        # Map each genre to its corresponding genre_id (ignoring ones not in the mapping)
        return [genre_mapping[g] for g in genres if g in genre_mapping]

    # Update the (track, genres) column with lists of genre_ids
    df[("track", "genres")] = df[("track", "genres")].apply(map_genres_to_ids)

    # Convert (track, tags) column to list of top 10 tags
    def process_tags(tags_str):
        if pd.isna(tags_str):
            return tags_str
        tags_dict = eval(tags_str)
        sorted_tags = sorted(
            tags_dict.items(), key=lambda item: int(item[1]), reverse=True)
        top_10_tags = [tag for tag, _ in sorted_tags[:10]]
        return top_10_tags

    df[('track', 'tags')] = df[('track', 'tags')].apply(process_tags)

    # Create the track_url column
    base_url = "https://open.spotify.com/search/"
    df[("track", "track_url")] = base_url + df[("track", "title")]

    return df


def create_album_data(df):
    # Make a copy of the DataFrame
    df_flat = df.copy()
    # Flatten the multiindex columns (e.g. ('album', 'title') becomes 'album_title')
    df_flat.columns = ['_'.join(col).strip() for col in df_flat.columns.values]

    # Add the track_id (which is the original index) as a column
    df_flat['track_id'] = df_flat.index
    
    # Group by the album identifier column (now 'album_release_7digitalid')
    album_df = df_flat.groupby('album_id').agg(
        album_title=('album_title', 'first'),
        album_image_file=('track_track_image_file', 'first'),
        album_tracks=('track_id', 'count'),       # Count the number of tracks
        track_ids=('track_id', list),             # List the track_ids
        artist_name = ('artist_name', 'first'),
        album_date_released = ('track_year', 'first')
    )

    # After your groupby operation, reset the index to make 'album_release_7digitalid' a column
    album_df = album_df.reset_index()
    album_df.set_index('album_id', inplace=True)
    album_df.index.name = 'album_id'

    base_url = "https://open.spotify.com/search/"
    album_df['album_url'] = base_url + album_df['album_title']

    return album_df


def create_artist_data(df):

    # Make a copy of the DataFrame
    df_flat = df.copy()

    # Flatten the multiindex columns (e.g. ('artist', 'name') becomes 'artist_name')
    df_flat.columns = ['_'.join(col).strip() for col in df_flat.columns.values]

    # Add the track_id (which is the original index) as a column
    df_flat['track_id'] = df_flat.index

    # Group by the artist identifier column (now 'artist_id')
    artist_df = df_flat.groupby('artist_id').agg(
        artist_7digitalid=('artist_7digitalid', 'first'),
        artist_familiarity=('artist_familiarity', 'first'),
        artist_hotttnesss=('artist_hotttnesss', 'first'),
        artist_latitude=('artist_latitude', 'first'),
        artist_location=('artist_location', 'first'),
        artist_longitude=('artist_longitude', 'first'),
        artist_mbid=('artist_mbid', 'first'),
        artist_mbtags=('artist_mbtags', 'first'),
        artist_name=('artist_name', 'first'),
        artist_playmeid=('artist_playmeid', 'first'),
        artist_similar_artists=('artist_similar_artists', 'first'),
        artist_terms=('artist_terms', 'first'),
        artist_tracks=('track_id', 'count'),       # Count of tracks per artist
        # List of track_ids for the artist
        track_ids=('track_id', list),
        album_ids=('album_id', lambda x: list(
            x.unique()))  # Unique album IDs
    )

    # After the groupby operation, reset the index to make 'artist_id' a column
    artist_df = artist_df.reset_index()

    

    # Optionally, set the DataFrame's index name (here we simply keep the default integer index)
    artist_df.set_index('artist_id', inplace=True)

    base_url = "https://open.spotify.com/search/"
    artist_df['artist_url'] = base_url + artist_df['artist_name']

    return artist_df


def process_genres(text):
    # Handle NaNs: if text is NaN, simply return it
    if pd.isna(text):
        return text

    result = []
    # Split on comma and iterate over each genre
    for item in text.split(","):
        genre = item.strip()
        # If genre is "Pop_Rock", add "Pop" and "Rock"
        if genre == "Pop_Rock":
            for subgenre in ["Pop", "Rock"]:
                if subgenre not in result:
                    result.append(subgenre)
        # Rename "Avant_Garde" to "Avant-Garde"
        elif genre == "Avant_Garde":
            subgenre = "Avant-Garde"
            if subgenre not in result:
                result.append(subgenre)
        else:
            if genre not in result:
                result.append(genre)
    return ", ".join(result)



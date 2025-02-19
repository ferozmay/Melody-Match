

"""This module contains the functions that create the inverted index. It relies on the data having been processed in data_processing.py which in turn relies on the data having been cleaned in data_cleaning.py.

The inverted index is a nested dictionary that has the following structure:
{token: {'Track': {'Name': {'doc_freq': 0, 'doc_ids': {}}, 'Genres': {'doc_freq': 0, 'doc_ids': {}}, 'Tags': {'doc_freq': 0, 'doc_ids': []}},
        {'Album': {'Name': {'doc_freq': 0, 'doc_ids': {}}, 'Genres': {'doc_freq': 0, 'doc_ids': {}}, 'Tags': {'doc_freq': 0, 'doc_ids': []}},
        {'Artist': {'Name': {'doc_freq': 0, 'doc_ids': {}}, 'Genres': {'doc_freq': 0, 'doc_ids': {}}, 'Tags': {'doc_freq': 0, 'doc_ids': []}}}
}
This structure means that if a query contains the word 'happy' we can easily find all the tracks, albums and artists with: happy in their name, happy as a genre (there will be none) and happy as a tag.
The doc_ids dictionary/list for the tracks dictionary will conatin track ids, the doc_ids for the album dict will contain and album ids and for the artists dict it will contain aritst ids.
This allows us to easily access the data associated with a track, album or artist in the tracks df, albums df or artist df.
"""

# Create the inverted index
def initialize_inverted_index_entry():
    """This function is used to initialize the inverted index. The inverted index is a nested dictionary where the value for an outer key if of the structure returned in this function.
    Justification for this structure: we are considering there to be nine different document types, and so we need to keep track of the frequency of a token across all documents of EACH of these types.
    The doc_ids is a dictionary for the Name and Genre becaus eof the following: if a token appears in a name, tehn we also count the position of the token in the name. While we don't care about the positon
    when searching, keeping track of the position also allows us to keep track of the term frequency within the name, (in case the term appears multiple times). 
    For genre we kept track of the frequency of each genre in the document. We viewed each instance that a song on an album or artist was classified as a certain genre as counting towards the frequency that genre occured
    in the document. Similarly with a track - although in this case the genre of course can only ever have a frequency of one. Later we will use the total number of genres in a document for ranking.
    For tags at the moment we don't have scores correpsonding to a tag so we just store them in a list. But once we get scores we can store them in a dict and use them for ranking. Eg if a song has a socre of 1.0 for danceability 
    this can be stored next to a danceable tag, and the song can be weighted higher than a song with a score of 0.5 for danceability. """
    return {
        'Track': {
            'Name': {'doc_freq': 0, 'doc_ids': {}},
            'Genres': {'doc_freq': 0, 'doc_ids': {}},
            'Tags': {'doc_freq': 0, 'doc_ids': []}
        },
        'Album': {
            'Name': {'doc_freq': 0, 'doc_ids': {}},
            'Genres': {'doc_freq': 0, 'doc_ids': {}},
            'Tags': {'doc_freq': 0, 'doc_ids': []}
        },
        'Artist': {
            'Name': {'doc_freq': 0, 'doc_ids': {}},
            'Genres': {'doc_freq': 0, 'doc_ids': {}},
            'Tags': {'doc_freq': 0, 'doc_ids': []}
        }
        }


def create_inverted_index(entire_pp_dfs):
    """This funciton creates the inverted index. It takes in the entire set of preprocessed data frames as a tuple and returns the inverted index.
    It picks a data frame then loops over each row and each column and then adds to the inverted index, depending on the column and row combination.
    Since the different doc types (name, genre, tag) require different handling, the add_to_inverted_index function checks the inputs given."""

    pp_track_data, pp_album_data, pp_artist_data = entire_pp_dfs
    inverted_index = dict()

    for index, row in pp_track_data.iterrows():
        
        for position, term in enumerate(row['track_name'].split(), start=1):
            add_to_inverted_index(inverted_index, term, 'Track', 'Name', index, position=position)
        
        # Process track genres
        for genre, frequency in row['track_genres'].items():
            add_to_inverted_index(inverted_index, genre, 'Track', 'Genres', index, frequency=frequency)
        
        # Process track tags
        for tag in row['track_tags'].split():
            add_to_inverted_index(inverted_index, tag, 'Track', 'Tags', index)

    for index, row in pp_album_data.iterrows():
        
        for position, term in enumerate(row['album_name'].split(), start=1):
            add_to_inverted_index(inverted_index, term, 'Album', 'Name', index, position=position)
        
        # Process album genres
        for genre, frequency in row['album_genres'].items():
            add_to_inverted_index(inverted_index, genre, 'Album', 'Genres', index, frequency=frequency)
        
        # Process album tags
        for tag in row['album_tags'].split():
            add_to_inverted_index(inverted_index, tag, 'Album', 'Tags', index)
    
    for index, row in pp_artist_data.iterrows():
        
        for position, term in enumerate(row['artist_name'].split(), start=1):
            add_to_inverted_index(inverted_index, term, 'Artist', 'Name', index, position=position)
        
        # Process artist genres
        for genre, frequency in row['artist_genres'].items():
            add_to_inverted_index(inverted_index, genre, 'Artist', 'Genres', index, frequency=frequency)
        
        # Process artist tags
        for tag in row['artist_tags'].split():
            add_to_inverted_index(inverted_index, tag, 'Artist', 'Tags', index)
    return inverted_index


def add_to_inverted_index(inverted_index, term, object_type, document_type, doc_id, position=None, frequency=None):
    """This funciton is used to add to an entry of the inverted index. For each term given as input and each object type (track, album , artist) the function adds
    to the entry in the inverted index. It acts differently depending on the document type (name, genre, tag). Why it does what it does is discuessed in the initialize_inverted_index_entry function"""
    
    # handle the different object types: a track, an album and artist
    # handle the different document types: a name (document is the entire name for the object), a genre (document is the list of genres for the object), a tag (document is the list of tags for the object)
    # initilaise, or add to index
    if term not in inverted_index:
        inverted_index[term] = initialize_inverted_index_entry()
    
    if doc_id not in inverted_index[term][object_type][document_type]['doc_ids']:
        inverted_index[term][object_type][document_type]['doc_freq'] += 1
        if document_type == 'Name':
            inverted_index[term][object_type][document_type]['doc_ids'][doc_id] = []
        if document_type == 'Genres':
            inverted_index[term][object_type][document_type]['doc_ids'][doc_id] = frequency
        if document_type == 'Tags':
            inverted_index[term][object_type][document_type]['doc_ids'].append(doc_id)
    if document_type == 'Name':
        inverted_index[term][object_type][document_type]['doc_ids'][doc_id].append(position)

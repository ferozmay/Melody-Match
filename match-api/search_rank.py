from utils.text_processing import process_text
import math
import itertools

# set some global variables
N = None
k, b = (None, None)
hyperparams = None

import re
import itertools

def parse_boolean_query(query):
    # regex looks for either:
    # 1. A word that's uppercase: AND, OR, NOT
    # 2. A word that's lowercase or mixed-case (which we assume to be a term).
    tokens = re.findall(r'\b(?:AND|OR|NOT|\w+)\b', query)
    
    is_boolean = False
    # filter tokens to ensure only uppercase AND, OR, and NOT are considered operators
    parsed_tokens = []
    for token in tokens:
        if token in ['AND', 'OR', 'NOT']:
            # make sure the operator is uppercase
            parsed_tokens.append(token)
            is_boolean = True
        else:
            # treat everything else as a search term
            parsed_tokens.append(token.lower())
    
    return parsed_tokens, is_boolean

def search_rank(query: str, index, doclengths_track_data, doclengths_album_data, doclengths_artist_data, collection_size: int, hyperparams_dict: dict):

    global N, k, b, hyperparams
    N = collection_size
    hyperparams = hyperparams_dict
    k = hyperparams['k']
    b = hyperparams['b']

    # parse the boolean query
    query_tokens, is_boolean = parse_boolean_query(query)

    # initialise dictionaries
    track_title_scores = dict()
    album_title_scores = dict()
    artist_title_scores = dict()
    track_genres_scores = dict()
    album_genres_scores = dict()
    artist_genres_scores = dict()
    track_tags_scores = dict()
    album_tags_scores = dict()
    artist_tags_scores = dict()

    object_types = ['Track', 'Album', 'Artist']
    document_types = ['Name', 'Genres', 'Tags']
    pairs = list(itertools.product(object_types, document_types))
    
    # process each token with Boolean logic
    current_set = None  # holds thhe set of document IDs after applying Boolean logic
    current_operator = "AND"  # default operator (for the first term)

    for token in query_tokens:
        print(f"Processing token: {token}")
        if token in ['AND', 'OR', 'NOT']:
            current_operator = token
        else:
            # if it's a term, get the scores for this term
            term = token.lower()

            # initialise the term_scores for this token
            term_scores = {
                'Track': dict(),
                'Album': dict(),
                'Artist': dict()
            }
            
            # process each document type (Track, Album, Artist)
            for pair in pairs:
                object_type, document_type = pair
                
                if term in index:
                    # if its a boolean query we only care about the titles
                    if not is_boolean:
                        # rank the term for each document type (track, album, artist)
                        if document_type == 'Name':
                            if object_type == 'Track':
                                track_title_scores = rank_titles(term, index, object_type, doclengths_track_data, track_title_scores)
                                term_scores['Track'].update(track_title_scores)
                            if object_type == 'Album':
                                album_title_scores = rank_titles(term, index, object_type, doclengths_album_data, album_title_scores)
                                term_scores['Album'].update(album_title_scores)
                            if object_type == 'Artist':
                                artist_title_scores = rank_titles(term, index, object_type, doclengths_artist_data, artist_title_scores)
                                term_scores['Artist'].update(artist_title_scores)
   
                    if document_type == 'Genres':
                        if object_type == 'Track':
                            track_genres_scores = rank_genres(term, index, object_type, doclengths_track_data, track_genres_scores)
                            term_scores['Track'].update(track_genres_scores)
                        if object_type == 'Album':
                            album_genres_scores = rank_genres(term, index, object_type, doclengths_album_data, album_genres_scores)
                            term_scores['Album'].update(album_genres_scores)
                        if object_type == 'Artist':
                            artist_genres_scores = rank_genres(term, index, object_type, doclengths_artist_data, artist_genres_scores)
                            term_scores['Artist'].update(artist_genres_scores)
                    
                    elif document_type == 'Tags':
                        if object_type == 'Track':
                            track_tags_scores = rank_tags(term, index, object_type, doclengths_track_data, track_tags_scores)
                            term_scores['Track'].update(track_tags_scores)
                        if object_type == 'Album':
                            album_tags_scores = rank_tags(term, index, object_type, doclengths_album_data, album_tags_scores)
                            term_scores['Album'].update(album_tags_scores)
                        if object_type == 'Artist':
                            artist_tags_scores = rank_tags(term, index, object_type, doclengths_artist_data, artist_tags_scores)
                            term_scores['Artist'].update(artist_tags_scores)
            
        # applyboolean logic to term scores
        if current_set is None:
            # initialise the set with the first term's results
            current_set = set(term_scores['Track'].keys()) | set(term_scores['Album'].keys()) | set(term_scores['Artist'].keys())
            print(f"Initial current_set: {current_set}")
        else:
            if current_operator == 'AND':
                current_set &= set(term_scores['Track'].keys()) | set(term_scores['Album'].keys()) | set(term_scores['Artist'].keys())
                print(f"After AND, current_set: {current_set}")
            elif current_operator == 'OR':
                current_set |= set(term_scores['Track'].keys()) | set(term_scores['Album'].keys()) | set(term_scores['Artist'].keys())
                print(f"After OR, current_set: {current_set}")
            elif current_operator == 'NOT':
                current_set -= set(term_scores['Track'].keys()) | set(term_scores['Album'].keys()) | set(term_scores['Artist'].keys())
                print(f"After NOT, current_set: {current_set}")


    track_keys = set(track_title_scores.keys()) | set(track_genres_scores.keys()) | set(track_tags_scores.keys())
    print(f"Track keys: {track_keys}")

    album_keys = set(album_title_scores.keys()) | set(album_genres_scores.keys()) | set(album_tags_scores.keys())
    print(f"Album keys: {album_keys}")

    artist_keys = set(artist_title_scores.keys()) | set(artist_genres_scores.keys()) | set(artist_tags_scores.keys())
    print(f"Artist keys: {artist_keys}")

    # after processing all tokens and applying Boolean logic, get final scores
    track_scores = {doc_id: (track_title_scores.get(doc_id, 0), track_genres_scores.get(doc_id, 0), track_tags_scores.get(doc_id, 0)) for doc_id in current_set}
    album_scores = {doc_id: (album_title_scores.get(doc_id, 0), album_genres_scores.get(doc_id, 0), album_tags_scores.get(doc_id, 0)) for doc_id in current_set}
    artist_scores = {doc_id: (artist_title_scores.get(doc_id, 0), artist_genres_scores.get(doc_id, 0), artist_tags_scores.get(doc_id, 0)) for doc_id in current_set}

    return track_scores, album_scores, artist_scores

def rank_titles(term, index, object_type, doclengths_df, scores:dict):
    """This function calculate the BM25 score for a term in the index, for a specific object type (track, artist, album) and the 'Name' document type.
    It takes in the doclengths_df and then gets the average length for the document type, and the length of each document that contains the term.
    It then adds the BM25 score to the entry on the socres dicitonary that corresponds to the document id. It returns the scores dictionary, to be used in another iteration."""
    
    # we form the name of the column we are interested in, in the doclengths df - eg track_name
    doclengths_column = ('_'.join([object_type.lower(), 'name']))

    # we get the average doc length for the 'Name' documents of the object 
    doclengths_avg = doclengths_df[doclengths_column]['avg']
    
    # get the document frequency of the term
    df = index[term][object_type]['Name']['doc_freq']

    # get the doc ids of the documents that contain the term 
    title_doc_ids = set(index[term][object_type]['Name']['doc_ids'].keys())

    # for each doc id, calculate the retrieval score
    for doc_id in title_doc_ids:
        if doc_id not in scores.keys():
            scores[doc_id] = 0
        # get the length of the document
        doc_length = doclengths_df[doclengths_column][doc_id]
        # get the term frequency of the term in the document
        tf = len(index[term][object_type]['Name']['doc_ids'][doc_id]) 
        # skip if tf or df are zero to prevent math errors
        if tf == 0 or df == 0:
            continue
        
        # add the bm25 score for the term, document pair
        scores[doc_id] += calculate_bm25(tf, df, doc_length, doclengths_avg)
    return scores

def rank_genres(term , index, object_type, doclengths_df,  scores:dict):
    """This function calculates the BM25 score like in rank_titles, the only difference is that the genres dictionaries are handled differently."""

    doclengths_column = ('_'.join([object_type.lower(), 'genres']))
    doclengths_avg = doclengths_df[doclengths_column]['avg']

    df = index[term][object_type]['Genres']['doc_freq']
    genres_dict = index[term][object_type]['Genres']['doc_ids']
    
    for doc_id in genres_dict:
        if doc_id not in scores.keys():
            scores[doc_id] = 0
        
        # get the length of the document
        doc_length = doclengths_df[doclengths_column][doc_id]
        # we get the term frequency of the genre in the document
        tf = genres_dict[doc_id]
        # skip if tf or df are zero to prevent math errors
        if tf == 0 or df == 0:
            continue

        # add the tfidf weight
        scores[doc_id] += calculate_bm25(tf, df, doc_length, doclengths_avg)
    return scores

def rank_tags(term , index, object_type, doclengths_df, scores:dict):
    """This function is liek the two before it just it deals with tags. The only difference is that for the moment we set tf = 1 since the tags for a track, artist or album
    as provided by the FMA shouldn't repeat themselves. However there is room to improve our ranking system by setting thsi differently.
    If we know a track has been given a 1.0 score for danceablility, then it should appear higher than a track that has been given a 0.5 score for the query danceable.
    By giving weights to tags we can replace the tf part of the ranking - since the tf is important for factoring how important a term is a to a document."""
   
    doclengths_column = ('_'.join([object_type.lower(), 'tags']))
    doclengths_avg = doclengths_df[doclengths_column]['avg']

    df = index[term][object_type]['Tags']['doc_freq']
    tags_doc_ids = index[term][object_type]['Tags']['doc_ids']
    
    for doc_id in tags_doc_ids:
        if doc_id not in scores.keys():
            scores[doc_id] = 0

        # for the time being we will leave the tf score as one but this could be used to change the weighting when a track, artist or album is more of a certain tag than others
        tf = 1
        # skip if tf or df are zero to prevent math errors
        if tf == 0 or df == 0:
            continue

        # add the tfidf weight
        scores[doc_id] += (1 + math.log10(tf)) * math.log10(N / df)
    return scores

def calculate_bm25(tf, df, doclength, doclengths_avg):
    """This funciton performs the caluclation for the BM25 score for a single term in a query, with a document.
    It uses the formula:
    BM25(t,d) = IDF(t) * (tf(t,d) * (k + 1)) / (tf(t,d) + k * (1 - b + b * (doclength / avgdoclength)))
    where:
    IDF(t) = log((N - df(t) + 0.5) / (df(t) + 0.5))
    tf(t,d) = frequency of term t in document d
    df(t) = number of docs containing term t
    N = total number of docs in collection
    k, b = hyperparameters
    doclength = length of the document
    avgdoclength = average length of documents

    There are different versions of the BM25 formula, you can read page 250 of IR in practice book for more details.
    There is sometimes another paramter k_2 but the purpouse of this hyperparameter is to regulate the number of times a term appears in a query - something we haven't considered
    in our calculations since it is likely unhelpful for our use case.

    The k parameter is used to regulate the term frequency, k = 0 means only the presence or absence of a term is acknoledged, k = 1.2 dampens the effect of the term frequency like a logarithm.
    The b parameter is used to regulate the effect of the document length compared to the other document lengths, b = 0 means the doc length is not acknowledged, b = 1 means the BM25 score
    is fully normalised by the document length.
    """
    
    global N, k, b
    idf = math.log((N - df + 0.5) / (df + 0.5))
    denom = tf + k * (1 - b + b * (doclength / doclengths_avg))
    return idf * (tf * (k + 1)) / denom
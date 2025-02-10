from utils.text_processing import process_text
import math
import itertools

def search_rank(query: str, index, collection_size: int):

        query_tokens = process_text(query).split()

        track_title_scores = {}
        album_title_scores = {}
        artist_title_scores = {}
        track_genres_scores = {}
        album_genres_scores = {}
        artist_genres_scores = {}
        track_tags_scores = {}
        album_tags_scores = {}
        artist_tags_scores = {}

        object_types = ['Track', 'Album', 'Artist']
        document_types = ['Name', 'Genres', 'Tags']
        pairs = list(itertools.product(object_types, document_types))
      
        for pair in pairs:
            for term in query_tokens:
                if term in index:
                    if pair[1] == 'Name':
                        if pair[0] == 'Track':
                            track_title_scores = rank_titles(term, index, pair[0], collection_size, track_title_scores)
                        if pair[0] == 'Album':
                            album_title_scores = rank_titles(term, index, pair[0],collection_size, album_title_scores)
                        if pair[0] == 'Artist':
                            artist_title_scores = rank_titles(term, index, pair[0], collection_size, artist_title_scores)
                    if pair[1] == 'Genres':
                        if pair[0] == 'Track':
                            track_genres_scores = rank_genres(term, index, pair[0], collection_size, track_genres_scores)
                        if pair[0] == 'Album':
                            album_genres_scores = rank_genres(term, index, pair[0], collection_size, album_genres_scores)
                        if pair[0] == 'Artist':
                            artist_genres_scores = rank_genres(term, index, pair[0], collection_size, artist_genres_scores)
                    if pair[1] == 'Tags':
                        if pair[0] == 'Track':
                            track_tags_scores = rank_tags(term, index, pair[0], collection_size, track_tags_scores)
                        if pair[0] == 'Album':
                            album_tags_scores = rank_tags(term, index, pair[0], collection_size, album_tags_scores)
                        if pair[0] == 'Artist':
                            artist_tags_scores = rank_tags(term, index, pair[0], collection_size, artist_tags_scores)
                else:
                    continue        
        #track dictionary
        track_keys = set(track_title_scores.keys()) | set(track_genres_scores.keys()) | set(track_tags_scores.keys())
        track_scores = {doc_id: {'Name' : track_title_scores.get(doc_id, 0), 'Genres' : track_genres_scores.get(doc_id, 0), 'Tags' : track_tags_scores.get(doc_id, 0)} for doc_id in track_keys}
        #album dictionary
        album_keys = set(album_title_scores.keys()) | set(album_genres_scores.keys()) | set(album_tags_scores.keys())
        album_scores = {doc_id: (album_title_scores.get(doc_id, 0),  album_genres_scores.get(doc_id, 0),  album_tags_scores.get(doc_id, 0)) for doc_id in album_keys}
        # artist dictionay
        artist_keys = set(artist_title_scores.keys()) | set(artist_genres_scores.keys()) | set(artist_tags_scores.keys())
        artist_scores = {doc_id: (artist_title_scores.get(doc_id, 0), artist_genres_scores.get(doc_id, 0),  artist_tags_scores.get(doc_id, 0)) for doc_id in artist_keys}
        return track_scores, album_scores, artist_scores

def rank_titles(term, index, object_type, collection_size, scores):
    # ranking with tfidf for time being
    # for each query term, calculate the weight of the term in each document
    # weight_t,d = (1 + log _10 tf (t,d) * log _10 (N/df(t))
    # tf(t,d) = frequency of term t in document d
    # df(t) = number of documents containing term t
    # N = total number of documents in the collection
    # collection size for all document types is the same since we are assuming all tracks have an album, artist
    # and then all of those three things have genres and tags
    title_doc_ids = []
    df = index[term][object_type]['Name']['doc_freq'] 
    title_doc_ids.append(set(index[term][object_type]['Name']['doc_ids'].keys()))
    for doc_id in title_doc_ids:
        if doc_id not in scores:
            scores[doc_id] = 0
        tf = len(index[term][object_type]['Name']['doc_ids'][doc_id]) 
        # skip if tf or df are zero to prevent math errors
        if tf == 0 or df == 0:
            continue

        # add the tfidf weight
        scores[doc_id] += (1 + math.log10(tf)) * math.log10(collection_size / df)
    return scores

def rank_genres(term , index, object_type, collection_size, scores):
    genres_dict = index[term][object_type]['Genres']['doc_ids']
    df = index[term][object_type]['Genres']['doc_freq']
    for doc_id in genres_dict:
        if doc_id not in scores:
            scores[doc_id] = 0
        # here I am making our own version of a tf(t,d)
        # for every object type eg track, artist, album, a genre can only appear once
        # however some objects may be categorised as only that genre 
        # in which case we have kept track of this by giving that genre a score of one in the genres dictionary
        # other genres might be less prevalent for a track, album or artist and for example the object may have a socre of 0.5 for this
        # since the point of the tf score is to give documents where a term appears more often we give preference to objects that have been classified as fewer different genres
        # since the values are all between 0 and 1 there is no need to dampen
        
        tf = genres_dict[doc_id]
        # skip if tf or df are zero to prevent math errors
        if tf == 0 or df == 0:
            continue

        # add the tfidf weight
        scores[doc_id] += (1 + tf) * math.log10(collection_size / df)
    return scores

def rank_tags(term , index, object_type, collection_size, scores):
    tags_doc_ids = index[term][object_type]['Tags']['doc_ids']
    df = index[term][object_type]['Tags']['doc_freq']
    for doc_id in tags_doc_ids:
        if doc_id not in scores:
            scores[doc_id] = 0

        # for the time being we will leave the tf score as one but this could be used to change the weighting when a track, artist or album is more of a certain tag than others
        tf = 1
        # skip if tf or df are zero to prevent math errors
        if tf == 0 or df == 0:
            continue

        # add the tfidf weight
        scores[doc_id] += (1 + math.log10(tf)) * math.log10(collection_size / df)
    return scores

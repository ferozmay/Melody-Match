import ast
from index.store_load import load_data
from index.boolean_search import infix_to_postfix, evaluate_postfix, boolean_tokenize
import json
import pandas as pd
from utils.text_processing import process_text
from utils.lyrics_expansion import expand_query
from utils import parse_id
import math
import itertools

from utils.text_processing import process_text
from utils.lyrics_expansion import expand_query


similar_songs_dict = {}

with open("data/stored_data/fma_sim_dict.json", "r") as f:
    similar_songs_dict = json.load(f)


def is_fma(track_id):
    _id = parse_id(track_id)
    if isinstance(_id, int):
        return True
    return False

def handle_nan(value):
    # if the value is NaN replace it with None (for valid JSON)
    if isinstance(value, float) and (value != value): 
        return None
    return value


class Index:
    def load_index(self):
        self.track_data, self.album_data, self.artist_data, self.doclengths_track_data, self.doclengths_album_data, self.doclengths_artist_data, self.index, self.lyrics_index, self.doclengths_lyrics, self.precomputed_similar_words_lyrics, self.lyrics_5000_stems, self.ft, self.lyrics_vectors, self.lyrics_word_map = load_data()
    
    def load_parameters(self, hyperparams: dict, ranking_algs: dict):
        self.hyperparams = hyperparams
        self.N = len(self.track_data)
        self.ranking_algs = ranking_algs

    def initialise_scores_dict(self):
        self.track_title_scores = dict()
        self.album_title_scores = dict()
        self.artist_title_scores = dict()
        self.track_genres_scores = dict()
        self.album_genres_scores = dict()
        self.artist_genres_scores = dict()
        self.track_tags_scores = dict()
        self.album_tags_scores = dict()
        self.artist_tags_scores = dict()
    
    def initialise_lyrics_scores_dict(self):
        self.track_lyrics_scores = dict()

    def boolean_filter(self, query: str, collection: dict, access_function):
        """
        Takes in a query, converts to postfix
        and evaluates the postfix expression on the index
        Returns the set of doc_ids that satisfy the query
        """
        tokens = boolean_tokenize(query)
        postfix = infix_to_postfix(tokens)
        return evaluate_postfix(postfix, collection, access_function)
        
    def search_rank(self, query: str):
        """This function takes in a query, the index, teh various document lengths dfs and the collection size and hyperparameters for the search.
        It then makes the collection size and hyperparameters arguments global variables so they can be used in the BM25 calculation later.
        It then intialises nine dictionaries for the different document combinations, and goes through each combination and for each term in a query it
        it upadates the nine dicitonaries giving a BM25 score for each document. The nine dictionaries are converted to three, so they can be presented by the front-end.
        Each entry of the final dicitonaries is of the form {doc_id: (name_score, genres_score, tags_score)}.
        This means that the tracks_scores dictionary for example will contain ids for all the tracks relevant to the search/ query and associated with each id will be a 
        score for the relevance of the track name, the track's genres and the track's tags to the query. """

        
        self.initialise_scores_dict()

        object_types = ['Artist', 'Album', 'Track']
        document_types = ['Name', 'Genres', 'Tags']
        pairs = list(itertools.product(object_types, document_types))

        # drop caps'ed AND, OR, NOT from query
        is_boolean = any([word in query for word in ['AND', 'OR', 'NOT']])
        unbooled_query = query.replace('AND', '').replace('OR', '').replace('NOT', '')
        query_tokens = process_text(unbooled_query).split()


        for pair in pairs:
            for term in query_tokens:
                # .boolean_filter(query):
                if term in self.index:
                    if pair[1] == 'Name':
                        if pair[0] == 'Artist':
                            self.rank_artist_titles(term, pair[0]) # include flag for artist's album titles scores and artist's track titles scores
                        if pair[0] == 'Album':
                            self.rank_album_titles(term, pair[0]) # include flag for album's artist titles scores
                        if pair[0] == 'Track':
                            self.rank_track_titles(term, pair[0]) # include flag for track's album titles scores and track's artist titles scores
                        
                    if pair[1] == 'Genres':
                        if pair[0] == 'Track':
                            self.rank_genres(term, pair[0],  self.doclengths_track_data,  self.track_genres_scores)
                        if pair[0] == 'Album':
                            self.rank_genres(term, pair[0],  self.doclengths_album_data, self.album_genres_scores)
                        if pair[0] == 'Artist':
                            self.rank_genres(term, pair[0],  self.doclengths_artist_data,  self.artist_genres_scores)
                    if pair[1] == 'Tags':
                        if pair[0] == 'Track':
                            self.rank_tags(term, pair[0], self.doclengths_track_data,  self.track_tags_scores)
                        if pair[0] == 'Album':
                            self.rank_tags(term, pair[0], self.doclengths_album_data,  self.album_tags_scores)
                        if pair[0] == 'Artist':
                            self.rank_tags(term, pair[0], self.doclengths_artist_data,  self.artist_tags_scores)
                else:
                    continue
        #track dictionary
        track_keys = set(self.track_title_scores.keys()) | set(self.track_genres_scores.keys()) | set(self.track_tags_scores.keys()) 
        track_scores = {doc_id: (self.track_title_scores.get(doc_id, 0), self.track_genres_scores.get(doc_id, 0), self.track_tags_scores.get(doc_id, 0)) for doc_id in track_keys}
        #album dictionary
        album_keys = set(self.album_title_scores.keys()) | set(self.album_genres_scores.keys()) | set(self.album_tags_scores.keys())
        album_scores = {doc_id: (self.album_title_scores.get(doc_id, 0),  self.album_genres_scores.get(doc_id, 0),  self.album_tags_scores.get(doc_id, 0)) for doc_id in album_keys}
        # artist dictionary
        artist_keys = set(self.artist_title_scores.keys()) | set(self.artist_genres_scores.keys()) | set(self.artist_tags_scores.keys())
        artist_scores = {doc_id: (self.artist_title_scores.get(doc_id, 0), self.artist_genres_scores.get(doc_id, 0),  self.artist_tags_scores.get(doc_id, 0)) for doc_id in artist_keys}
        
        # apply boolean filter to the track scores
        if is_boolean:
            # tracks
            filtered_track_ids = self.boolean_filter(
                query,
                self.index,
                lambda term, index: set(index.get(process_text(term), {}).get('Track', {}).get('Name', {}).get('doc_ids', {}).keys())
            )
            track_scores = {doc_id: track_scores.get(doc_id) for doc_id in filtered_track_ids if doc_id in track_scores}
            # albums
            filtered_album_ids = self.boolean_filter(
                query,
                self.index,
                lambda term, index: set(index.get(process_text(term), {}).get('Album', {}).get('Name', {}).get('doc_ids', {}).keys())
            )
            album_scores = {doc_id: album_scores.get(doc_id) for doc_id in filtered_album_ids if doc_id in album_scores}
            # artists
            filtered_artist_ids = self.boolean_filter(
                query,
                self.index,
                lambda term, index: set(index.get(process_text(term), {}).get('Artist', {}).get('Name', {}).get('doc_ids', {}).keys())
            )
            artist_scores = {doc_id: artist_scores.get(doc_id) for doc_id in filtered_artist_ids if doc_id in artist_scores}
        
        
        return track_scores, album_scores, artist_scores

    def rank_track_titles(self, term , object_type): # include parameter to allow search for albums, aritsts for tracks and artists for albums
        """This function calculate the BM25 score for a term in the index, for a specific object type (track, artist, album) and the 'Name' document type.
        It takes in the doclengths_df and then gets the average length for the document type, and the length of each document that contains the term.
        It then adds the BM25 score to the entry on the socres dicitonary that corresponds to the document id. It returns the scores dictionary, to be used in another iteration."""
        ranking_alg = self.ranking_algs['names']

        # we form the name of the column we are interested in, in the doclengths df - eg track_name
        doclengths_column = ('_'.join([object_type.lower(), 'name']))

        # we get the average doc length for the 'Name' documents of the object 
        doclengths_avg = self.doclengths_track_data[doclengths_column]['avg']
        
        # get the document frequency of the term
        df = self.index[term][object_type]['Name']['doc_freq']

        # get the doc ids of the documents that contain the term 
        title_doc_ids = set(self.index[term][object_type]['Name']['doc_ids'].keys())

        # for each doc id, calculate the retrieval score
        for doc_id in title_doc_ids:
            if doc_id not in self.track_title_scores.keys():
                self.track_title_scores[doc_id] = 0
            # get the length of the document
            doc_length = self.doclengths_track_data[doclengths_column][doc_id]
            # get the term frequency of the term in the document
            tf = len(self.index[term][object_type]['Name']['doc_ids'][doc_id]) 
            # skip if tf or df are zero to prevent math errors
            if tf == 0 or df == 0:
                continue
            
            # add the bm25 score for the term, document pair
            if ranking_alg == 'BM25':
                self.track_title_scores[doc_id] += self.calculate_bm25(tf, df, doc_length, doclengths_avg)
            elif ranking_alg == 'TFIDF':
                self.track_title_scores[doc_id] += self.calculate_tfidf(tf, df)


    def rank_album_titles(self, term, object_type): # include parameter to allow search for albums, aritsts for tracks and artists for albums
        """This function calculate the BM25 score for a term in the index, for a specific object type (track, artist, album) and the 'Name' document type.
        It takes in the doclengths_df and then gets the average length for the document type, and the length of each document that contains the term.
        It then adds the BM25 score to the entry on the socres dicitonary that corresponds to the document id. It returns the scores dictionary, to be used in another iteration."""
        gamma = self.hyperparams['gamma']
        ranking_alg = self.ranking_algs['names']
        
        # we form the name of the column we are interested in, in the doclengths df - eg track_name
        doclengths_column = ('_'.join([object_type.lower(), 'name']))

        # we get the average doc length for the 'Name' documents of the object 
        doclengths_avg = self.doclengths_album_data[doclengths_column]['avg']
        
        # get the document frequency of the term
        df = self.index[term][object_type]['Name']['doc_freq']

        # get the doc ids of the documents that contain the term 
        title_doc_ids = set(self.index[term][object_type]['Name']['doc_ids'].keys())

        # for each doc id, calculate the retrieval score
        for doc_id in title_doc_ids:
            if doc_id not in self.album_title_scores.keys():
                self.album_title_scores[doc_id] = 0
            
            # get the length of the document
            doc_length = self.doclengths_album_data[doclengths_column][doc_id]
            # get the term frequency of the term in the document
            tf = len(self.index[term][object_type]['Name']['doc_ids'][doc_id]) 
            # skip if tf or df are zero to prevent math errors
            if tf == 0 or df == 0:
                continue
            

            # add the bm25 score for the term, document pair
            if ranking_alg == 'BM25':
                album_score = self.calculate_bm25(tf, df, doc_length, doclengths_avg)
                self.album_title_scores[doc_id] += album_score
            elif ranking_alg == 'TFIDF':
                album_score = self.calculate_tfidf(tf, df)
                self.album_title_scores[doc_id] += album_score

            # get the track ids
            trackid_list = self.album_data.loc[doc_id]['track_ids']
            # add a score proportinal to the aritst scores for all the trakc ids that an artist has
            for track_id in trackid_list:
                if track_id not in self.track_title_scores.keys():
                    self.track_title_scores[track_id] = album_score * gamma
                else:
                    self.track_title_scores[track_id] += album_score * gamma
        

    def rank_artist_titles(self, term, object_type): # include parameter to allow search for albums, aritsts for tracks and artists for albums
        """This function calculate the BM25 score for a term in the index, for a specific object type (track, artist, album) and the 'Name' document type.
        It takes in the doclengths_df and then gets the average length for the document type, and the length of each document that contains the term.
        It then adds the BM25 score to the entry on the socres dicitonary that corresponds to the document id. It returns the scores dictionary, to be used in another iteration."""
        alpha = self.hyperparams['alpha']
        beta = self.hyperparams['beta']
        ranking_alg = self.ranking_algs['names']
        # we form the name of the column we are interested in, in the doclengths df - eg track_name
        doclengths_column = ('_'.join([object_type.lower(), 'name']))

        # we get the average doc length for the 'Name' documents of the object 
        doclengths_avg = self.doclengths_artist_data[doclengths_column]['avg']
        
        # get the document frequency of the term
        df = self.index[term][object_type]['Name']['doc_freq']

        # get the doc ids of the documents that contain the term 
        title_doc_ids = set(self.index[term][object_type]['Name']['doc_ids'].keys())

        # for each doc id, calculate the retrieval score
        for doc_id in title_doc_ids:
            if doc_id not in self.artist_title_scores.keys():
                self.artist_title_scores[doc_id] = 0
            # get the length of the document
            doc_length = self.doclengths_artist_data[doclengths_column][doc_id]
            # get the term frequency of the term in the document
            tf = len(self.index[term][object_type]['Name']['doc_ids'][doc_id]) 
            # skip if tf or df are zero to prevent math errors
            if tf == 0 or df == 0:
                continue
            
            if ranking_alg == 'BM25':
                # add the bm25 score for the term, document pair
                artist_score = self.calculate_bm25(tf, df, doc_length, doclengths_avg)
                self.artist_title_scores[doc_id] += artist_score
            elif ranking_alg == 'TFIDF':
                artist_score = self.calculate_tfidf(tf, df)
                self.artist_title_scores[doc_id] += artist_score

            # get the track ids
            trackid_list = self.artist_data.loc[doc_id]['track_ids']

            for track_id in trackid_list:
                if track_id not in self.track_title_scores.keys():
                    self.track_title_scores[track_id] = artist_score * alpha
                else:
                    self.track_title_scores[track_id] += artist_score * alpha
            
            # get the album ids
            albumid_list = self.artist_data.loc[doc_id]['album_ids']

            for album_id in albumid_list:
                if album_id not in self.album_title_scores.keys():
                    self.album_title_scores[album_id] = artist_score * beta
                else:
                    self.album_title_scores[album_id] += artist_score * beta


    def rank_genres(self, term , object_type, doclengths_df, scores:dict):
        """This function calculates the BM25 score like in rank_titles, the only difference is that the genres dictionaries are handled differently."""
        ranking_alg = self.ranking_algs['genres']

        doclengths_column = ('_'.join([object_type.lower(), 'genres']))
        doclengths_avg = doclengths_df[doclengths_column]['avg']

        df = self.index[term][object_type]['Genres']['doc_freq']
        genres_dict = self.index[term][object_type]['Genres']['doc_ids']
        
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
            
            if ranking_alg == 'BM25':
                # add the bm25 score for the term, document pair
                scores[doc_id] += self.calculate_bm25(tf, df, doc_length, doclengths_avg)
            elif ranking_alg == 'TFIDF':
                scores[doc_id] += self.calculate_tfidf(tf,df)


    def rank_tags(self, term , object_type, doclengths_df, scores:dict):
        """This function is liek the two before it just it deals with tags. The only difference is that for the moment we set tf = 1 since the tags for a track, artist or album
        as provided by the FMA shouldn't repeat themselves. However there is room to improve our ranking system by setting thsi differently.
        If we know a track has been given a 1.0 score for danceablility, then it should appear higher than a track that has been given a 0.5 score for the query danceable.
        By giving weights to tags we can replace the tf part of the ranking - since the tf is important for factoring how important a term is a to a document."""
       
        doclengths_column = ('_'.join([object_type.lower(), 'tags']))
        doclengths_avg = doclengths_df[doclengths_column]['avg']

        df = self.index[term][object_type]['Tags']['doc_freq']
        tags_doc_ids = self.index[term][object_type]['Tags']['doc_ids']
        
        for doc_id in tags_doc_ids:
            if doc_id not in scores.keys():
                scores[doc_id] = 0

            # for the time being we will leave the tf score as one but this could be used to change the weighting when a track, artist or album is more of a certain tag than others
            tf = 1
            # skip if tf or df are zero to prevent math errors
            if tf == 0 or df == 0:
                continue

            # add the tfidf weight
            scores[doc_id] += self.calculate_tfidf(tf, df)


    def search_rank_lyrics(self, query:str, expand:bool):
        if expand:
            query_tokens = expand_query(query, self.ft, self.precomputed_similar_words_lyrics, self.lyrics_vectors, self.lyrics_word_map, self.lyrics_5000_stems)
        else:
            query_tokens = process_text(query).split()
        # print("Extended query:", query_tokens)
        self.initialise_lyrics_scores_dict()
        for term in query_tokens:
            if term in self.lyrics_index:
                self.rank_lyrics(term)
            else:
                continue
        return self.track_lyrics_scores


    
    def rank_lyrics(self, term):
        """This function calculates the score for a song based on the bag of words representation of a song by its lyrics"""
        ranking_alg = self.ranking_algs['lyrics']
        msd_doc_ids = self.lyrics_index[term].keys()
        df = len(msd_doc_ids)

        doclengths_df = self.doclengths_lyrics
        doclengths_column = 'doc_length'

        # TODO - Convert that to self.doclengths_lyrics_avg (so it doesn't get computed every time)
        doclengths_avg = doclengths_df[doclengths_column].mean()

        for doc_id in msd_doc_ids: 
            if doc_id not in self.track_lyrics_scores.keys():
                    self.track_lyrics_scores[doc_id] = 0
            tf = self.lyrics_index[term][doc_id]
            
            doclength = self.doclengths_lyrics[doclengths_column][doc_id]

            if tf == 0 or df == 0:
                continue
            if ranking_alg == 'BM25':
               self.track_lyrics_scores[doc_id] += self.calculate_bm25(tf, df, doclength, doclengths_avg)
            elif ranking_alg == 'TFIDF':
                self.track_lyrics_scores[doc_id] += self.calculate_tfidf(tf, df)
            


    def calculate_tfidf(self, tf, df):
       """This function calculates the tfidf score for a term in a document. It uses the formula:
          tfidf(t,d) = tf(t,d) * log(N / df(t))
          where:
          tf(t,d) = frequency of term t in document d
          df(t) = number of docs containing term t
          N = total number of docs in collection
       """
       return (1 + math.log10(tf)) * math.log10(self.N / df)




    def calculate_bm25(self, tf, df, doclength, doclengths_avg):
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
        N = self.N
        k = self.hyperparams['k']
        b = self.hyperparams['b']
        idf = math.log((N - df + 0.5) / (df + 0.5))
        denom = tf + k * (1 - b + b * (doclength / doclengths_avg))
        return idf * (tf * (k + 1)) / denom

        
    def track_ids_to_data(self, track_ids, include_similar=False, only_essential=False):
        track_data = self.track_data
        data = []
        single = False

        # First ensure we have scalar values
        if isinstance(track_ids, pd.Series):
            track_ids = track_ids.tolist()  # Convert Series to list
            
        if not isinstance(track_ids, list):
            track_ids = [track_ids]
            single = True

        for track_id in track_ids:
            if track_id not in track_data.index:
                continue

            track_info = track_data.loc[track_id]
            similar_songs = []
            if include_similar:
                if is_fma(track_id):
                    similar_songs = json.loads(self.track_ids_to_data(self.get_similar_songs(track_id)))
                else:
                    items = ast.literal_eval(self.track_data.loc[track_id, ("track", "similars")])
                    similar_songs = list(items.keys())
                    similar_songs = json.loads(self.track_ids_to_data(similar_songs))
                    # similar_songs = self.track_data.loc[track_id][["track", "similars"]]

            genres = track_info[("track", "genres_string")]

            if only_essential:
                data.append({
                    "id": track_id,
                    "title": handle_nan(track_info[("track", "title")]),
                    "artist": handle_nan(track_info[("artist", "name")]),
                    "album": handle_nan(track_info[("album", "title")]),
                    "runtime": handle_nan(track_info[("track", "duration")]),
                })
            else:
                data.append({
                    "id": track_id,
                    "title": handle_nan(track_info[("track", "title")]),
                    "artist": handle_nan(track_info[("artist", "name")]),
                    "runtime": handle_nan(track_info[("track", "duration")]),
                    "albumCover": handle_nan(track_info[("track", "track_image_file")]),
                    "link": handle_nan(track_info[("track", "track_url")]),
                    "artistLink": handle_nan(track_info.get(("track", "artist_url"))),
                    "album": handle_nan(track_info[("album", "title")]),
                    "albumLink": handle_nan(track_info.get(("track", "album_url"))),
                    "genres": genres,
                    "albumId": handle_nan(track_info[("album", "id")]),
                    "artistId": handle_nan(track_info[("artist", "id")]),
                    "similarSongs": similar_songs
                })
        
        if single:
            return json.dumps(data[0], default=str)
        return json.dumps(data, default=str, indent=4)

    def album_ids_to_data(self, album_ids, include_tracks=False):
        album_data = self.album_data
        data = []
        single = False
        if not isinstance(album_ids, list):
            album_ids = [album_ids]
            single = True

        for album_id in album_ids:
            if album_id not in album_data.index:
                continue
            album_info = album_data.loc[album_id]
            album_tracks = []
            if include_tracks:
                album_tracks = json.loads(self.track_ids_to_data(album_info[("track_ids")]))
            
            # # turn album gernres dictionary (id: frequency) into a list of genre ids
            # album_genres = album_info[("album_genres")]
            # album_genres = [genre_id for genre_id, _ in album_genres.items()]
            # # turn genre ids into genre names
            # album_info["album_genres"] = self.genre_ids_to_words(album_genres)
            
            data.append({
                "id": album_id,
                "title": handle_nan(album_info[("album_title")]),
                "artist": handle_nan(album_info[("artist_name")]),
                # "artistId": handle_nan(album_info[("artist_id")]),
                "releaseDate": handle_nan(album_info[("album_date_released")]),
                "albumCover": handle_nan(album_info[("album_image_file")]),
                "noOfTracks": handle_nan(album_info[("album_tracks")]),
                "link": handle_nan(album_info[("album_url")]),
                "genres:": album_info["album_genres_string"],
                "songs": album_tracks,
            })

        if single:
            return json.dumps(data[0], default=str)
        return json.dumps(data, default=str)

    def artist_ids_to_data(self, artist_ids, include_tracks=False, include_albums=False):
        artist_data = self.artist_data
        data = []
        single = False
        if not isinstance(artist_ids, list):
            single = True
            artist_ids = [artist_ids]
        for artist_id in artist_ids:
            if artist_id not in artist_data.index:
                continue
            artist_info = artist_data.loc[artist_id]
            albums = []
            songs = []
            if include_albums:
                albums = json.loads(self.album_ids_to_data(
                    artist_info[("album_ids")], include_tracks=True))
            if include_tracks:
                songs = json.loads(self.track_ids_to_data(
                    artist_info[("track_ids")]))
            data.append({
                "id": artist_id,
                "name": handle_nan(artist_info[("artist_name")]),
                "artistImage": handle_nan(artist_info[("artist_image_file")]),
                "link": handle_nan(artist_info[("artist_url")]),
                "songs": songs,
                "albums": albums,
                "bio": handle_nan(artist_info[("artist_bio")])
            })
        if single:
            return json.dumps(data[0], default=str)
        return json.dumps(data, default=str)



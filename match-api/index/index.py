import math
import numpy as np
import pandas as pd
import ast
import json
from utils.text_processing import process_text
import urllib.parse
from index.clean_store_load import load_track_data

class TrackIndex:
    def load_index(self):
        self.track_data, self.inverted_index = load_track_data()


    def get_google_search_link(song, artist, album):
        google_search = f"Free Music Archive {song} {artist} {album}"
        encoded_search = urllib.parse.quote_plus(google_search)
        return f"https://www.google.com/search?q={encoded_search}"


    def track_ids_to_data(self, track_ids):
        # Load the data
        data = []
        for track_id in track_ids:
            track_info = self.track_data.loc[track_id]
            artist_website = track_info[("artist", "website")]
            # for each of the query results, we create a hyperlink indicating what teh google search for the result would look like
            # this can replace the artist_website if we want or not - can definitely replace for those without a website
            google_search = TrackIndex.get_google_search_link(track_info[("track", "title")], track_info[("artist", "name")], track_info[("album", "title")] )
            # Check if artist_website is nan and handle it
            if isinstance(artist_website, float) and np.isnan(artist_website):
                artist_website = google_search
            data.append({
                "id": track_id,
                "title": track_info[("track", "title")],
                "artist": track_info[("artist", "name")],
                "runtime": track_info[("track", "duration")],
                "albumCover": track_info[("track", "track_image_file")],
                "link": track_info[("track","track_url")],
                "artistLink": track_info[("track", "artist_url")] # temporarily using the google search instead of the artist website 
            })

        return json.dumps(data, default=str)
    
    def simple_search(self, query: str):

        query_tokens = process_text(query).split()

        term_doc_ids = []

        if len(query_tokens) == 1:
            term = query_tokens[0]
            if term in self.inverted_index:
                term_doc_ids.append(set(self.inverted_index[term]['docs'].keys()))
                docs = self.inverted_index[term]['docs'].keys()
                return docs

        # multiple search terms
        for term in query_tokens:
            if term in self.inverted_index:
                term_doc_ids.append(set(self.inverted_index[term]['docs'].keys()))
        
        if not term_doc_ids:
            return []
                
        common_doc_ids = set.intersection(*term_doc_ids)

        results = list(common_doc_ids)
        
        return results

    def tfidf_scores(self, query: str, collection_size: int):
        # for each query term, calculate the weight of the term in each document
        # weight_t,d = (1 + log _10 tf (t,d) * log _10 (N/df(t))
        # tf(t,d) = frequency of term t in document d
        # df(t) = number of documents containing term t
        # N = total number of documents in the collection

        terms = process_text(query).split()
        term_dfs = {term: self.inverted_index[term]['doc_freq'] for term in terms}

        # for each doc, calculate the retrieval score
        # (the sum of the weights of the terms that appear in both the query and the document)

        retrieval_scores = {}
        
        # get docs to consider (any doc that contains at least one of the query terms)
        doc_ids = set()
        for term in terms:
            if term in self.inverted_index:
                doc_ids.update(self.inverted_index[term]['docs'].keys())

        # for each doc, calculate the retrieval score
        for doc_id in doc_ids:
            if doc_id not in retrieval_scores:
                retrieval_scores[doc_id] = 0
            for term in terms:
                weight = 0
                if term in self.inverted_index and doc_id in self.inverted_index[term]['docs']:
                    tf = len(self.inverted_index[term]['docs'][doc_id]) # no. of listed appearances of term in doc = freq. in doc
                    df = term_dfs[term]
                    weight = (1 + math.log10(tf)) * math.log10(collection_size / df)
                    retrieval_scores[doc_id] += weight

        return retrieval_scores
    



    
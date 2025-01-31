import math
import numpy as np
import pandas as pd
import ast
import json
from utils.text_processing import process_text
import urllib.parse
from collections import defaultdict, Counter


class TrackIndex:
    def load_index(self):
        # load the data
        self.track_data = pd.read_csv('data/fma_metadata/tracks.csv', index_col=0, header=[0, 1])

        # load raw tracks 
        self.raw_tracks = pd.read_csv('data/fma_metadata/raw_tracks.csv')

        # get only the track_id, track_url and track_image_file cols
        self.raw_tracks = self.raw_tracks[["track_id", "track_url", "track_image_file", "artist_url"]]

        self.raw_tracks.set_index("track_id", inplace=True)

        # convert raw_tracks to a multi-index format to match track_data
        self.raw_tracks.columns = pd.MultiIndex.from_tuples([("track", col) for col in self.raw_tracks.columns])

        # merge with track_data using track_id as the key
        self.track_data = self.track_data.merge(self.raw_tracks, left_index=True, right_index=True, how="left")
        
        # Drop tracks with no titles
        nan_track_titles = self.track_data[self.track_data[("track", "title")].isna()].index
        self.track_data.drop(nan_track_titles, inplace=True)

        # Process the titles
        # TODO: pickle that shit
        track_titles = self.track_data[("track", "title")].apply(process_text)
        # create the index from processed titles {title: track_id}
        self.titles_index = dict(zip(track_titles, self.track_data.index))

        # Fix album cover URLs
        self.track_data[("track", "track_image_file")] = self.track_data.index.map(self.fix_album_cover_url)

        # generate the info for each token as a tuple (token, track_id, position)
        token_instances = []
        for track_id, title in zip(self.track_data.index, track_titles):
            words = title.split()  # tokenize title into words
            for position, word in enumerate(words, start=1):
                token_instances.append((word, track_id, position))
        
        # create the inverted index
        self.inverted_index = self.create_inverted_index(token_instances)

        # save to file
        with open('inverted-index.json', 'w') as f:
            json.dump(self.inverted_index, f, indent=4)

    def create_inverted_index(self, term_sequence):
        inverted_index = defaultdict(lambda: {'doc_freq': 0, 'docs': {}})
        
        for term, track_id, position in term_sequence:
            # +1 doc_freq when we encounter the term in a new title
            if track_id not in inverted_index[term]['docs']:
                inverted_index[term]['doc_freq'] += 1

            # store the position of the term in the title
            if track_id not in inverted_index[term]['docs']:
                inverted_index[term]['docs'][track_id] = []
            inverted_index[term]['docs'][track_id].append(position)

        return inverted_index

    def search(self, query):
        query = process_text(query)
        track_ids = []
        for title in self.titles_index.keys():
            if query in title:
                track_ids.append(self.titles_index[title])
        return track_ids

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
    
    def fix_album_cover_url(self, track_id):

        track_info = self.track_data.loc[track_id]
        album_cover_path = track_info[("track", "track_image_file")]

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


    
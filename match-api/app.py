import time
app_start_time = time.time()
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from index.index_data_ranking import Index
import pickle, pandas as pd, time
import threading
from utils.ids_to_data import track_ids_to_data, album_ids_to_data, artist_ids_to_data

# init the app
app = Flask(__name__)

# Set up CORS to prevent blockage of requests from local domains
cors = CORS(
    app, 
    resources={r"/api/*": {"origins": ["http://localhost:3000", "http://192.168.0.13:3000"]}}
)

def load_index():

    global index
    index = Index()
    
    start_time = time.time()
    index.load_index()
    print("Data loaded successfully! Time taken: ", time.time() - start_time)

index_thread = threading.Thread(target=load_index)
index_thread.start()
index_thread.join()

app_end_time = time.time()
print("App loaded successfully! Time taken: ", app_end_time - app_start_time)

@app.route("/api/songs/<track_id>")
def get_song(track_id):
    return index.track_ids_to_data(parse_id(track_id), include_similar=True)

@app.route("/api/albums/<album_id>")
def get_album(album_id):
    return index.album_ids_to_data(parse_id(album_id), include_tracks=True)

@app.route("/api/artists/<artist_id>")
def get_artist(artist_id):
    return index.artist_ids_to_data(parse_id(artist_id), include_albums=True, include_tracks=True)
    
@app.route("/api/search")
def handle_request():
    query = request.args.get("query", None)
    limit = int(request.args.get("limit", 10))

    if query:
          # total number of tracks
        # the hyperparamters k,b are reported to be sensible for BM25 algorithm, but we can evaluate different settings for our use case 
        # we can also evaluate the effect of the hyperparameters alpha, beta, gamma which are used for instances where an artists songs should show in the songs section
        hyperparams = {'k':1.2, 'b':0.75, 'alpha':1, 'beta':1, 'gamma':1}

        # we give the capability to choose between BM25 and TFIDF for each of the different documents types that can do both: 
        # names (song names, artist names, album names), genres (song genres, artist genres, album genres), lyrics (song lyrics)
        ranking_algs = {'names': 'BM25', 'genres': 'BM25', 'lyrics': 'TFIDF'}
        index.load_parameters(hyperparams, ranking_algs)
        track_scores, album_scores, artist_scores = index.search_rank(query)
        lyrics_scores = index.search_rank_lyrics(query)

        # Define a helper function to sum the values of a tuple 
        def tuple_sum(t):
            total = 0
            for v in t:
                # If v is a Series (or anything that has a 'sum' attribute), use its sum
                if hasattr(v, 'sum'):
                    total += v.sum()
                else:
                    total += v
            return total

        # temporarily just ordered based on the title score
        sorted_track_scores = sorted(track_scores.items(), key=lambda item: sum(list(item[1])), reverse=True)
        sorted_album_scores = sorted(album_scores.items(), key=lambda x: tuple_sum(x[1]), reverse=True)  # Now sort album_scores using the helper function
        sorted_artist_scores = sorted(artist_scores.items(), key=lambda item: sum(list(item[1])), reverse=True)

        sorted_lyrics_scores = sorted(lyrics_scores.items(), key=lambda item: item[1], reverse=True)

        ranked_track_ids = [track_id for track_id, _ in sorted_track_scores][:limit] 
        ranked_album_ids = [album_id for album_id, _ in sorted_album_scores][:limit]
        ranked_artist_ids = [artist_id for artist_id, _ in sorted_artist_scores][:limit]

        ranked_lyric_track_ids = [track_id for track_id, _ in sorted_lyrics_scores][:limit]

        track_data = index.track_ids_to_data(ranked_track_ids)
        album_data = index.album_ids_to_data(ranked_album_ids)
        artist_data = index.artist_ids_to_data(ranked_artist_ids)
        
        lyrics_data = index.track_ids_to_data(ranked_lyric_track_ids)

        # To see some of the results and that the search is working uncomment this code
        # print("Track data results: ", '\n', track_data)
        # print("Track scores: ", '\n', sorted_track_scores)
        # print("Album data results: ", '\n', album_data)
        # print("Album scores: ", '\n', sorted_album_scores)
        # print("Artist data results: ", '\n', artist_data)
        # print("Artist scores: ", '\n', sorted_artist_scores)
        print("Lyrics data results: ", '\n', lyrics_data)
        # print("Lyrics scores: ", '\n', sorted_lyrics_scores)
        return {'songs': json.loads(track_data), 'albums' : json.loads(album_data), 'artists': json.loads(artist_data)}

    return {}



def parse_id(some_id):
    try:
        return int(some_id)
    except ValueError:
        return str(some_id)
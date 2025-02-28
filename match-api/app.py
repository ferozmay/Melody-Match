import time
app_start_time = time.time()
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from index.index_class import Index
import pickle, pandas as pd, time
import threading
from search_rank import search_rank
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
    return index.track_ids_to_data(int(track_id), include_similar=True)

@app.route("/api/albums/<album_id>")
def get_album(album_id):
    return index.album_ids_to_data(int(album_id), include_tracks=True)

@app.route("/api/artists/<artist_id>")
def get_artist(artist_id):
    return index.artist_ids_to_data(int(artist_id), include_albums=True, include_tracks=True)

@app.route("/api/search")
def handle_request():
    query = request.args.get("query", None)
    limit = int(request.args.get("limit", 10))


    if query:
        collection_size = len(index.track_data)  # total number of tracks
        # these hyperparamters are reported to be sensible for BM25 algorithm, but we can evaluate different settings for our use case 
        hyperparams = {'k':1.2, 'b':0.75}
        track_scores, album_scores, artist_scores = search_rank(query, index.index, index.doclengths_track_data, index.doclengths_album_data, index.doclengths_artist_data,  collection_size, hyperparams)
            
        # temporarily just ordered based on the title score
        sorted_track_scores = sorted(track_scores.items(), key=lambda item: sum(item[1]), reverse=True)
        sorted_album_scores = sorted(album_scores.items(), key=lambda item: sum(item[1]), reverse=True)
        sorted_artist_scores = sorted(artist_scores.items(), key=lambda item: sum(item[1]), reverse=True)
        

        ranked_track_ids = [track_id for track_id, _ in sorted_track_scores][:limit] 
        ranked_album_ids = [album_id for album_id, _ in sorted_album_scores][:limit]
        ranked_artist_ids = [artist_id for artist_id, _ in sorted_artist_scores][:limit]
        track_data = index.track_ids_to_data(ranked_track_ids)
        album_data = index.album_ids_to_data(ranked_album_ids)
        artist_data = index.artist_ids_to_data(ranked_artist_ids)
        # to see some of the results and that the search is working uncomment this code
        # print("Track data results: ", '\n', track_data)
        # print("Track scores: ", '\n', sorted_track_scores)
        # print("Album data results: ", '\n', album_data)
        # print("Album scores: ", '\n', sorted_album_scores)
        # print("Artist data results: ", '\n', artist_data)
        # print("Artist scores: ", '\n', sorted_artist_scores)
        return {'songs': json.loads(track_data), 'albums' : json.loads(album_data), 'artists': json.loads(artist_data)}

    return {}
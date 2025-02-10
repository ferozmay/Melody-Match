import time
app_start_time = time.time()
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from index.index import Index
import pickle, pandas as pd, time
import threading
from search import search_rank
from ranking import tfidf
from utils.ids_to_data import track_ids_to_data, album_ids_to_data

# init the app
app = Flask(__name__)

# Set up CORS to prevent blockage of requests from local domains
cors = CORS(
    app, 
    resources={r"/api/*": {"origins": ["http://localhost:3000", "http://10.124.114.40:5173"]}}
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

@app.route("/api/search")
def handle_request():
    query = request.args.get("query", None)
    limit = int(request.args.get("limit", 10))


    if query:
        collection_size = len(index.track_data)  # total number of tracks
        track_scores, album_scores, artist_scores = search_rank(query, index.index, collection_size)
        
        # temporarily just ordered based on the title score
        print(list(track_scores.items())[:10])
        sorted_track_scores = sorted(track_scores.items(), key=lambda item: item[0], reverse=True)
        sorted_album_scores = sorted(album_scores.items(), key=lambda item: item[0], reverse=True)
        sorted_artist_scores = sorted(artist_scores.items(), key=lambda item: item[0], reverse=True)

        ranked_track_ids = [track_id for track_id, _ in sorted_track_scores][:limit] 
        ranked_album_ids = [album_id for album_id, _ in sorted_album_scores][:limit]
        ranked_artist_ids = [artist_id for artist_id, _ in sorted_artist_scores][:limit]

        track_data = track_ids_to_data(index.track_data, ranked_track_ids)
        album_data = album_ids_to_data(index.album_data, ranked_album_ids)
        # we don't have an artist ids to data function yet

        return {'songs': json.loads(track_data), 'albums' : json.loads(album_data)}

    return []
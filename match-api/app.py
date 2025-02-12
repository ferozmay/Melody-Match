import time
app_start_time = time.time()
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from index.track_index import TrackIndex
from index.album_index import AlbumIndex
import pickle, pandas as pd, time
import threading
from search import simple_search
from ranking import tfidf
from utils.ids_to_data import track_ids_to_data, album_ids_to_data

# init the app
app = Flask(__name__)

# Set up CORS to prevent blockage of requests from local domains
cors = CORS(
    app, 
    resources={r"/api/*": {"origins": ["http://localhost:3000"]}}
)

# # load the index
# start_time = time.time()
# song_title_index = TrackIndex()
# song_title_index.load_index()
# print("Data loaded successfully! Time taken: ", time.time() - start_time)

def load_index():

    global track_index, album_index

    track_index = TrackIndex()
    album_index = AlbumIndex()
    
    start_time = time.time()

    track_index.load_track_index()
    album_index.load_album_index()
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

    track_query = True

    if query:
        # get results
        if track_query:
            track_results = simple_search(query, track_index.index)
            collection_size = len(track_index.track_data)  # total number of tracks
            tfidf_scores = tfidf(query, track_index.index, collection_size)
            
            # sort the results by tdidf score
            ranked_results = sorted(
                [(track_id, tfidf_scores.get(track_id, 0)) for track_id in track_results],  
                key=lambda x: x[1],  
                reverse=True
            )

            ranked_track_ids = [track_id for track_id, _ in ranked_results][:limit] 

            data = track_ids_to_data(track_index.track_data, ranked_track_ids)

        else:
            album_results = simple_search(query, album_index.index)
            collection_size = len(album_index.album_data)  # total number of albums
            tfidf_scores = tfidf(query, album_index.index, collection_size)
            
            # sort the results by tdidf score
            ranked_results = sorted(
                [(album_id, tfidf_scores.get(album_id, 0)) for album_id in album_results],  
                key=lambda x: x[1],  
                reverse=True
            )

            ranked_album_ids = [album_id for album_id, _ in ranked_results][:limit]

            data = album_ids_to_data(album_index.album_data, ranked_album_ids)

        return {"songs":json.loads(data)}

    return {}
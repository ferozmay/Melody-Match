import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from index.index import TrackIndex
import pickle, pandas as pd, time


# init the app
app = Flask(__name__)

# Set up CORS to prevent blockage of requests from local domains
cors = CORS(
    app, 
    resources={r"/api/*": {"origins": ["http://localhost:5173", "http://10.124.114.40:5173"]}}
)

# load the index
start_time = time.time()
song_title_index = TrackIndex()
song_title_index.load_index()
print("Data loaded successfully! Time taken: ", time.time() - start_time)


@app.route("/api/track")
def handle_request():
    query = request.args.get("query", None)
    limit = int(request.args.get("limit", 10))

    if query:
        # get results
        song_results = song_title_index.simple_bow_search(query)

        collection_size = len(song_title_index.track_data)  # total number of tracks
        
        # get tfidf scores for this query
        tfidf_scores = song_title_index.tfidf_scores(query, collection_size)

        # sort the results by tdidf score
        ranked_results = sorted(
            [(track_id, tfidf_scores.get(track_id, 0)) for track_id in song_results],  
            key=lambda x: x[1],  
            reverse=True
        )

        ranked_track_ids = [track_id for track_id, _ in ranked_results][:limit] 

        data = song_title_index.track_ids_to_data(ranked_track_ids)

        return data

    return []
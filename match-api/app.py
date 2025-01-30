import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from index.index import TrackIndex

# init the app
app = Flask(__name__)

# Set up CORS to prevent blockage of requests from local domains
cors = CORS(
    app, 
    resources={r"/api/*": {"origins": ["http://localhost:5173", "http://10.124.114.40:5173"]}}
)

# load the index
song_title_index = TrackIndex()
song_title_index.load_index()

@app.route("/api/track")
def handle_request():
    query = request.args.get("query", None)
    limit = int(request.args.get("limit", 10))

    if query:
        song_results = song_title_index.simple_bow_search(query)
        data = song_title_index.track_ids_to_data(list(song_results)[:limit])
        return data

    return []
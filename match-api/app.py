from flask import Flask, request
from index.index import TrackIndex

# init the app
app = Flask(__name__)

# load the index
song_title_index = TrackIndex()
song_title_index.load_index()

@app.route("/track")
def handle_request():
    query = request.args.get("query", None)
    limit = int(request.args.get("limit", 10))
    if query:
        song_results = song_title_index.search(query)
        return song_results[:limit]

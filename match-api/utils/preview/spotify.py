import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth


os.environ["SPOTIPY_CLIENT_ID"] = '1b529e30c45c436ab981c95bfa4c57f4'
os.environ["SPOTIPY_CLIENT_SECRET"] = '55be3ac01f6f49b09b3098e0054b3bbd'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:3000/callback'


scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


print(sp.track('spotify:track:4mn2kNTqiGLwaUR8JdhJ1l'))
# https://open.spotify.com/track/?si=73e3a4b794384c7b
# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
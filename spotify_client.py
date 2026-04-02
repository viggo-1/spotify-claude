import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "user-top-read",
    "user-read-recently-played",
    "user-library-read",
    "user-read-private",
]


def get_client() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=" ".join(SCOPES)))

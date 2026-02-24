import sys
import configparser
from pathlib import Path
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

#config
CWD = str(Path(__file__).parent)
CONFIG = configparser.ConfigParser()
CONFIG.read(CWD + "/config.ini")

#USER = CONFIG["spotify"]["user"]
CLIENT_ID = CONFIG["spotify"]["client_id"]
CLIENT_SECRET = CONFIG["spotify"]["client_secret"]
REDIRECT_URI = CONFIG["spotify"]["redirect_uri"]
SCOPE = CONFIG["spotify"]["scope"]
CACHE_PATH = CWD + "/.cache"


#auth
spotify_client = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=CACHE_PATH
        )
    )
album_cache = {}

#helpers
def extract_playlist_id(url: str) -> str:
    if "playlist/" not in url:
        raise ValueError("Invalid Spotify playlist URL")
    return url.split("playlist/")[1].split("?")[0]

def parse_release_date(date_str: str) -> datetime:
    if not date_str:
        return datetime(1800, 1, 1)
    parts = date_str.split("-")
    
    try:
        if len(parts) == 1: #YYYY
            return datetime(int(parts[0]), 1, 1)
        elif len(parts) == 2: #YYYY, MM
            return datetime(int(parts[0]), int(parts[1]), 1)
        elif len(parts) == 3: #YYYY, MM, DD
            return datetime(int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        pass
    
    return datetime(1800, 1, 1)

def get_playlist_tracks(playlist_id):
    results = []
    offset = 0

    while True:
        response = spotify_client.playlist_items(
            playlist_id,
            offset=offset,
            limit=100,
            additional_types=["track"]
        )

        items = response["items"]
        if not items:
            break

        for item in items:
            track = item["track"]
            if not track or not track.get("id"):
                continue #ignore local/unavailable tracks
            results.append({
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "release_date": parse_release_date(
                    track["album"]["release_date"]
                )
            })
        
        offset += 100
    return results

def create_sorted_playlist(original_playlist, sorted_tracks):
    user_id = spotify_client.current_user()["id"]

    new_playlist = spotify_client.user_playlist_create(
        user=user_id,
        name=f"{original_playlist['name']} (Oldest → Newest)",
        public=False,
        description="Sorted by release date (oldest to newest)"
    )

    track_ids = [track["id"] for track in sorted_tracks]

    # Spotify only allows 100 tracks per request
    for i in range(0, len(track_ids), 100):
        spotify_client.playlist_add_items(
            new_playlist["id"],
            track_ids[i:i+100]
        )

    return new_playlist["external_urls"]["spotify"]

def sort_tracks_by_date(tracks):
    return sorted(tracks, key=lambda x: x["release_date"])

def main():
    if len(sys.argv) != 2:
        print("Usage: python spotisort.py <playlist_url>")
        sys.exit(1)

    playlist_url = sys.argv[1]
    playlist_id = extract_playlist_id(playlist_url)

    print("Fetching playlist...")
    playlist = spotify_client.playlist(playlist_id)

    print("Getting tracks...")
    tracks = get_playlist_tracks(playlist_id)

    print(f"Sorting {len(tracks)} tracks...")
    sorted_tracks = sort_tracks_by_date(tracks)

    print("Creating new playlist...")
    new_playlist_url = create_sorted_playlist(playlist, sorted_tracks)

    print("\n Done!")
    print(f"New playlist created: {new_playlist_url}")


if __name__ == "__main__":
    main()

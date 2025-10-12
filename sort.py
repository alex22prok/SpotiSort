import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# https://spotipy.readthedocs.io/en/2.25.1/#authorization-code-flow
# Load environment variables
load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-read-playback-state user-modify-playback-state"
))


#Get playlist_id from playlist URL passed as argument
#maybe allow different input to find playlist such as -url or -name with account
match sys.argv[1]:
    case "-url":
        playlist_url = sys.argv[2]
        playlist_id = playlist_url.split("list=")[1]
        playlist = sp.playlist(playlist_id)
    case "-id":
        #
        playlist_id = sys.argv[2]
    case "-name":
        #
        playlist_name = sys.argv[2]


def extract():
    # create new playlist
    # sort existing within program
    # add each oldest song to new playlist in order
    for track in playlist["tracks"]["items"]:
        #extract(track_id, release_date)
        tracks = track

    merge_sort(tracks)



def merge_sort(tracks):
    if len(tracks) <= 1:
        return tracks
        
    mid = len(tracks) // 2
    left = merge_sort(tracks[:mid])
    right = merge_sort(tracks[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i["release_date"]] <= right[j["release_date"]]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    result.extend(left[i:])
    result.extend(right[j:])
    return result



# Spotisort
Spotisort is a small script to sort Spotify playlists by release date from oldest to newest.

## Requirements
- [Spotipy](https://github.com/spotipy-dev/spotipy) module (`pip install spotipy`)
- A [Spotify app](https://developer.spotify.com/dashboard/applications)


## Installation
```
git clone https://github.com/alex22prok/SpotiSort
```
 
Edit `config.ini` with the data you got from the Spotify app. The Redirect URI inserted has to be whitelisted in the Spotify app settings


## Usage
$ ./python spotisort.py <playlist_url>


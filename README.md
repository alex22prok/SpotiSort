# Spotisort
Spotisort is a small script to sort Spotify playlists by release date from oldest to newest.

## Requirements
- [Spotipy](https://github.com/spotipy-dev/spotipy) module (`pip3 install spotipy`)
- A [Spotify app](https://developer.spotify.com/dashboard/applications)


## Installation
```
git clone https://github.com/alex22prok/SpotiSort
```
 
Remember to edit `config.ini` with the data you got from the Spotify app. The Redirect URI inserted has to be whitelisted in the Spotify app settings as in figure.


## Usage
$ ./python spotisort.py <playlist_url>


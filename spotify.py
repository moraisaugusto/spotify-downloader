import os
from libs.spotify import Spotify
from libs.youtube import Youtube

# Credentials
os.environ["SPOTIPY_CLIENT_ID"] = ''
os.environ["SPOTIPY_CLIENT_SECRET"] = ''
os.environ["SPOTIPY_REDIRECT_URI"] = 'augustomorais.com.br'


# Retrieving each Playlist and Recording on Database
#spotify = Spotify()
#spotify.retrievePlaylists("")


# Getting every Music
youtube = Youtube()
youtube.getMusics('')




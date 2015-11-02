#!/usr/bin/env python3

import os
from libs.spotify import Spotify
from libs.youtube import Youtube

# Credentials
os.environ["SPOTIPY_CLIENT_ID"] = '8b7bf9e74d7a4a91a05979c04f0cd946'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'c2d172637b9d4a4b8c04aefbfbc1cbea'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://augustomorais.com.br'


# Retrieving each Playlist and Recording on Database
#spotify = Spotify()
#spotify.retrievePlaylists("moraisaf")


# Getting every Music
youtube = Youtube()
youtube.getMusics('Rock!')




#!/usr/bin/env python3

import os
import sys
from libs.spotify import Spotify
from libs.youtube import Youtube

# Credentials
os.environ["SPOTIPY_CLIENT_ID"] = '8b7bf9e74d7a4a91a05979c04f0cd946'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'c2d172637b9d4a4b8c04aefbfbc1cbea'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://augustomorais.com.br'

if len(sys.argv) == 1:
    print("There is a argument missing.")
    print("update: update all spotify musics")
    print("sync PLAYLIST: download all music from a PLAYLIST")
    exit()

if "update" in sys.argv[1]:
    # Retrieving each Playlist and Recording on Database
    spotify = Spotify()
    spotify.retrievePlaylists("moraisaf")

elif "sync" in sys.argv[1]:
    if 3 <= len(sys.argv):
        # Getting every Music
        youtube = Youtube()
        youtube.getMusics(sys.argv[2])
    else:
        print("Please, select a playlist to download\n")
else:
    print("Select the correct parameters: update or sync PLAYLIST\n")


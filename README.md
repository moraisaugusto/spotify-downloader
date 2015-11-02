# Spotify Downloader

__Spotify Downloader__ is a app that download your the spotify playlist, convert all musics to mp3 and write the tag3d. This was created only for educational use. 


### Prerequisites

* Linux / Windows (tested on Debian)
* Python Modules: youtube_dl,  beautifulsoup4, mutagen, spotipy
* ffmpeg


### Installation

Install all Python modules: 

```shell
pip3 install youtube_dl beautifulsoup4 mutagen spotipy
aptitude install ffmpeg
```

#### Configuration

Create the download and tmp folders

```shell
mkdir downloads tmp
```

Configure your credentials. Edit the file spotify.py

```shell
os.environ["SPOTIPY_CLIENT_ID"] = ''
os.environ["SPOTIPY_CLIENT_SECRET"] = ''
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://yourredirectURI'
spotify.retrievePlaylists("SPOTIFYUSERNAME")
youtube.getMusics('YOURPLAYLIST')
```

#### Using

Edit the file spotify.py

NOTE: The first time when you run the script will be ask to you the REDIRECT URI. Just paste the URI returned from the given URI. 

```shell
python spotify.py
```

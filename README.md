# Another Dotfiles


__Another dotfiles__ is a collection of ZSH and VIM configurations based on [robbyrussell/oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) and [nicknisi/dotfiles](https://github.com/nicknisi/dotfiles). 

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
os.environ["SPOTIPY_REDIRECT_URI"] = 'yourredirectURI'
```

## License

Another Dotfiles is released under the [MIT license](https://raw.githubusercontent.com/aflavio/another-dotfiles/master/LICENSE).

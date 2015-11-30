import spotipy
import spotipy.util as util

class Spotify():
    """Spotify

    This class gets the user`s playlists and tracks

    """

    def retrievePlaylists(self, username):
        """ Retrieves all user playlists """
        token = util.prompt_for_user_token(username)

        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(username, 50)

            for playlist in playlists['items']:
                playlist['name'] = self.clear_str(playlist['name'])

                print('Syncing: {0}'. format(str(playlist['name'])))
                print('\tTracks: {0}\n'. format(playlist['tracks']['total']))

                results = sp.user_playlist(username, playlist['id'], fields='tracks, album, next')
                tracks = results['tracks']

                self.show_tracks(tracks, playlist['name'])
                while tracks['next']:
                    tracks = sp.next(tracks)
                    self.show_tracks(tracks, playlist['name'])

        return True


    def show_tracks(self, tracks, playlist):
        """ Gets all tracks data """
        import sqlite3

        conn = sqlite3.connect("data/spotify.db")
        cursor = conn.cursor()

        for i,item in enumerate(tracks['items']):
            track = item['track']
            artwork = str(track['album']['images'][0]['url'])
            artist = track['artists'][0]['name']
            title = track['name']
            trackNumber = str(track['track_number'])
            trackID = track['id']
            album = self.clear_str(track['album']['name'])

            sql = 'SELECT * FROM musics WHERE id=?'
            cursor.execute(sql, [(trackID)])

            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO musics VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                                    (trackID , playlist, artist, title, album,
                                    trackNumber, artwork, 0))

                print('Writing Track ID: {0}'.  format(trackID))
                conn.commit()

    def clear_str(self, string):
        """ Clear strange Unicode Chars """
        string.replace(u'\u2014', u'-') # replacing hiphen char
        string.replace(u'\u2013', u'-') # replacing hiphen char
        string = string.encode('cp850','replace').decode('cp850')

        return string


import sys
import os
#import glob
from bs4 import BeautifulSoup
#from bs4 import UnicodeDammit
#from inspect import getmembers
#from pprint import pprint
import sqlite3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TRCK, TIT2, TPE1, TALB, TDRC, TCON, COMM, error
import urllib.request
from optparse import TitledHelpFormatter
from libs.util import retry


#Loading libs
if (sys.version_info > (3,0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
#else:
#    from urllib2 import urlopen
#    from urllib import quote_plus as qp  

class Youtube():
    """ Youtube
    
    This Class performs the download from Youtube and Write the ID3 tags on mp3.
    
    Table musics: 
        flags: 
            0 - not downloaded
            1 - downloaded
            2 - synced
    """
    TMP_DIR = os.getcwd() + '/tmp/'
    DL_DIR = os.getcwd() + '/downloads/'

    def getMusics(self, playlist):
        """ Download musics from a playlist """
        
        conn = sqlite3.connect('data/spotify.db')
        cursor = conn.cursor()
        
        sql = 'SELECT * FROM musics WHERE flag = 0 AND playlist = "' + playlist + '"'
        cursor.execute(sql)
        musics = cursor.fetchall()
        
        if not musics:
            print('All Musics from "{0}" playlist are already downloaded'. format(playlist))
            # Creating playlist only for downloaded musics
            sql = 'SELECT * FROM musics WHERE flag = 1 AND playlist = "' + playlist + '"'
            cursor.execute(sql)
            musics = cursor.fetchall()
            
            self.create_m3u(playlist, musics)    
            exit()
        
        print('Playlist: ' + str(musics[0][1]))
        
        for music in musics:
            
            # check if music is already downloaded
            downloaded = self.find(music[0] + '.mp3', self.DL_DIR)
            if downloaded is not None:
                print ('Already downloaded: {0}' . format(music[0]))
                sql = 'UPDATE musics set flag = 1 WHERE id = "' + music[0] + '"'
                cursor.execute(sql)
                conn.commit()
                continue
            
            query = music[2] + " - " + music[3]
            
            # Magic happens here.
            video_link = self.performYoutubeSearch(query)
            
            if video_link is not False:
                
                self.performYoutubeDownload(music[1], music[0], video_link)
                self.writeID3tag(music, music[0])
            else:
                print ('Nothing found')
                
        self.create_m3u(playlist, musics)    
        
        return True
    
        
    
    @retry(3, delay=0.1)
    def performYoutubeSearch(self, query):
        """ Perform a Youtube Search """
        response = urlopen('https://www.youtube.com/results?search_query=' + qp(query))
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            if '/watch?v=' in link.get('href'):
                # May change when Youtube gets updated in the future.
                video_link = link.get('href')
                break
        
        result = soup.find('a', 'yt-uix-tile-link')
        
        if result is not None:
            title = soup.find('a', 'yt-uix-tile-link').text
            title = title.encode('latin-1', 'ignore').decode('utf-8', 'ignore')
            print("Found: " + title)
            return video_link
        else:
            return False
        
    def performYoutubeDownload(self, playlist, audioFileName, video_link):
        """ Performs music download from Youtube """         
        # Links are relative on page, making them absolute.
        video_link = 'http://www.youtube.com/' + video_link
        command = 'youtube-dl -q -o "' + self.DL_DIR + audioFileName + '.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 0 ' + video_link 
        
        # Youtube-dl is a proof that god exists.
        os.system(command)
        return True
        
    def writeID3tag(self, info, audioFile):
        """ Writes the ID3 on mp3  """
        
        # writing id3 tag
        audioPath = self.DL_DIR + audioFile + '.mp3'
        audio = ID3(audioPath)
        
        audio.add(TIT2(encoding=3, text=info[3])) # title
        audio.add(TPE1(encoding=3, text=info[2])) #artist
        audio.add(TALB(encoding=3, text=info[4])) # album
        audio.add(TRCK(encoding=3, text=str(info[5]))) # track Number
        audio.add(COMM(encoding=3, text=u'by <aflavio at gmail.com>')) # comments
        
        # writing artwork on mp3
        artworkFile = audioFile + '.jpg'
        urllib.request.urlretrieve(info[6], self.TMP_DIR + artworkFile)
        pic = APIC(3, u'image/jpg', 3, u'Front cover', open(self.TMP_DIR + artworkFile, 'rb').read())
        audio.add(pic)
        
        audio.save()
    
    def create_m3u(self, playlist, musics):
        """ Create the playlist """
        
        # converting list to array
        all_musics = []
        for music in musics:
            all_musics.append(music[0] + '.mp3')
        
        try:
            print ('Processing directory...')
    
            playlist = playlist + '.m3u'
            mp3s = []
    
            os.chdir(self.DL_DIR)
            
            # getting mp3 data            
            for file in all_musics:
                meta_info = {
                    'filename': file,
                    'length': int(MP3(file).info.length),
                    'tracknumber': EasyID3(file)['tracknumber'][0].split('/')[0],
                }
                mp3s.append(meta_info)
            
            if len(mp3s) > 0:
                print ('Writing playlist {0}...' . format(playlist))
    
                # write the playlist
                of = open('../' + playlist, 'w')
                of.write("#EXTM3U\n")
    
                #sorted by track number
                for mp3 in mp3s:
                    of.write('#EXTINF:{0},{1}\n' . format(mp3['length'], mp3['filename']))
                    of.write('downloads/' + mp3['filename'] + "\n")
    
                of.close()
            else:
                print ('No mp3 files found.')
    
        except:
            print ('ERROR occured when processing directory. Ignoring.')
            print ('Text: {0}'. format(sys.exc_info()[0]))
    
    def find(self, name, path):
        """ Try to find a file in a directory """
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

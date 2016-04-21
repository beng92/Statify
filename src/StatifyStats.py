'''
x Total plays
x Total artists
x Total unique songs
  Average song per artist
x Favourite track
  Favourite artist (by plays or time)
  Favourite album (req. api)
  Average/total/unique plays per range
  Average/total/unique artists per range
  Average/total time listened per range
  Favourite genre (req. api) (by plays or time)
  % songs skipped before end (req. api)
  Most skipped song/artist (req. api)
  Graph of time of day listening
  Graph of day of the week listening
  Listening habits by Spotify values e.g. accousticness (req. api)
  Search listening history

https://developer.spotify.com/web-api/
https://github.com/plamere/spotipy
http://spotipy.readthedocs.org/en/latest/
http://cgbystrom.com/articles/deconstructing-spotifys-builtin-http-server/
https://github.com/cgbystrom/spotify-local-http-api/issues/2
https://github.com/cgbystrom/spotify-local-http-api
http://effbot.org/zone/wcklib-calendar.htm
http://svn.python.org/projects/sandbox/trunk/ttk-gsoc/samples/ttkcalendar.py
'''

import time, datetime, StatifyCache, logging
import libs.spotipy as spotipy

# Songs read in order (date, artist, title)

class StatifyStats:
    def __init__(self):
        self.allSongs = []
        self.allItems = []
        self.firstdate = None
        self.enddate = None
        logging.basicConfig(filename="debug.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s > %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        self.length = 0
        
        self.spotify = spotipy.Spotify()
        self.sc = StatifyCache.StatifyCache()
        self.cache()
        
    def cache(self):
        """Re-cache's the new list. Called on reload.
        """
        logging.info("Cache initiated")
        for (date, artist, title) in list(set(self.allSongs)):
            if not self.sc.existsSong(title, artist):
                songid = self.sc.search(title, artist)
                if songid != None:
                    result = self.sc.add(songid, "song")
                    logging.debug("Adding songid to cache: " + str(songid))
                    if result != None and not self.sc.existsID(result.artistid, "artist"):
                        self.sc.add(result.artistid, "artist")
                        logging.debug("Added artistid to cache: " + result.artistid)
                    if result != None and not self.sc.existsID(result.albumid, "album"):
                        self.sc.add(result.albumid, "album")
                        logging.debug("Adding albumid to cache: " + result.albumid)
                
    
    
    def most_common(self, list):
        d = {}
        for item in list:
            if item in d:
                d[item] = d[item] + 1
            else:
                d[item] = 1
        max = 0
        name = ""
        for item in d:
            if d[item] > max:
                max = d[item]
                name = item
        return (name,max)
    
    def most_common_artist_plays(self, list):
        return self.most_common([a for d,a,t in list])
        
    def most_common_artist_link(self, artist):
        try:
            return self.sc.getName(artist, "artist").artisturl
        except: 
            logging.warning("Could not get most common artist link")
            return None
        
    def most_common_song_plays(self, list):
        return self.most_common([(a,t) for d,a,t in list])
        
    def most_common_song_link(self, song):
        try:
            return self.sc.getName(song, "song").songurl
        except: 
            logging.warning("Could not get most common song link")
            return None
    
    def listening_time(self, list): # Expecting self.allItems in form (d,s)
        timer = datetime.timedelta()
        start = None
        for d,s in list:
            if start == None:
                start = d
            if s == "Spotify":
                end = d
                timer = timer + (d - start)
                start = None
        if start != None:
            timer = timer + (datetime.datetime.now() - start)
        return timer
                
    def load(self, start, end):
        """Loads the data.txt file created by StatifyTracking.pyw
        """
        file = open("data/data.txt")
        lines = file.read().splitlines()
        file.close()
        ret = len(lines) > self.length
        self.length = len(lines)
        
        
        
        self.allSongs = []
        self.allItems = []
        self.firstdate = None

        for line in lines:
            dateLine = line.split('>',1)[0]
            date = datetime.datetime.strptime(dateLine, "%a %b %d %H:%M:%S %Y")
            if self.firstdate == None:
                self.firstdate = date
            self.enddate = date
            song = line.split('>',1)[1]
            index = lines.index(line)
            if song != "Spotify" and song != "" and index+2 < len(lines) and not (lines[index+1].split(">",1)[1] == "Spotify" and lines[index+2].split(">",1)[1] == song):
                artistName = song.split(" - ",1)[0]
                songName = song.split(" - ",1)[1]
                self.allSongs.append((date, artistName, songName))
            if song != "":
                self.allItems.append((date,song))
        
        if start != None and end != None:
            self.allSongs = [(d,a,t) for d,a,t in self.allSongs if d >= start and d <= end]
            self.allItems = [(d,s) for d,s in self.allItems if d >= start and d <= end]

        return ret

        
    def plays(self):
        """Return total number of plays for the currently loaded list
        """
        return str(len(self.allSongs))
    def artists(self):
        """Return number of artists in the currently loaded list
        """
        return str(len(set([a for d,a,t in self.allSongs])))
    def uniquePlays(self):
        """Return the number of songs in the currently loaded list
        """
        return str(len(set([(a,t) for d,a,t in self.allSongs])))
    def mcSong(self):
        """Returns the most common song, with a link to the Spotify page.
        """
        results = self.most_common_song_plays(self.allSongs)
        return (" - ".join(results[0]) + " (" + str(results[1]) + ")", self.most_common_song_link(results[0][1]))
    def mcArtist(self):
        """Returns the most common artist, with a link to the Spotify page.
        """
        results = self.most_common_artist_plays(self.allSongs)
        return (results[0] + " (" + str(results[1]) + ")", self.most_common_artist_link(results[0]))
    def listenTime(self):
        """Returns the total listening time for the currently selected range.
        """
        result = self.listening_time(self.allItems)
        days = int(result.days)
        hours = int(result.seconds/3600)
        minutes = int(result.seconds/60)-(hours*60)
        return str(days) + (" day, " if result.days == 1 else " days, ") + str(hours) + (" hour, " if hours == 1 else " hours, ") + str(minutes) + (" minute " if minutes == 1 else " minutes ")
        return ret
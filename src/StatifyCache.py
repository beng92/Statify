import spotipy

class StatifyCache:
    def __init__(self):
        self.spotipy = spotipy.Spotify()
        file = open("data/cache.xml",'r')
        read = file.read()
    
    def add(self, songid, artistid, albumid):
        if(songid != None):
            self.addSong(songid)
        if(artistid != None):
            self.addArtist(artistid)
        if(albumid != None):
            self.addAlbum(albumid)
    
    def addSong(self, id):
        result = self.spotipy.track(id)
        name     = result['name']
        songurl  = result['external_urls']['spotify']
        artist   = result['artists'][0]['name']
        artistid = result['artists'][0]['id']
        album    = result['album']['name']
        albumid  = result['album']['id']
        explicit = result['explicit']
        discno   = result['disc_number']
        trackno  = result['track_number']
        duration = result['duration_ms']
        song = Song(id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration)
    
    def addArtist(self, id):
        result = self.spotipy.artist(id)
        name      = result['name']
        artisturl = result['external_urls']['spotify']
        imageurl  = result['images'][0]['url']
        artist = Artist(id, name, artisturl, imageurl)
        
    def addAlbum(self, id):
        result = self.spotipy.album(id)
        name        = result['name']
        artist      = result['artists'][0]['name']
        artistid    = result['artists'][0]['id']
        albumurl    = result['external_urls']['spotify']
        imageurl    = result['images'][0]['url']
        tracks      = []
        duration    = 0
        for track in result['tracks']['items']:
            tracks.append(track['name'])
            duration += track['duration_ms']
        totaltracks = result['tracks']['total']
        album = Album(id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration)
        
        
class Song: 
    def __init__(self, id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration):
        print ("Song:", id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration)
    
    def write(self):
        pass
        
        
class Artist: 
    def __init__(self, id, name, artisturl, imageurl):
        print ("Artist:", id, name, artisturl, imageurl)
    
    def write(self):
        pass
        
        
class Album: 
    def __init__(self, id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration):
        print ("Album:", id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration)
    
    def write(self):
        pass
        
        
def test():
    sc = StatifyCache()
    sc.add("2ELcuwXrtMA8ect9cGTYnQ","2Dr744zaEbNqmW9jxw4gfq","2PqYzY7wdgq0ydlC3nR4ei")

test()
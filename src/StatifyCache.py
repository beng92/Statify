import spotipy
import xml.etree.ElementTree as ET


class StatifyCache:
    def __init__(self):
        self.spotipy = spotipy.Spotify()
        self.tree = ET.parse("data/cache.xml")
        self.root = self.tree.getroot()
        self.allSongs   = self.root[0]
        self.allArtists = self.root[1]
        self.allAlbums  = self.root[2]
        
    def add(self, songid, artistid, albumid):
        if(songid != None and not self.exists(id, "song")):
            self._addSong(songid)
        if(artistid != None and not self.exists(id, "artist")):
            self._addArtist(artistid)
        if(albumid != None and not self.exists(id, "album")):
            self._addAlbum(albumid)
    
    def _addSong(self, id):
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
        return Song(self.tree, id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration)
    
    def _addArtist(self, id):
        result = self.spotipy.artist(id)
        name      = result['name']
        artisturl = result['external_urls']['spotify']
        imageurl  = result['images'][0]['url']
        return Artist(self.tree, id, name, artisturl, imageurl)
        
    def _addAlbum(self, id):
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
        return Album(self.tree, id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration)
    
    def exists(self, id, type):
        found = False
        if type == "song" or type == "any":
            for track in self.allSongs.findall('song'):
                if track.find('id').text == id:
                    found = True 
        if type == "artist"or type == "any":
            for artist in self.allArtists.findall('artist'):
                if artist.find('id').text == id:
                    found = True
        if type == "album" or type == "any":
            for album in self.allAlbums.findall('album'):
                if album.find('id').text == id:
                    found = True
        else:
            return None
        return found
    
    def get(self, id):
        if self.exists(id, "any"):
            for track in self.allSongs.findall('song'):
                if track.find('id').text == id:
                    return track
            for artist in self.allArtists.findall('artist'):
                if artist.find('id').text == id:
                    return artist
            for album in self.allAlbums.findall('album'):
                if album.find('id').text == id:
                    return album
        else:
            return None
            
class Song: 
    def __init__(self, tree, id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration):
        self.id = id
        self.name = name
        self.songurl = songurl
        self.artist = artist
        self.artistid = artistid
        self.album = album
        self.albumid = albumid
        self.explicit = explicit
        self.discno = discno
        self.trackno = trackno
        self.duration = duration
        
        self.tree = tree
        self.write()
        #print ("Song:", id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration)
    
    def write(self):
        new = ET.Element('song')
        
        newid           = ET.SubElement(new, 'id')
        newname         = ET.SubElement(new, 'name')
        newsongurl      = ET.SubElement(new, 'songurl')
        newartist       = ET.SubElement(new, 'artist')
        newartistid     = ET.SubElement(new, 'artistid')
        newalbum        = ET.SubElement(new, 'album')
        newalbumid      = ET.SubElement(new, 'albumid')
        newexplicit     = ET.SubElement(new, 'explicit')
        newdiscno       = ET.SubElement(new, 'discno')
        newtrackno      = ET.SubElement(new, 'trackno')
        newduration     = ET.SubElement(new, 'duration')
       
        
        newid.text          = self.id 
        newname.text        = self.name 
        newsongurl.text     = self.songurl 
        newartist.text      = self.artist 
        newartistid.text    = self.artistid 
        newalbum.text       = self.album
        newalbumid.text     = self.albumid
        newexplicit.text    = str(self.explicit)
        newdiscno.text      = str(self.discno)
        newtrackno.text     = str(self.trackno)
        newduration.text    = str(self.duration)
        
        self.tree.getroot()[0].append(new)
        self.tree.write("data/cache.xml")
        
        
class Artist: 
    def __init__(self, tree, id, name, artisturl, imageurl):
        self.id = id
        self.name = name
        self.artisturl = artisturl
        self.imageurl = imageurl
        
        self.tree = tree
        self.write()
        #print ("Artist:", id, name, artisturl, imageurl)
    
    def write(self):
        new = ET.Element('artist')
        
        newid        = ET.SubElement(new, 'id')
        newname      = ET.SubElement(new, 'name')
        newartisturl = ET.SubElement(new, 'artisturl')
        newimageurl  = ET.SubElement(new, 'imageurl')
        
        newid.text        = self.id
        newname.text      = self.name
        newartisturl.text = self.artisturl
        newimageurl.text  = self.imageurl
        
        self.tree.getroot()[1].append(new)
        self.tree.write("data/cache.xml")
        
        
class Album: 
    def __init__(self, tree, id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration):
        self.id = id
        self.name = name
        self.artist = artist
        self.artistid = artistid
        self.albumurl = albumurl
        self.imageurl = imageurl
        self.tracks = tracks
        self.totaltracks = totaltracks
        self.duration = duration
        
        self.tree = tree
        self.write()
        #print ("Album:", id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration)
    
    def write(self):
        new = ET.Element('album')
        
        newid           = ET.SubElement(new, 'id')
        newname         = ET.SubElement(new, 'name')
        newartist       = ET.SubElement(new, 'artist')
        newartistid     = ET.SubElement(new, 'artistid')
        newalbumurl     = ET.SubElement(new, 'albumurl')
        newimageurl     = ET.SubElement(new, 'imageurl')
        newtracks       = ET.SubElement(new, 'tracks')
        newtotaltracks  = ET.SubElement(new, 'totaltracks')
        newduration     = ET.SubElement(new, 'duration')
       
        
        newid.text          = self.id 
        newname.text        = self.name 
        newartist.text      = self.artist 
        newartistid.text    = self.artistid 
        newalbumurl.text    = self.albumurl
        newimageurl.text    = self.imageurl
        newtracks.text      = str(self.tracks)
        newtotaltracks.text = str(self.totaltracks)
        newduration.text    = str(self.duration)
        
        self.tree.getroot()[2].append(new)
        self.tree.write("data/cache.xml")
        
        
def test():
    sc = StatifyCache()
    #print(sc.exists("2ELcuwXrtMA8ect9cGTYnQ", "song")
    #sc.add("2ELcuwXrtMA8ect9cGTYnQ","2Dr744zaEbNqmW9jxw4gfq","2PqYzY7wdgq0ydlC3nR4ei")
    print(sc.exists("2Dr744zaEbNqmW9jxw4gfq", "any"))
    print(sc.exists("2Dr744zaEbNqsjxw4gfq", "any"))
    print(sc.get("2PqYzY7wdgq0ydlC3nR4ei"))

test()
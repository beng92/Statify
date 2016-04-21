import spotipy, logging
import xml.etree.ElementTree as ET
import os.path


class StatifyCache:
    def __init__(self):
        self.spotipy = spotipy.Spotify()
        logging.basicConfig(filename="debug.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s > %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        
        try:
            self.tree = ET.parse("data/cache.xml")
        except:
            logging.warning("Could not parse cache file... Recreating.")
            data    = ET.Element('root')
            songs   = ET.SubElement(data, 'songs')
            artists = ET.SubElement(data, 'artists')
            albums  = ET.SubElement(data, 'albums')
            ET.ElementTree(data).write("data/cache.xml")
        self.tree = ET.parse("data/cache.xml")
            
        
        self.root = self.tree.getroot()
        self.allSongs   = self.root.find('songs')
        self.allArtists = self.root.find('artists')
        self.allAlbums  = self.root.find('albums')
        
    def add(self, id, type):
        """Add a song to the cache file.
        id is type spotify ID.
        type should be song, artist or album.
        """
        if id == None or self.existsID(id, type):
            return None
        if(type == "song"):
            return self._addSong(id)
        if(type == "artist"):
            return self._addArtist(id)
        if(type == "album"):
            return self._addAlbum(id)
    
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
    
    def existsID(self, id, type):
        """Checks an id to see if it exists in the cache file
        type should be song, artist or album or any.
        """
        found = False
        if type == "song" or type == "any":
            for track in self.allSongs.findall('song'):
                if track.find('id').text == id:
                    found = True 
        if type == "artist" or type == "any":
            for artist in self.allArtists.findall('artist'):
                if artist.find('id').text == id:
                    found = True
        if type == "album" or type == "any":
            for album in self.allAlbums.findall('album'):
                if album.find('id').text == id:
                    found = True
        return found
        
    def existsSong(self, song, artist):
        """Checks a song and artist name to see if it exists in the cache file
        """
        found = False
        for track in self.allSongs.findall('song'):
            if track.find('name').text == song and track.find('artist').text == artist:
                found = True 
        return found
    
    def getID(self, id):
        """Return the Song, Artist or Album object based on id, if it exists
        """
        if self.existsID(id, "any"):
            for track in self.allSongs.findall('song'):
                if track.find('id').text == id:
                    return Song.read(track)
            for artist in self.allArtists.findall('artist'):
                if artist.find('id').text == id:
                    return Artist.read(artist)
            for album in self.allAlbums.findall('album'):
                if album.find('id').text == id:
                    return Album.read(album)
        else:
            return None
            
    def getName(self, name, type):
        """Return the Song, Artist or Album object based on name, if it exists
        type is either song, artist or album.
        """
        if type == "song":
            for track in self.allSongs.findall('song'):
                if track.find('name').text == name:
                    return Song.read(track)
        if type == "artist":
            for artist in self.allArtists.findall('artist'):
                if artist.find('name').text == name:
                    return Artist.read(artist)
        if type == "album":
            for album in self.allAlbums.findall('album'):
                if album.find('name').text == name:
                    return Album.read(album)
        return None
            
    def search(self, song, artist):
        """Sends a search string to Spotify's servers to return an ID
        Artist must not be None, song can be None
        """
        if song != None and artist != None:
            result = self.spotipy.search(q="artist:" + artist + " track:" + song, limit=1, type='track')
            if len(result['tracks']['items']) > 0:
                return result['tracks']['items'][0]['id']
            else:
                return None
        elif song == None and artist != None:
            result = self.spotipy.search(q="artist:" + artist, limit=1, type='artist')
            if len(result['artists']['items']) > 0:
                return result['artists']['items'][0]['id']
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
        
        if tree != None:
            self.tree = tree
            self.write()
        #print ("Song:", id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration)
    
    def write(self):
        """Write this object to the cache file as XML
        """
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
    
    def read(element):
        """Read this object from an Element object
        """
        id           = element.find('id').text
        name         = element.find('name').text
        songurl      = element.find('songurl').text
        artist       = element.find('artist').text
        artistid     = element.find('artistid').text
        album        = element.find('album').text
        albumid      = element.find('albumid').text
        explicit     = element.find('explicit').text
        discno       = element.find('discno').text
        trackno      = element.find('trackno').text
        duration     = element.find('duration').text
        return Song(None, id, name, songurl, artist, artistid, album, albumid, explicit, discno, trackno, duration)
        
class Artist: 
    def __init__(self, tree, id, name, artisturl, imageurl):
        self.id = id
        self.name = name
        self.artisturl = artisturl
        self.imageurl = imageurl
        
        if tree != None:
            self.tree = tree
            self.write()
        #print ("Artist:", id, name, artisturl, imageurl)
    
    def write(self):
        """Write this object to the cache file as XML
        """
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
    
    def read(element):
        """Read this object from an Element object
        """
        id        = element.find('id').text
        name      = element.find('name').text
        artisturl = element.find('artisturl').text
        imageurl  = element.find('imageurl').text
        return Artist(None, id, name, artisturl, imageurl)
        
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
        
        if tree != None:
            self.tree = tree
            self.write()
        #print ("Album:", id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration)
    
    def write(self):
        """Write this object to the cache file as XML
        """
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

    def read(element):
        """Read this object from an element object
        """
        id           = element.find('id').text
        name         = element.find('name').text
        artist       = element.find('artist').text
        artistid     = element.find('artistid').text
        albumurl     = element.find('albumurl').text
        imageurl     = element.find('imageurl').text
        tracks       = element.find('tracks').text
        totaltracks  = element.find('totaltracks').text
        duration     = element.find('duration').text
        return Album(None, id, name, artist, artistid, albumurl, imageurl, tracks, totaltracks, duration)
        
def test():
    """Used to test cache changes.
    """
    pass
    #sc = StatifyCache()
    #print(sc.existsID("2ELcuwXrtMA8ect9cGTYnQ", "song"))
    #print(sc.existsID("2Dr744zaEbNqmW9jxw4gfq", "any"))
    #print(sc.existsID("2Dr744zaEbNqsjxw4gfq", "any"))
    #print(sc.get("2PqYzY7wdgq0ydlC3nR4ei").find('name').text)
    #result = sc.add(sc.search("Lunar Liftoff", "Adam Young"), "song")
    #result = sc.get(sc.search("Lunar Liftoff", "Adam Young"))
    #result2 = sc.add(result.find('albumid').text, "album")
    #print(result2)
    #print(sc.existsSong("Lunar Liftoff", "Adam Young"))
    #print(sc.existsID("3dRfiJ2650SZu6GbydcHNb", "artist"))
    #print(sc.getName("Adam Young","artist").artisturl)
    
    
    
test()
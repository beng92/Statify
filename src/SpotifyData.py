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
'''

import time, datetime, spotipy

# Songs read in order (date, artist, title)

def most_common(list):
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

def reduce_range(list):
    sel1 = input("  1. All time\n  2. Set start date and time\n  3. Set end date and time\n  4. Set both start and end\n> ")
    start = datetime.datetime.strptime("01/01/00 00:00:00", "%d/%m/%y %H:%M:%S")
    end = datetime.datetime.now()
    
    if(sel1 == "1"):
        return list
    if(sel1 == "2" or sel1 == "4"):
        print("\nEnter start date and time\n")
        startdate = input("Enter date (dd/mm/yy): ")
        starttime = input("Enter time (hh:mm:ss): ")
        if startdate == "today" or startdate == "":
            startdate = datetime.datetime.strftime(datetime.date.today(), "%d/%m/%y")
        if starttime == "now"or starttime == "":
            starttime = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
        try:
            start = datetime.datetime.strptime(startdate + " " + starttime, "%d/%m/%y %H:%M:%S")
        except:
            print("Error")
            
    if(sel1 == "3" or sel1 == "4"):
        print("\nEnter end date and time\n")
        enddate = input("Enter date (dd/mm/yy): ")
        endtime = input("Enter time (hh:mm:ss): ")
        if enddate == "today" or enddate == "":
            enddate = datetime.datetime.strftime(datetime.date.today(), "%d/%m/%y")
        if endtime == "now" or endtime == "":
            endtime = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
        try:
            end = datetime.datetime.strptime(enddate + " " + endtime, "%d/%m/%y %H:%M:%S")
        except:
            print("Error")
        
    if len(list[0]) == 2:
        result = [(d,s) for d,s in list if d >= start and d <= end]
    elif len(list[0]) == 3:
        result = [(d,a,t) for d,a,t in list if d >= start and d <= end]
    else: 
        return None
    return result
    
    
def reduce_range_previous(list):
    sel2 = input("  1. All time\n  2. Enter number of weeks\n  3. Enter number of days\n  4. Enter number of hours\n> ")
    if(sel2 == "1"):
        return list
        
    elif(sel2 == "2" or sel2 == "3" or sel2 == "4"):
        start = datetime.datetime.now()
        end = datetime.datetime.now()
        if(sel2 == "2"):
            sel3 = input("Weeks = ")
            start = start - datetime.timedelta(weeks=int(sel3))
        if(sel2 == "3"):
            sel3 = input("Days = ")
            start = start - datetime.timedelta(days=int(sel3))
        if(sel2 == "4"):
            sel3 = input("Hours = ")
            start = start - datetime.timedelta(hours=int(sel3))
    
    if len(list[0]) == 2:
        result = [(d,s) for d,s in list if d >= start and d <= end]
    elif len(list[0]) == 3:
        result = [(d,a,t) for d,a,t in list if d >= start and d <= end]
    else: 
        return None
    return result
    
    
def most_common_artist_plays(list):
    return most_common([a for d,a,t in list])
    
def most_common_song_plays(list):
    return most_common([(a,t) for d,a,t in list])

def listening_time(list): # Expecting allItems in form (d,s)
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
            

# http://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

allSongs = []
allItems = []
spotify = spotipy.Spotify()

def load():
    file = open("SpotifyStats.txt")
    lines = file.read().splitlines()
    file.close()

    global allSongs
    global allItems
    allSongs = []
    allItems = []

    for line in lines:
        dateLine = line.split('>',1)[0]
        date = datetime.datetime.strptime(dateLine, "%a %b %d %H:%M:%S %Y")
        song = line.split('>',1)[1]
        if song != "Spotify" and song != "":
            artistName = song.split(" - ",1)[0]
            songName = song.split(" - ",1)[1]
            allSongs.append((date, artistName, songName))
        if song != "":
            allItems.append((date,song))
    print("Loaded songs.")


load()
while True:
    print("\nWhich option would you like?")
    print("  1. Number of Plays\n  2. Number of Unique Songs\n  3. Number of Artists\n  4. Most Common Track\n  5. Most Common Artist\n  6. Listening Time\n  7. Reload Data")
    selection = input("> ")

    if(selection == "1"):
        print("\nNumber of songs: " + str(len(reduce_range(allSongs))))
    
    elif(selection == "2"):
        print("\nNumber of unique songs: " + str(len(set([(a,t) for d,a,t in reduce_range(allSongs)]))))
    
    elif(selection == "3"):
        print("\nNumber of Artists: " + str(len(set([a for d,a,t in reduce_range(allSongs)]))))

    elif(selection == "4"):
        results = most_common_song_plays(reduce_range(allSongs))
        print("\nFavourite Song is {} with {} plays".format(' - '.join(results[0]), str(results[1])))
        try:
            searchResult = spotify.search(q="artist:" + results[0][0] + " track:" + results[0][1], limit=1,type='track')
            url = str(searchResult['tracks']['items'][0]['external_urls']['spotify'])
            print(url)
        except: 
            pass
        
    elif(selection == "5"):
        results = most_common_artist_plays(reduce_range(allSongs))
        print("\nFavourite Artist is {} with {} plays".format(results[0], str(results[1])))
        try:
            searchResult = spotify.search(q="artist:" + results[0], limit=1,type='track')
            url = str(searchResult['tracks']['items'][0]['artists'][0]['external_urls']['spotify'])
            print(url)
        except: 
            pass
        
    elif(selection == "6"):
        result = listening_time(reduce_range(allItems))
        days = int(result.days)
        hours = int(result.seconds/3600)
        minutes = int(result.seconds/60)-(hours*60)
        print ("\nListening time:", str(days), "day" if result.days == 1 else "days", str(hours), "hour" if hours == 1 else "hours", str(minutes), "minute" if minutes == 1 else "minutes")
        
    elif(selection == "7"):
        load()
    else:
        print ("Error.\n> ")


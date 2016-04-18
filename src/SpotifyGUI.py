from tkinter import *
from SpotifyStats2 import *
from ttkcalendar import *
from CalendarDialog import *

class SpotifyGUI2:
    def __init__(self):

        root = Tk()
        ss = SpotifyStats()
        
        mainFrame = Frame(root)
        bottomFrame = Frame(root)
        labels = {}
        #http://effbot.org/zone/wcklib-calendar.htm
        #http://svn.python.org/projects/sandbox/trunk/ttk-gsoc/samples/ttkcalendar.py
        
        startdate = ss.firstdate
        enddate = ss.enddate
        
        
        def startcal():
            startdate = CalendarDialog(root).result
        def endcal():
            enddate = CalendarDialog(root).result

        startB = Tkinter.Button(root, text="Start", command=startcal)
        endB = Tkinter.Button(root, text="End", command=endcal)
        startB.pack()
        endB.pack()
        
        
        
        def reload():
            ss.load()
            ss.range(startdate, enddate)
            labels["1. Plays"] = ss.plays()
            labels["2. Unique Songs"] = ss.uniquePlays()
            labels["3. Artists"] = ss.artists()
            labels["4. Most Common Track"] = ss.mcSong()
            labels["5. Most Common Artist"] = ss.mcArtist()
            labels["6. Listening Time"] = ss.listenTime()
        
            count = 0
            for a in sorted(labels.keys()):
                left = Label(mainFrame,text=a)
                right = Label(mainFrame, text=labels[a])
                left.grid(column=0, row=count, sticky=W)
                right.grid(column=1, row=count, sticky=W)
                count += 1
        
        mainFrame.pack()
        bottomFrame.pack()
        reloadB = Button(bottomFrame, text="Reload", command=reload)
        reloadB.pack()
        reload()
        root.mainloop()
        

SpotifyGUI2()
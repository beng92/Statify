from tkinter import *
from SpotifyStats import *
from libs.ttkcalendar import *
from libs.CalendarDialog import *

class SpotifyGUI:
    def __init__(self):

        root = Tk()
        ss = SpotifyStats()
        
        topFrame = Frame(root)
        mainFrame = Frame(root)
        bottomFrame = Frame(root)
        labels = {}

        ss.load(None, None)
        global startdate, enddate
        startdate = ss.firstdate
        enddate = ss.enddate
        
        startL = Label(topFrame,text=startdate)
        endL = Label(topFrame,text=enddate)
        
        def startcal():
            global startdate
            startdate = CalendarDialog(root).result
            startL.config(text=startdate)
        def endcal():
            global enddate
            enddate = CalendarDialog(root).result
            endL.config(text=enddate)
            

        startB = Tkinter.Button(topFrame, text="Start", command=startcal)
        endB = Tkinter.Button(topFrame, text="End", command=endcal)
        startB.pack(side=LEFT)
        startL.pack(side=LEFT)
        endB.pack(side=LEFT)
        endL.pack(side=LEFT)
        
        
        
        def reload(): 
            ss.load(startdate, enddate)
            labels["1. Plays"] = ss.plays()
            labels["2. Unique Songs"] = ss.uniquePlays()
            labels["3. Artists"] = ss.artists()
            labels["4. Most Common Track"] = ss.mcSong()
            labels["5. Most Common Artist"] = ss.mcArtist()
            labels["6. Listening Time"] = ss.listenTime()
        
            count = 0
            for child in mainFrame.winfo_children():
                child.destroy()
            for a in sorted(labels.keys()):
                left = Label(mainFrame,text=a)
                right = Label(mainFrame, text=labels[a])
                left.grid(column=0, row=count, sticky=W)
                right.grid(column=1, row=count, sticky=W)
                count += 1
        
        topFrame.pack()
        mainFrame.pack()
        bottomFrame.pack()
        reloadB = Button(bottomFrame, text="Reload", command=reload)
        reloadB.pack()
        reload()
        root.mainloop()
        

SpotifyGUI()
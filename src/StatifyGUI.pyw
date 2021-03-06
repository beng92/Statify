from tkinter import *
from StatifyStats import *
from libs.ttkcalendar import *
from libs.DateTimeDialog import *
from urllib import *
import webbrowser, logging

class StatifyGUI:
    def __init__(self):
        root = Tk()
        root.wm_title("Statify")
        root.iconbitmap('icons/statify.ico')
        logging.basicConfig(filename="debug.log", filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s > %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        ss = StatifyStats()
        
        
        topFrame = Frame(root)
        mainFrame = Frame(root)
        bottomFrame = Frame(root)
        
        ss.load(None, None)
        logging.info("Loaded songs")
        global startdate, enddate, labels
        startdate = ss.firstdate
        enddate = ss.enddate
        labels = {}
        
        startL = Label(topFrame,text=startdate)
        endL = Label(topFrame,text=enddate)
        
        def startcal():
            """Creates a datetime picker for the start of the range
            """
            global startdate
            result = DateTimeDialog(root, "Set Start", "icons/statify.ico").result
            if(result != None):
                startdate = result
                startL.config(text=startdate)
                logging.info("Set start date: " + str(startdate))
        def endcal():
            """Creates a datetime picker for the end of the range.
            """
            global enddate
            result = DateTimeDialog(root, "Set End", "icons/statify.ico").result
            if(result != None):
                enddate = result
                endL.config(text=enddate)
                logging.info("Set end date: " + str(enddate))
            

        startB = Tkinter.Button(topFrame, text="Start", command=startcal)
        endB = Tkinter.Button(topFrame, text="End", command=endcal)
        startB.pack(side=LEFT)
        startL.pack(side=LEFT)
        endB.pack(side=LEFT)
        endL.pack(side=LEFT)
        
            
        def reload(): 
            """Reload data and stats.
            """
            logging.info("Reloading")
            ss.load(startdate, enddate)
                
            
            for child in mainFrame.winfo_children():
                child.destroy()
                
            row = 0
            l1 = Label(mainFrame,text="Plays")
            r1 = Label(mainFrame,text=ss.plays())
            l1.grid(column=0, row=row, sticky=W)
            r1.grid(column=1, row=row, sticky=W)
            row += 1
            
            l2 = Label(mainFrame,text="Unique Songs")
            r2 = Label(mainFrame,text=ss.uniquePlays())
            l2.grid(column=0, row=row, sticky=W)
            r2.grid(column=1, row=row, sticky=W)
            row += 1
            
            l3 = Label(mainFrame,text="Artists")
            r3 = Label(mainFrame,text=ss.artists())
            l3.grid(column=0, row=row, sticky=W)
            r3.grid(column=1, row=row, sticky=W)
            row += 1
            
            l2 = Label(mainFrame,text="Average songs per day")
            r2 = Label(mainFrame,text=ss.playsPerDay())
            l2.grid(column=0, row=row, sticky=W)
            r2.grid(column=1, row=row, sticky=W)
            row += 1
            
            l4 = Label(mainFrame,text="Most Common Track")
            r4 = Button(mainFrame, text=ss.mcSong()[0], fg="blue", cursor="hand2", command=lambda: webbrowser.open_new(ss.mcSong()[1]))
            l4.grid(column=0, row=row, sticky=W)
            r4.grid(column=1, row=row, sticky=W)
            row += 1
            
            l5 = Label(mainFrame,text="Most Common Artist")
            r5 = Button(mainFrame, text=ss.mcArtist()[0], fg="blue", cursor="hand2", command=lambda: webbrowser.open_new(ss.mcArtist()[1]))
            l5.grid(column=0, row=row, sticky=W)
            r5.grid(column=1, row=row, sticky=W)
            row += 1
            
            l6 = Label(mainFrame,text="Listening Time")
            r6 = Label(mainFrame,text=ss.listenTime())
            l6.grid(column=0, row=row, sticky=W)
            r6.grid(column=1, row=row, sticky=W)
            row += 1
        
                   
        topFrame.pack()
        mainFrame.pack()
        bottomFrame.pack()
        reloadB = Button(bottomFrame, text="Reload", command=reload)
        reloadB.pack()
        reload()
        root.mainloop()
        

StatifyGUI()
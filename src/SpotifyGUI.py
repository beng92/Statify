from tkinter import *
from SpotifyStats import *

class SpotifyGUI:
    def __init__(self):

        root = Tk()
        ss = SpotifyStats()
        
        leftFrame = Frame(root)
        rightFrame = Frame(root)
        
        def write(function):
            textBox.delete('1.0', END)
            textBox.insert(INSERT, function())
        
            
            
        
        scroll = Scrollbar(rightFrame)    
        textBox = Text(rightFrame, height=16, width=60)
        scroll.config(command=textBox.yview)
        textBox.config(yscrollcommand=scroll.set)
        
        
        
        playsB = Button(leftFrame, text="Plays", command=lambda: write(ss.plays))
        artistsB = Button(leftFrame, text="Artists", command=lambda: write(ss.artists))
        uplaysB = Button(leftFrame, text="Unique Plays", command=lambda: write(ss.uniquePlays))
        mcsongB = Button(leftFrame, text="Most Common Song", command=lambda: write(ss.mcSong))
        mcartistB = Button(leftFrame, text="Most Common Artist", command=lambda: write(ss.mcArtist))
        listentimeB = Button(leftFrame, text="Listening Time", command=lambda: write(ss.listenTime))
        reloadB = Button(leftFrame, text="Reload Data", command=lambda: write(ss.load))
        buttons = [playsB, artistsB, uplaysB, mcsongB, mcartistB, listentimeB, reloadB]
        
        rightFrame.pack(side=RIGHT)
        leftFrame.pack(side=BOTTOM)
        for b in buttons:
            b.pack(fill=X, pady=5, padx=5)
        textBox.pack(side=LEFT, fill=Y)
        scroll.pack(side=RIGHT, fill=Y)
        
        ss.load()
        root.mainloop()
'''
        label = Label(veryTopFrame, text="Name:")
        name = Entry(veryTopFrame)
        text = Text(topFrame)
        text.config(state=DISABLED)
        entry = Entry(bottomFrame, text="Button 4",fg="purple")
        #entry.bind('<Return>', write)
        button = Button(bottomFrame, text="Send")
        #button.bind('<Button-1>',write)

        label.pack(side=LEFT)
        name.pack(side=LEFT)
        text.pack(side=LEFT)
        button.pack(side=RIGHT)
        entry.pack(side=BOTTOM)

        
        '''

SpotifyGUI()
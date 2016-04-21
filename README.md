# Statify
Spotify Listening Statistics - Simple live tracking of listening data and statistical analysis

###WARNING: This software is in ACTIVE development.
If you would like to get involved, start tracking your live listening statistics using the StatifyTracking.exe (Windows only) or StatifyTracking.pyw (Cross-Platform) 

[Screenshot](https://raw.githubusercontent.com/beng92/Statify/master/demo1.png)

[Get the tracking program here (.exe)](https://github.com/beng92/Statify/raw/master/src/StatifyTracking.exe)
.exe built by pyinstaller. It will create a folder called 'data' and a file called 'data.txt' where it will log the time and the artist and song based on the current Spotify Window title. Must be running at all times you plan to track listening, so create a shortcut and add it to your Start Menu StartUp folder so it always starts when you log onto the machine.

StatifyGUI.pyw will cache all requests to the Spotify servers to reduce load on their systems, storing the data produced in the same data folder as StatifyTracking.exe in a file called cache.xml. This is plain-text .xml file.

[Sample data can be downloaded](https://github.com/beng92/Statify/raw/master/src/data/data.txt) of my own listening data. Please don't judge!

Any questions, queries or well-wishes do not hesitate to contact me at ben [@] quelea.org
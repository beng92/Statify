import win32gui, time, os

track = win32gui.GetWindowText(win32gui.FindWindow('SpotifyMainWindow', None))
if not os.path.exists('data'):
    os.makedirs('data')
file = open('data/data.txt', 'a')
file.write(time.ctime() + ">" + track + '\n')
file.flush()
os.fsync(file.fileno())

while True:
    if (track == win32gui.GetWindowText(win32gui.FindWindow('SpotifyMainWindow', None))):
        pass
    else:
        track = win32gui.GetWindowText(win32gui.FindWindow('SpotifyMainWindow', None))
        if (track != ""):
            file.write(time.ctime() + ">" + track + '\n')
            file.flush()
            os.fsync(file.fileno())
    time.sleep(0.5)
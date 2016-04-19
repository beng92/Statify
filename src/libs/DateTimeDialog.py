import tkinter as Tkinter
import libs.ttkcalendar as ttkcalendar
import calendar, datetime

import libs.tkSimpleDialog as tkSimpleDialog


class DateTimeDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()
        
        self.date = Tkinter.Frame(master)
        self.spinboxH = Tkinter.Spinbox(self.date, from_=0, to=24, width=3, format="%02.0f", justify="right")
        self.spinboxH.pack(side=Tkinter.LEFT)
        self.label = Tkinter.Label(self.date, text=":")
        self.label.pack(side=Tkinter.LEFT)
        self.spinboxM = Tkinter.Spinbox(self.date, from_=0, to=60, width=3, format="%02.0f", justify="right")
        self.spinboxM.pack(side=Tkinter.LEFT)
        self.label = Tkinter.Label(self.date, text=":")
        self.label.pack(side=Tkinter.LEFT)
        self.spinboxS = Tkinter.Spinbox(self.date, from_=0, to=60, width=3, format="%02.0f", justify="right")
        self.spinboxS.pack(side=Tkinter.LEFT)
        
        self.date.pack()
        
        
    def apply(self):
        if(self.calendar.selection == None):
            self.result = None
        else:
            self.datetime = calendar.datetime.datetime
            hours = int(self.spinboxH.get()) if int(self.spinboxH.get()) < 24 and int(self.spinboxH.get()) >= 0 else 0
            minutes = int(self.spinboxM.get()) if int(self.spinboxM.get()) < 60 and int(self.spinboxM.get()) >= 0 else 0
            seconds = int(self.spinboxS.get()) if int(self.spinboxS.get()) < 60 and int(self.spinboxS.get()) >= 0 else 0
            self.result = self.datetime(self.calendar.selection.year, self.calendar.selection.month, self.calendar.selection.day, )
     
    def settoday(self):
        self.datetime = calendar.datetime.datetime
        self.result = self.datetime(self.calendar.today.year, self.calendar.today.month, self.calendar.today.day, self.datetime.now().hour, self.datetime.now().minute, self.datetime.now().second)
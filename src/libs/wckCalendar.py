#
# WCKLIB
# $Id$
#
# simple calendar widget
#
# history:
# 2007-09-22 fl   created
#
# Copyright (c) 2007 by Fredrik Lundh.  All rights reserved.
#
# See the README file for license details.
#

import calendar, datetime

from WCK import *

# FIXME: add keyboard navigation
# FIXME: turn shown date and selected date into properties (?)
# FIXME: add option for setting first day of week
# FIXME: add more styling options (?)

class CalendarController(Controller):

    def create(self, handle):
        handle("<Button-1>", self.handle_click)

    def handle_click(self, event):
        widget = event.widget
        widget.focus_set()
        widget.ui_handle_click(event.x, event.y)

##
# A simple calendar widget for WCK/Tkinter.

class Calendar(Widget):

    ui_option_font = FONT

    ui_option_foreground = FOREGROUND
    ui_option_background = BACKGROUND

    ui_option_selectbackground = SELECTBACKGROUND
    ui_option_selectforeground = SELECTFOREGROUND

    ui_option_borderwidth = 2
    ui_option_relief = "sunken"

    # called when the selection is changed
    ui_option_command = None

    ui_controller = CalendarController

    def __init__(self, master, **options):
        self.calendar = calendar.Calendar()
        self.weekdays = calendar.day_name
        self.calendar_date = datetime.date.today()
        self.selection = self.calendar_date
        # FIXME: add option for setting first day of week
        self.ui_init(master, options)

    def ui_handle_config(self):
        self.font = self.ui_font(
            self.ui_option_foreground, self.ui_option_font)
        w, h = self.font.measure("0")
        return (w * (2*7 + 6) + 4, h * 8 + 4)

    def ui_handle_repair(self, draw, x0, y0, x1, y1):
        w, h = self.font.measure("0")
        year = self.calendar_date.year
        month = self.calendar_date.month
        # header
        x = y = 2
        title = self.calendar_date.strftime("%B %Y")
        draw.text((x, y), title, self.font)
        y += h
        for day in self.weekdays:
            draw.text((x, y), day[:1], self.font)
            x += 3*w
        y += h
        # calender body
        for week in self.calendar.monthdatescalendar(year, month):
            x = 2
            for day in week:
                if day.month == self.calendar_date.month:
                    if day == self.selection:
                        draw.rectangle(
                            (x-1, y-1, x+2*w+1, y+h+1),
                            self.ui_brush(self.ui_option_selectbackground))
                        draw.text(
                            (x, y), str(day.day),
                            self.ui_font(self.ui_option_selectforeground,
                                         self.ui_option_font))
                    else:
                        draw.text((x, y), str(day.day), self.font)
                x += 3*w
            y += h

    def ui_handle_click(self, x, y):
        w, h = self.font.measure("0")
        x = (x - 2) / (w*3)
        y = (y - 2) / h - 2
        if x < 0 or y < 0:
            return
        year = self.calendar_date.year
        month = self.calendar_date.month
        data = self.calendar.monthdatescalendar(year, month)
        try:
            date = data[y][x]
        except IndexError:
            return
        if date.month != month:
            return
        self.selection = date
        self.ui_damage()
        if callable(self.ui_option_command):
            self.ui_option_command()

    # ----------------------------------------------------------------
    # model api

    ##
    # Gets the selected year and month, as a datetime.date object (the
    # day should be ignored).

    def getselection(self):
        return self.selection

    ##
    # Sets the selected year and month.

    def setselection(self, date):
        if self.selection != date:
            self.selection = date
            self.ui_damage()
        # FIXME: update viewed date as well?

    ##
    # Gets the year and month, as a datetime.date object (the day should
    # be ignored).

    def getdate(self):
        return self.calendar_date

    ##
    # Sets the year and month.  You can pass in either a datetime.date
    # object (the day will be ignored), or the year and month separately.

    def setdate(self, year, month=None):
        if isinstance(year, datetime.date):
            date = year
        else:
            date = datetime.date(year, month, 1)
        if self.calendar_date != date:
            self.calendar_date = date
            self.ui_damage()

# --------------------------------------------------------------------
# test/demo stuff

def demo():

    from Tkinter import Tk, Frame, Button, BOTH, LEFT

    root = Tk()
    root.title("wckCalendar")

    def echo():
        print (view.getselection())

    view = Calendar(root, font="verdana", background="white", command=echo)
    view.pack(fill=BOTH, expand=1)

    buttonbox = Frame(root)
    def previous():
        date = view.getdate()
        if date.month == 1:
            view.setdate(date.year-1, 12)
        else:
            view.setdate(date.year, date.month-1)
    def next():
        date = view.getdate()
        if date.month == 12:
            view.setdate(date.year+1, 1)
        else:
            view.setdate(date.year, date.month+1)
    b = Button(buttonbox, text="previous", command=previous, width=10)
    b.pack(side=LEFT)
    b = Button(buttonbox, text="next", command=next, width=10)
    b.pack(side=LEFT)
    buttonbox.pack(expand=1, padx=2, pady=2)

    root.mainloop()

if __name__ == "__main__":
    demo()

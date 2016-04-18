
import calendar
import tkinter as tk
import datetime

class Data:
    def __init__(self):
        self.day_selected = 0
        self.month_selected = 0
        self.year_selected = 0
        self.day_name = 0

class Calendar:
    def __init__(self, parent, data):
        self.data = data
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = 2013
        self.month = 7
        self.wid = []
        self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
        
        self.setup(self.year, self.month)
        
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            #w.destroy()
            self.wid.remove(w)
    
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)

    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
        
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)
        
    def selection(self, day, name):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name
        
        self.data.day_selected = day
        self.data.month_selected = self.month
        self.data.year_selected = self.year
        self.data.day_name = name
        
        #self.selected = day
        self.clear()
        self.setup(self.year, self.month)
        
    def setup(self, y, m):
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)
        
        header = tk.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)
        
        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)
        
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num)
        
        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    #print(calendar.day_name[day])
                    b = tk.Button(self.parent, width=1, text=day, command=lambda day=day:self.selection(day, calendar.day_name[(day-1) % 7]))
                    self.wid.append(b)
                    b.grid(row=w, column=d)
                    
        sel = tk.Label(self.parent, height=2, text='{} {} {} {}'.format(
            self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)
        
        ok = tk.Button(self.parent, width=5, text='OK', command='disabled')
        self.wid.append(ok)
        ok.grid(row=9, column=2, columnspan=3, pady=10)
        
def win(parent, d):
    win = tk.Toplevel(parent)
    cal = Calendar(win, d)

data = Data()
root = tk.Tk()
tk.Button(root, text='calendar', command=lambda:win(root, data)).grid()

root.mainloop()

print(data.__dict__)


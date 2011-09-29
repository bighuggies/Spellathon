'''
Created on 23/09/2011

@author: Andrew
'''
from Tkinter import *

class ScrollListbox(Frame):
    def __init__(self, master, items=None):
        self.items = items
        self.listbox = Listbox(self)
        
    def insert(self, name, item):
        self.items[name] = item
        
    def delete(self, name="", item=None):
        try:
            del self.items[name]
        except KeyError:
            for key, value in self.items.iteritems():
                if value == item:
                    del self.items[key]
                    
    def update(self):
        self.listbox.delete(first=0, last=END)
        self.listbox.insert(END, *sorted(self.items.keys()))
        
class LogonFields(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

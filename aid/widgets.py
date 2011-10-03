'''
Created on 23/09/2011

@author: Andrew
'''
from Tkinter import *
import os

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

class Dialog(Toplevel):
    def __init__(self, parent, title = None, btncolumn=100, btnrow=100):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)
            
        self.result = None
                    
        self.build()
        self.arrange()
        self.buttonbox(btncolumn, btnrow)

#        body.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")
        
        # Disable other windows
        self.grab_set()

        # Handle the window being closed by the window manager
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # Arrange the window relative to the parent
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        # Wait until the dialog is closed
        self.wait_window(self)

    #
    # construction hooks

    def build(self):
        # create dialog body.

        pass
    
    def arrange(self):
        # arrange widgets
        
        pass

    def buttonbox(self, btncolumn, btnrow):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.grid(column=0, row=0, padx=2, pady=2)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(column=1, row=0, padx=2, pady=2)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid(column=btncolumn, row=btnrow, sticky="se")

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override
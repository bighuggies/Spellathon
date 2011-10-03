'''
Created on 23/09/2011

@author: Andrew
'''
from Tkinter import *
import os

class TabBar(Frame):
    def __init__(self, master=None, tabs=None):
        Frame.__init__(self, master)
        
        
        self.tabs = tabs
        self.tab_var = StringVar()
        
        self.tab_var.set(self.tabs.keys()[0])
        
        self.tab_buttons = []
        
        self.build()
        self.arrange()
        self.switch_tab()
        
    def build(self):
        self.tab_frame = Frame(self)
        
        for name in self.tabs.iterkeys():
            self.tab_buttons.append(Radiobutton(self.tab_frame, text=name,
                                                variable=self.tab_var,
                                                value=name, indicatoron=0,
                                                command = self.switch_tab))
        
    def arrange(self):
        self.tab_frame.grid(row=0, column=0)
        
        for i, button in enumerate(self.tab_buttons):
            button.grid(column=i, row=0)
            
    def switch_tab(self):
        newtab = self.tab_var.get()
        
        for tab in self.tabs.itervalues():
            tab.grid_forget()
            
        self.tabs[newtab].grid(column=0,row=1)

class MultiScrollListbox(Frame):
    def __init__(self, master=None, items=None):
        Frame.__init__(self, master)
        self.listboxes=[]
        self.curselection = None
        
        if items:
            self.items = items        
            self.build()
            self.arrange()
            self.bind()
            self.update()
        
    def build(self):
        self.scrollbar = Scrollbar(self, orient=VERTICAL)            
        
        for i in range(0, len(self.items[0])):
            self.listboxes.append(Listbox(self, yscrollcommand=self.scrollbar.set,
                                  selectmode="single", borderwidth=0, 
                                  selectborderwidth=0, exportselection=0))

        self.scrollbar.config(command=self.on_vertical_scrollbar)
        
    def arrange(self):
        for listbox in self.listboxes:
            listbox.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar.pack(side=RIGHT, fill=Y)

    def bind(self):
        for listbox in self.listboxes:
            listbox.bind("<MouseWheel>", self.on_mwheel)
            listbox.bind("<Button-4>", self.on_mwheel)
            listbox.bind("<Button-5>", self.on_mwheel)
            listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

                            
    def on_vertical_scrollbar(self, *args):
        for listbox in self.listboxes:
            apply(listbox.yview, args)
            
    def on_mwheel(self, event):
        if (event.num == 4):    # Linux encodes wheel as 'buttons' 4 and 5
            delta = -1
        elif (event.num == 5):
            delta = 1
        else:                   # Windows & OSX
            delta = event.delta
        for lb in self.listboxes:
            lb.yview("scroll", delta, "units")
            
        return "break"
    
    def on_listbox_select(self, event):
        lindex = int(event.widget.curselection()[0])
        
        for listbox in self.listboxes:
            listbox.selection_clear(0, END)
            listbox.selection_set(lindex)

        self.curselection = (self.listboxes[0].get(lindex))
            
    def update(self):
        for i in range(len(self.listboxes)):
            self.listboxes[i].delete(first=0, last=END)

            for item in self.items:
                lol = list(item)
                self.listboxes[i].insert(END, lol[i])

class ScrollListbox(Frame):
    def __init__(self, master, items=None):
        Frame.__init__(self, master)
        
        if items:
            self.items = items
        else:
            self.items = {}
            
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.listbox = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        
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
        self.resizable(False, False)

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
        w.grid(column=0, row=0, padx=5, pady=2)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(column=1, row=0, padx=5, pady=2)

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
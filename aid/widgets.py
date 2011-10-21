'''
Module for custom Tkinter widgets.

Exported classes:

DateEntry -- A group of combo boxes for taking day/month/year input.
TabBar -- Tabs that let the user switch between multiple views in one window.
MultiScrollListbox -- A multi-columned scrollable listbox.
ScrollListbox -- A single column scrollable listbox.
Dialog -- A toplevel window for taking user input and validating it.

'''
from Tkinter import *
import datetime
import tkMessageBox

class DateEntry(Frame):
    '''A group of combo boxes for taking day/month/year input.
    
    Public functions:
    get -- Returns the date selected by the user.
    
    '''
    def __init__(self, master=None):
        '''Build and arrange the component widgets.'''
        Frame.__init__(self, master)
        
        # The default date is the earliest possible one.
        self.defaults = [1, 1, 1970]
        # Create a date object in order to check whether or not the date is
        # valid.
        self.date = datetime.date(self.defaults[2], self.defaults[1], self.defaults[0])
        
        self._build()
        self._arrange()
        
    def _build(self):
        '''Create the widgets and variables to trace date selections.'''
        self.day_lbl = Label(self, text='Day:')
        self.month_lbl = Label(self, text='Month:')
        self.year_lbl = Label(self, text='Year:')
        
        self.day_var = IntVar()
        self.month_var = IntVar()
        self.year_var = IntVar()
        
        self.vars = [self.day_var, self.month_var, self.year_var]

        for i, var in enumerate(self.vars):
            var.set(self.defaults[i])
            var.trace('w', self._validate)
        
        days = []
        months = []
        years = []
        
        for i in range(1,32):
            days.append(i)
            
        for i in range(1,13):
            months.append(i)
            
        for i in range(1970, 2012):
            years.append(i)
        
        self.day_opt = OptionMenu(self, self.day_var, *days)
        self.month_opt = OptionMenu(self, self.month_var, *months)
        self.year_opt = OptionMenu(self, self.year_var, *years)
        
        self.widgets = [self.day_lbl, self.day_opt, self.month_lbl, self.month_opt,
                   self.year_lbl, self.year_opt]
        
    def _arrange(self):
        '''Place the widgets in the frame.'''
        for i, w in enumerate(self.widgets):
            w.grid(column=i, row=0, padx=2, pady=2, sticky='we')
            
    def get(self):
        '''Return the currently selected date.'''
        return self.date
        
    def _validate(self, *args):
        '''Check if the selected date is a valid one.'''
        try:
            # Try and create a date object from the inputs. If an exception is
            # thrown, the date is not valid.
            self.date = datetime.date(self.year_var.get(), self.month_var.get(), self.day_var.get())
        except ValueError:
            tkMessageBox.showerror('Date error', 'Please enter a valid date!')
            for i, var in enumerate(self.vars):
                var.set(self.defaults[i])

class TabBar(Frame):
    '''Tabs that let the user switch between multiple views in one window.
    
    Public functions:
    switch_tab -- Switch the view to the one associated with the chosen tab.
    
    '''
    def __init__(self, master=None, tabs=None):
        '''Build and arrange the component widgets.
        
        Arguments:
        master -- The parent window.
        tabs -- A dictionary of name/frame value pairs.
        
        '''
        Frame.__init__(self, master)
        
        self.tabs = tabs
        self.tab_var = StringVar()
        
        self.tab_var.set(self.tabs.keys()[0])
        
        self.tab_buttons = []
        
        self._build()
        self._arrange()
        
        # Switch to the initial tab.
        self.switch_tab()
        
    def _build(self):
        '''Create the component widgets.'''
        self.tab_frame = Frame(self, relief=SUNKEN, padx=5, pady=5)
        
        # Create a tab button for each tab.
        for name in self.tabs.iterkeys():
            self.tab_buttons.append(Radiobutton(self.tab_frame, text=name,
                                                variable=self.tab_var,
                                                value=name, indicatoron=0,
                                                command = self.switch_tab,
                                                height=1, padx=5, pady=5))
        
    def _arrange(self):
        '''Arrange the tabs in the frame.'''
        self.tab_frame.grid(row=0, column=0, sticky="we")
        
        for i, button in enumerate(self.tab_buttons):
            button.grid(column=i, row=0, sticky="we", padx=2, pady=2)
            
    def switch_tab(self):
        '''Switch the view to the one associated with the chosen tab.'''
        # Get the selected tab.
        newtab = self.tab_var.get()
        
        # Stop displaying other tabs.
        for tab in self.tabs.itervalues():
            tab.grid_forget()
        
        # Display the chosen tab.
        self.tabs[newtab].grid(column=0,row=1)

class MultiScrollListbox(Frame):
    '''A multi-columned scrollable listbox.
    http://stackoverflow.com/questions/4066974/scrolling-multiple-tkinter-listboxes-together
    http://code.activestate.com/recipes/52266-multilistbox-tkinter-widget/
    
    Public functions:
    add_listener -- Add a listener to be notified of listbox selections.
    get -- Get the current listbox selection.
    update -- Update the listbox items.
    
    '''
    def __init__(self, master=None, items=None, headers=None):
        '''Create the multi column scrollable listbox widget.
        
        Arguments:
        master -- Parent window.
        items -- A list of tuples where each element of the list corresponds to
        an entry in the listbox and each element of the tuple corresponds to a
        column. Every entry must have the same number of elements.
        headers -- List of column headings.
        
        '''
        Frame.__init__(self, master)
        self.listboxes = []
        
        if headers:
            self.headers = headers
        else:
            self.headers = []
            
        self.curselection = None
        self.listeners = []
        self.header_frames = []
        
        if items:
            self.items = items        
            self._build()
            self._arrange()
            self._bindings()
            self.update()
        
    def _build(self):
        '''Create the component widgets.'''
        self.scrollbar = Scrollbar(self, orient=VERTICAL)            
        
        # Create x listboxes where x is the number of elements in each tuple of
        # the items list.
        for i in range(0, len(self.items[0])):
            self.listboxes.append(Listbox(self, yscrollcommand=self.scrollbar.set,
                                  selectmode='single', borderwidth=1, 
                                  selectborderwidth=0, exportselection=0))
        
        # Create the header for each column.
        for i, header in enumerate(self.headers):
            frame = Frame(self, relief=SUNKEN)
            label = Label(frame, text=header)
            label.grid()
            self.header_frames.append(frame)

        self.scrollbar.config(command=self._on_vertical_scrollbar)
        
    def _arrange(self):
        '''Arrange the component widgets.'''
        for i, header in enumerate(self.header_frames):
            header.grid(column=i, row=0, sticky="we")
            
        for i, listbox in enumerate(self.listboxes):
            listbox.grid(column=i, row=1, sticky="we")
            
        self.scrollbar.grid(column=100, row=1, sticky="ns")
        
    def _bindings(self):
        '''Bind the listbox to a set of events.'''
        for listbox in self.listboxes:
            # Listen for scrolling events so that the seperate listboxes can be
            # scrolled simultaneously.
            listbox.bind('<MouseWheel>', self._on_mwheel)
            listbox.bind('<Button-4>', self._on_mwheel)
            listbox.bind('<Button-5>', self._on_mwheel)
            # Let the widget keep track of selection events.
            listbox.bind('<<ListboxSelect>>', self._on_listbox_select)
                     
    def _on_vertical_scrollbar(self, *args):
        '''Let the scrollbar effect every listbox.'''
        for listbox in self.listboxes:
            apply(listbox.yview, args)
            
    def _on_mwheel(self, event):
        '''When the mousewheel is scrolled, all listboxes are scrolled
        together.'''
        if (event.num == 4):    # Linux encodes wheel as 'buttons' 4 and 5.
            delta = -1
        elif (event.num == 5):
            delta = 1
        else:                   # Windows & OSX.
            delta = event.delta
        for lb in self.listboxes:
            lb.yview('scroll', delta, 'units')
            
        return 'break' # Cancel the original scroll.
    
    def _on_listbox_select(self, event):
        '''React to listbox selection events.'''
        # Get the current selection and update the current selection.
        try:
            lindex = int(event.widget.curselection()[0])
        except IndexError:
            lindex = 0
            
        self._update_selection(lindex)
                
    def _update_selection(self, lindex=0):
        '''When a selection is made in a listbox, apply that selection to
        all of the listboxes in the multi listbox widget.
        
        Arguments:
        lindex -- The list index of the selection.
        
        '''
        try:
            for listbox in self.listboxes:
                listbox.selection_clear(0, END)
                listbox.selection_set(lindex)
                
            self.curselection = (self.listboxes[0].get(lindex))

        except IndexError:
            # If the listboxes are empty, then the curselection is none.
            self.curselection = None
        
        # Notify listeners of selection.
        if self.listeners:
            for listener in self.listeners:
                listener.listbox_select(self.curselection, index=lindex)        
    def add_listener(self, listener):
        '''Add a listener to be notified of listbox selection events.
        
        Arguments:
        listener -- The object to be notified of listbox selection events.
        
        '''
        self.listeners.append(listener)
        
    def get(self):
        '''Return the current listbox selection (the string in the first column
        of the entry).'''
        return self.curselection
            
    def update(self):
        '''Populate the listboxes.'''
        for i in range(len(self.listboxes)):
            self.listboxes[i].delete(first=0, last=END)

            for item in self.items:
                l = list(item)
                self.listboxes[i].insert(END, l[i])
        
        # Make sure that if the listbox is now empty, the curselection is set
        # to none. Otherwise, select the first item in the updated list.
        self._update_selection()
                                
class ScrollListbox(Frame):
    '''A single column scrollable listbox.
    
    Public functions:
    insert -- Add an entry to the listbox.
    delete -- Remove an entry from the listbox.
    update -- Update the entries in the listbox.
    add_listener -- Add a listener to be notified of listbox selection events.
    
    '''
    def __init__(self, master, items=None):
        '''Create and arrange the component widgets.
        
        Arguments:
        master -- Parent window.
        items -- Name/object pairs where the names will be entries in the
        listbox and the objects will be the related items.
        
        '''
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
        
        self.listbox.bind('<<ListboxSelect>>', self._on_listbox_select)
        self.listeners = []
        self.curselection = None
    
    def _on_listbox_select(self, event):
        ''''Set the current selection on a selection event and notify subscribed
        listeners.'''
        # Get the selected entry from the listbox.
        lindex = int(event.widget.curselection()[0])
        self.curselection = (self.listbox.get(lindex))
        
        # Send a message to each listener containing the name of the entry and
        # the related object.
        if self.listeners:
            for listener in self.listeners:
                listener.listbox_select(self.curselection,
                                        self.items[self.curselection])
    
    def insert(self, name, item):
        '''Add a new entry.
        
        Arguments:
        name -- Name of the entry.
        item -- Object associated with the entry.
        
        '''
        self.items[name] = item
        self.update()
        
    def delete(self, name='', item=None):
        '''Delete an entry either by name or by the associated object.
        
        Arguments
        name -- Name of the entry to delete.
        item -- Object to delete.
        
        '''
        try:
            # Try and delete by the name.
            del self.items[name]
        except KeyError:
            # If that fails, try and delete by the item.
            for key, value in self.items.iteritems():
                if value == item:
                    del self.items[key]
        
        # Update the entries.          
        self.update()
                    
    def update(self):
        '''Update the entries in the listbox.'''
        self.listbox.delete(first=0, last=END)
        self.listbox.insert(END, *sorted(self.items.keys()))
        
    def add_listener(self, listener):
        '''Add a listener to be notified of listbox selection events.
        
        Arguments:
        listener -- The object to be notified of listbox selections.
        
        '''
        self.listeners.append(listener)
        
class Dialog(Toplevel):
    '''A toplevel window for taking user input and validating it.
    http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    
    Public functions:
    ok -- Confirm the dialog.
    cancel -- Cancel the dialog.
    
    '''
    def __init__(self, master, title=None, btncolumn=100, btnrow=100):
        '''Create the dialog.
        
        Arguments:
        master -- Parent window.
        title -- Title of the dialog window.
        btncolumn -- The column where the ok and cancel buttons should be
        placed.
        btnrow -- The row where the ok and cancel buttons should be placed.
        
        '''
        Toplevel.__init__(self, master)
        self.transient(master)
        self.resizable(False, False)

        if title:
            self.title(title)
            
        self.result = None
        
        self._build()
        self._arrange()
        self._buttonbox(btncolumn, btnrow)

#        body.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')
        
        # Disable other windows
        self.grab_set()

        # Handle the window being closed by the window manager
        self.protocol('WM_DELETE_WINDOW', self.cancel)

        # Arrange the window relative to the master
        self.geometry('+%d+%d' % (master.winfo_rootx()+50,
                                  master.winfo_rooty()+50))

        # Wait until the dialog is closed
        self.wait_window(self)

    #
    # construction hooks

    def _build(self):
        '''Create dialog body.'''
        # override
        pass
    
    def _arrange(self):
        '''Arrange dialog widgets.'''
        # override
        pass

    def _buttonbox(self, btncolumn, btnrow):
        '''Add standard button box. override if you don't want the
        standard buttons.'''

        box = Frame(self)

        w = Button(box, text='OK', width=10, command=self.ok, default=ACTIVE)
        w.grid(column=0, row=0, padx=5, pady=2)
        w = Button(box, text='Cancel', width=10, command=self.cancel)
        w.grid(column=1, row=0, padx=5, pady=2)

        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)

        box.grid(column=btncolumn, row=btnrow, sticky='se')

    def _validate(self):
        '''Check if the input if valid.'''
        # override
        return 1

    def _apply(self):
        '''Apply changes.'''
        # override
        pass 
    
    def ok(self, event=None):
        '''Confirm the dialog.'''
        if not self._validate():
            return

        self.withdraw()
        self.update_idletasks()

        self._apply()

        self.cancel()

    def cancel(self, event=None):
        '''Cancel the dialog.'''
        # put focus back to the master window
        self.master.focus_set()
        self.destroy()
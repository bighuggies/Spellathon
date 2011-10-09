'''
Module to _build each view and manage behaviour of the Spellathon application.

Exported classes:

UserListModel -- Model to keep track of the users in the user management view.
WordDestinationModel -- Model to keep track of the destination list in the list
edit view.
WordSourceModel -- Model to keep track of the source words list in the list edit
view.
TLDROptionMenuModel -- Model to keep track of the tldr items in an OptionMenu.
TLDRMultiScrollListbox -- Model to keep track of the list items in the multi
column list widget in the list management view.

'''
from Tkinter import *
import shutil
import os
import tkMessageBox
import tools.tldr as tldr
import tools.database as db

class UserListModel(object):
    '''Model to keep track of the users in the user management view.
    
    Public functions:
    update_items -- Get the users from the database and display them in the
    listbox.
    delete_user -- Remove a user from the list.
    listbox_select -- React to a user being selected in the listbox.
    
    '''
    def __init__(self, listbox):
        '''Create the user model.
        
        Arguments:
        listbox -- The multi column listbox of the view containing the list of
        users.
        
        '''
        self.listbox = listbox
        # Listen for selection events from the listbox.
        self.listbox.add_listener(self)
        self.user = None
        
        self.um = db.get_user_manager()
        self.users = self.um.retrieve_users()
        
        # Populate the listbox.
        self.update_items()

    def update_items(self):
        '''Get the users from the database and display them in the listbox.'''
        items = []
        users = self.um.retrieve_users()
        
        # Build the list of tuples containing user information to pass to the
        # listbox.
        for user in users:
            items.append((user.username, user.realname, user.dob))
        
        # Set the listbox items to the built list of users.
        self.listbox.items = sorted(items)
        # Tell the listbox to update itself.
        self.listbox.update()
        
    def delete_user(self):
        '''Remove the selected user from the list.'''
        if tkMessageBox.askokcancel('Delete user', 'Delete the selected user?'):
            self.um.remove_user(self.listbox.get())
            self.update_items()
            self.um.commit()
            
    def listbox_select(self, selection, index):
        '''When a user is selected, set that user as the current focus of the
        model.'''
        self.user = self.users[index]

class WordDestinationModel(object):
    '''Model to keep track of the destination list in the list
    edit view.
    
    Public functions:
    listbox_select -- Update the view's word metadata when a word is selected.
    add_word -- Add a word to the list.
    add_words -- Add a bunch of words to the list.
    remove_word -- Remove the currently selected word from the list.
    remove_all_words -- Remove all the words from the list.
    save -- Write all the words in the list to disk, creating a new tldr file.
    filter_listbox -- Update the list to show words that match the filter.
    
    '''
    def __init__(self, interface, listname, listbox, filter, filtervar):
        '''Create the word destination model.
        
        Arguments:
        interface -- The frame that the widgets are shown on.
        listname -- The name of the list being edited.
        listbox -- The listbox that shows the words currently in the list.
        filter -- The entry box where the filter is input.
        filtervar -- The string variable which keeps track of the filter input.
        
        '''
        self.interface = interface
        self.listname = listname
        self.listbox = listbox
        self.filter = filter
        self.filtervar = filtervar
        
        self.listbox.add_listener(self)
        
        # Get the words currently in the list by parsing the tldr.
        self.wordlist = tldr.parse_tldr('wordlists/' + listname + '.tldr',
                                        listname)
        # Keep track of the filter.
        self.filtervar.trace('w', self.filter_listbox)
        
        self.listbox.items = self.wordlist.words
        self.listbox.update()
                
    def listbox_select(self, string, word):
        '''Update the view's word metadata when a word is selected.'''
        self.interface.update_metadata(word)
        
    def add_word(self, word):
        '''Add a word to the list.'''
        self.wordlist.add_word(word)
        # Update the list of words according to the filter.
        self.filter_listbox()
        
    def add_words(self, words):
        '''Add a bunch of words to the list.'''
        self.wordlist.words = dict(words.items() + self.wordlist.words.items())
        # Update the list of words according to the filter.
        self.filter_listbox()
            
    def remove_word(self, word):
        '''Remove a word from the list.'''
        self.wordlist.del_word(word)
        self.listbox.delete(word)
        self.interface.reset_metadata()
        
    def remove_all_words(self):
        '''Remove all words from the list.'''
        # Only remove those words which are currently visible in the list.
        for word in self.listbox.items.keys():
            self.wordlist.del_word(word)
            
        self.listbox.items = self.wordlist.words
        self.filter_listbox()
        self.interface.reset_metadata()
        
    def save(self):
        '''Write all the words in the list to disk, creating a new tldr file.'''
        tldr.generate_tldr(self.wordlist, 'wordlists/' + self.wordlist.name + 
                           '.tldr')
    
    def filter_listbox(self, *args):
        '''Update the listbox to show only words which match the user's
        filter.'''
        self.listbox.items = {}
        
        for key, value in self.wordlist.words.iteritems():
            if not key.lower().find(self.filtervar.get().lower()):
                self.listbox.items[key] = value                
        
        self.listbox.update()
        
class WordSourceModel(object):
    '''Model to keep track of the source words list in the list edit
    view.

    Public functions:
    source_chosen -- React to a source list being chosen from the source
    combobox.
    filter_listbox -- Update list to display only words which match the filter.
    listbox_select -- When a word is selected from the list, update the word
    metadata in the view.
    get_word -- Get the currently selected word.
    get_words -- Get all of the words currently in the source list.
    
    '''
    def __init__(self, interface, optionmenu, optionmenuvar, listbox, filter, filtervar):
        '''Create the word source model.
        
        Arguments:
        interface -- Interface that the source list is displayed on.
        optionmenu -- Option menu containing the entries of all the sources.
        optionmenuvar -- StringVar which tracks the optionmeny choice.
        listbox -- Listbox which displays all the words in the currently
        selected source.
        filter -- Entry box where the user enters the filter.
        filtervar -- StringVar which keeps track of what is entered in the
        filter. 
        
        '''
        self.interface = interface
        self.optionmenu = optionmenu
        self.optionmenuvar = optionmenuvar
        self.listbox = listbox
        self.filter = filter
        self.filtervar = filtervar
        self.items = {}
        self.word = None
        
        self.optionmenuvar.trace('w', self.source_chosen)
        self.filtervar.trace('w', self.filter_listbox)
        self.wm = db.get_word_manager()
        
        self.listbox.add_listener(self)
            
    def source_chosen(self, *args):
        ''' When a source is chosen from the option menu, update the list of
        words accordingly.'''
        # Retrieve the words from the database.
        words = self.wm.retrieve_words_of_difficulty(self.optionmenuvar.get())
        
        for word in words:
            self.items[word.word] = word
        
        # Add all the words to the listbox and update the display.
        self.listbox.items = self.items
        self.listbox.update()
        
    def filter_listbox(self, *args):
        '''Update the listbox to show only words which match the user's
        filter.'''
        self.listbox.items = {}
        
        for key, value in self.items.iteritems():
            if not key.lower().find(self.filtervar.get().lower()):
                self.listbox.items[key] = value                
        
        self.listbox.update()
        
    def listbox_select(self, string, word):
        '''When a word is selected from the source listbox, update the word
        metadata panel.'''
        self.word = word
        self.interface.update_metadata(word)
        
    def get_word(self):
        '''Get the currently selected word.'''
        return self.word
    
    def get_words(self):
        '''Get the currently visible list items.'''
        return self.listbox.items

class TLDROptionMenuModel(object):
    '''Model to keep track of the tldr items in an OptionMenu.

    Public functions:
    update_entries -- Add an entry to the option menu for each tldr file.
    get_list_name -- Return the name of the currently selected list.
    get_list -- Return the WordList object of the currently selected list.
    
    '''
    def __init__(self, optionmenu, optionmenuvar):
        '''Create the TLDROptionMenuModel
        
        Arguments:
        optionmenu -- The option menu which will contain the entries.
        optionmenuvar -- The StringVar to keep track of the selected entry.
        
        '''
        self.optionmenu = optionmenu
        self.optionmenuvar = optionmenuvar
        # Get all of the wordlists in the wordlists folder.
        self.wordlists = tldr.parse_tldr_files('wordlists/')
        
        # Populate the option menu.
        self.update_entries()
    
    def update_entries(self):
        '''Add an entry to the option menu for each tldr file.'''
        self.optionmenu['menu'].delete(0, END)
        
        if self.wordlists:
            for i in sorted(self.wordlists.keys()):
                self.optionmenu['menu'].add_command(label=i, command=lambda temp = i: self.optionmenu.setvar(self.optionmenu.cget('textvariable'), value = temp))
            
            self.optionmenuvar.set(sorted(self.wordlists.keys())[0])
        else:
            self.optionmenuvar.set("")
        
    def get_list_name(self):
        '''Return the name of the currently selected list.'''
        return self.optionmenuvar.get()
    
    def get_list(self):
        '''Return the WordList object of the currently selected list.'''
        if self.optionmenuvar.get() != "":
            return self.wordlists[self.optionmenuvar.get()]
        else:
            return None
        
class TLDRMultiScrollListbox(object):
    '''Model to keep track of the list items in the multi
    column list widget in the list management view.
    
    Public functions:
    update_items -- Parse each tldr file and display an entry for it.
    import_list -- Import a tldr file from outside the application.
    delete -- Delete a tldr file.
    
    '''
    def __init__(self, listbox):
        '''Create the model.
        
        Arguments:
        listbox -- The multi column listbox widget in which to display the tldr
        entries.
        
        '''
        self.listbox = listbox
        self.wordlists = tldr.parse_tldr_files('wordlists/')
        
        # Populate the listbox.
        self.update_items()
        
    def update_items(self):
        '''Parse each tldr file and display an entry for it.'''
        items = []
        self.wordlists = tldr.parse_tldr_files('wordlists/')
        
        # Build the list of tuples to pass to the multi column listbox widget.
        for wordlist in self.wordlists.values():
            items.append((wordlist.name, wordlist.source, wordlist.date_edited, str(len(wordlist.words))))
            
        self.listbox.items = sorted(items)
        self.listbox.update()
        
    def import_list(self, listfile):
        '''Import a tldr file from outside the application.'''
        try:
            # Move the list to the spellingaid directory
            shutil.copy(listfile, 'wordlists/')
            # Add the list
            self.update_items()
        except Exception:
            tkMessageBox.showerror('Error', 'Either no file was selected or that list already exists.')
        
    def delete(self):
        '''Delete a tldr file.'''
        tldr = self.listbox.get()
        
        if tldr:
            # Move the selected tldr file to the trash.
            try:
                shutil.move('wordlists/' + tldr + '.tldr', 'trash/' + tldr + '.tldr')
            except IOError:
                os.mkdir('trash')
                shutil.copy('wordlists/' + tldr + '.tldr', 'trash/' + tldr + '.tldr')
        else:
            tkMessageBox.showerror('Error', 'No list selected.')
        
        self.update_items()
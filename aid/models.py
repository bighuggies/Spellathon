'''
Created on 5/10/2011

@author: andrew
'''
from Tkinter import *
import shutil
import os
import tkMessageBox
import tools.tldr as tldr
import aid.database as db

class WordDestinationModel(object):
    def __init__(self, interface, listname, listbox, filter, filtervar):
        self.interface = interface
        self.listname = listname
        self.listbox = listbox
        self.filter = filter
        self.filtervar = filtervar
        
        self.listbox.add_listener(self)
        
        self.wordlist = tldr.parse_tldr('wordlists/' + listname + '.tldr', listname)
                
        self.listbox.items = self.wordlist.words
        self.listbox.update
        
    def listbox_select(self, string, word):
        self.interface.update_metadata(word)
        
class WordSourceModel(object):
    def __init__(self, interface, optionmenu, optionmenuvar, listbox, filter, filtervar):
        self.interface = interface
        self.optionmenu = optionmenu
        self.optionmenuvar = optionmenuvar
        self.listbox = listbox
        self.filter = filter
        self.filtervar = filtervar
        self.items = {}
        
        self.optionmenuvar.trace('w', self.source_chosen)
        self.filtervar.trace('w', self.filter_listbox)
        self.wm = db.get_word_manager()
        
        self.listbox.add_listener(self)
            
    def source_chosen(self, *args):
        words = self.wm.retrieve_words_of_difficulty(self.optionmenuvar.get())
        
        for word in words:
            self.items[word.word] = word
            
        self.listbox.items = self.items
        self.listbox.update()
        
    def filter_listbox(self, *args):
        self.listbox.items = {}
        
        for key, value in self.items.iteritems():
            if not key.lower().find(self.filtervar.get().lower()):
                self.listbox.items[key] = value                
        
        self.listbox.update()
        
    def listbox_select(self, string, word):
        self.interface.update_metadata(word)


class ListEditModel(object):
    def __init__(self):
        a=0

class TLDROptionMenuModel(object):
    def __init__(self, optionmenu, optionmenuvar):
        self.optionmenu = optionmenu
        self.optionmenuvar = optionmenuvar
        self.wordlists = tldr.parse_tldr_files('wordlists/')
                
        self.update_entries()
    
    def update_entries(self):
        self.optionmenu['menu'].delete(0, END)

        for i in sorted(self.wordlists.keys()):
            self.optionmenu['menu'].add_command(label=i, command=lambda temp = i: self.optionmenu.setvar(self.optionmenu.cget('textvariable'), value = temp))
        
        self.optionmenuvar.set(sorted(self.wordlists.keys())[0])
        
    def get_list_name(self):
        return self.optionmenuvar.get()
    
    def get_list(self):
        return self.wordlists[self.optionmenuvar.get()]
        
class TLDRMultiScrollListbox(object):
    def __init__(self, listbox):
        self.listbox = listbox
        self.wordlists = tldr.parse_tldr_files('wordlists/')
        
        self.update_items()
        
    def update_items(self):
        items = []
        self.wordlists = tldr.parse_tldr_files('wordlists/')
        
        for wordlist in self.wordlists.values():
            items.append((wordlist.name, wordlist.source, wordlist.date_edited, str(len(wordlist.words))))
            
        self.listbox.items = sorted(items)
        self.listbox.update()
        
    def import_list(self, listfile):
        
        try:
            # Move the list to the spellingaid directory
            shutil.copy(listfile, "wordlists/")
            # Add the list
            self.update_items()
        except Exception:
            tkMessageBox.showerror('Error', 'That list already exists.')
        
    def delete(self):
        tldr = self.listbox.get()
        
        del self.wordlists[tldr]
        
        try:
            shutil.copy('wordlists/' + tldr + '.tldr', 'trash/' + tldr + '.tldr')
        except IOError:
            os.mkdir('trash')
            shutil.copy('wordlists/' + tldr + '.tldr', 'trash/' + tldr + '.tldr')
            
        os.remove('wordlists/' + tldr + '.tldr')

        self.update_items()


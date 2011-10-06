'''
Created on 5/10/2011

@author: andrew
'''
import glob
from tools import tldr
from Tkinter import *

class TLDROptionMenuModel(object):
    def __init__(self, optionmenu, optionmenuvar):
        self.optionmenu = optionmenu
        self.optionmenuvar = optionmenuvar
        self.wordlists = self.parse_tldr_files()
        
        self.update_entries()
        
    
    def parse_tldr_files(self):
        tldrs = {}
        
        for t in glob.glob('wordlists/*.tldr'):
            tldrs[t[10:-5]] = tldr.parse_tldr(t, t[10:-5])

        return tldrs
    
    def update_entries(self):
        self.optionmenu['menu'].delete(0, END)

        for i in sorted(self.wordlists.keys()):
            self.optionmenu['menu'].add_command(label=i, command=lambda temp = i: self.optionmenu.setvar(self.optionmenu.cget('textvariable'), value = temp))
        
        self.optionmenuvar.set(sorted(self.wordlists.keys())[0])
        
    def get_list_name(self):
        return self.optionmenuvar.get()
    
    def get_list(self):
        return self.wordlists[self.optionmenuvar.get()]
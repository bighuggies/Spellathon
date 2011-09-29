'''
Created on Sep 29, 2011

@author: ahug048
'''
from Tkinter import *

class Logon(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.build()
        self.arrange()
        
    def build(self):
        self.username_lbl = Label(self, text="Username:")
        self.password_lbl = Label(self, text="Password:")
        
        self.username_ebx = Entry(self)
        self.password_ebx = Entry(self)
        
        
        self.buttonframe = Frame(self)
        
        self.userpw = [self.username_lbl, self.username_ebx, self.password_lbl, self.password_ebx, self.buttonframe]

        self.login_btn = Button(self.buttonframe, text="Login")
        self.new_user_btn = Button(self.buttonframe, text="New user")
        self.administrate_btn = Button(self.buttonframe, text="Administrate")
        
        self.buttons = [self.login_btn, self.new_user_btn, self.administrate_btn]
        
    def arrange(self):
        for i, widget in enumerate(self.userpw):
            widget.grid(column=0, row=i, padx=2, pady=2, sticky="WE")
            
        for i, widget in enumerate(self.buttons):
            widget.grid(column=i, row=0, padx=2, pady=2, sticky="WE")
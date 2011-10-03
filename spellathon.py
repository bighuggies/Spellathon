'''
Created on Sep 29, 2011

@author: ahug048
'''
from aid.views import *
from aid.widgets import *
from Tkinter import *

if __name__ == "__main__":
    root = Tk()
    
        
    logon = Logon(root)
    logon.grid(column=1, row=1)
    admin = Administration(root)
    wlcm = WelcomeScreen(root)
    score = Score(root, btncolumn=1)
    aid = SpellingAid(root)
    spc = SpellingComplete(root, btncolumn=0)
    reg = UserRegistration(root, btncolumn=0)
    auth = Authoriser(root, btncolumn=0)
    adm = CreateAdmin(root, btncolumn=0)

    root.mainloop()
'''
Created on Sep 29, 2011

@author: ahug048
'''
from aid.views import *
from aid.widgets import *
from Tkinter import *

if __name__ == "__main__":
    root = Tk()
    
    items = []
    
    for i in range(1,50):
        items.append((i, i, i))
        
    msl = MultiScrollListbox(root, items=items)
    msl.grid(sticky="nswe")
    
#    logon = Logon(root)
#    logon.grid(column=1, row=1)
#    wlcm = WelcomeScreen(root)
#    score = Score(root, btncolumn=1)
#    aid = SpellingAid(root)
#    spc = SpellingComplete(root, btncolumn=0)
#    reg = UserRegistration(root, btncolumn=0)
#    auth = Authoriser(root, btncolumn=0)
#    adm = CreateAdmin(root, btncolumn=0)

    root.mainloop()
'''
Created on Sep 29, 2011

@author: ahug048
'''
from aid.views import Logon, UserRegistration
from aid.widgets import Dialog
from Tkinter import *

if __name__ == "__main__":
    root = Tk()
    
    logon = Logon(root)
    logon.grid(column=1, row=1)
    reg = UserRegistration(root, btncolumn=1, btnrow=100)

    root.mainloop()
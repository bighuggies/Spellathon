'''
Created on Sep 29, 2011

@author: ahug048
'''
from aid.views import Logon
from Tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    root.wm_withdraw()
    logon = Logon(root)
    root.mainloop()
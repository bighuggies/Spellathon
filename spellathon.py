'''
Created on Sep 29, 2011

@author: ahug048
'''
from spellingaid.views import Logon
from Tkinter import *

if __name__ == "__main__":
    root = Tk()
    sa = Logon(root)
    sa.pack(fill=BOTH, expand=True)
    root.mainloop()
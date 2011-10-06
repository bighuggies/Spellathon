'''S    

Created on Sep 29, 2011

@author: ahug048
'''
from aid.views import Logon
from Tkinter import *
from aid.models import *

if __name__ == "__main__":
    root = Tk()
    root.wm_withdraw()
    logon = Logon(root)
    root.mainloop()

#    root = Tk()
#    
#    om_var = StringVar()
#    om = OptionMenu(root, om_var, "")
#    omm = TLDROptionMenuModel(om, om_var)
#    
#    om.pack()
#    
#    root.mainloop()
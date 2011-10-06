from aid.views import Logon
from Tkinter import *
from aid.models import *

if __name__ == "__main__":
    root = Tk()
    root.wm_withdraw()
    logon = Logon(root)
    root.mainloop()
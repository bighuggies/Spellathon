from aid.views import Logon
from Tkinter import *
from aid.models import *
import tkMessageBox

files = {'images' :['example.gif', 'go.gif', 'main.gif', 'score.gif', 'spbee.gif', 'speak.gif', 'stop.gif', 'submit.gif']}

if __name__ == '__main__':
    for image in files['images']:
        try:
            f = open('images/' + image, 'r')
            f.close()
        except IOError:
            tkMessageBox.showerror('Error', 'You are missing the file ' + image + '. Please reinstall.')
    
    root = Tk()
#    root.wm_withdraw()
    logon = Logon(root)
    logon.pack()
    root.mainloop()
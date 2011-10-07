from aid.views import Logon, FirstRun
from Tkinter import *
from aid.models import *
import subprocess
import tkMessageBox

# List of all the files necessary to run the program.
files = {'images' :['example.gif', 'go.gif', 'main.gif', 'score.gif',
                    'spbee.gif', 'speak.gif', 'stop.gif', 'submit.gif'], 'config': ['.config']}

def check_festival():
    '''
    Try run festival to check if it's installed. If not show an error and don't
    run the program.
    '''
    try:
        p = subprocess.Popen('festival', stdin=subprocess.PIPE)
        p.stdin.write('(SayText "Welcome to spell a thon!")')
        p.stdin.close()
    except OSError:
        tkMessageBox.showerror('Error', 'You do not have festival installed.' +
                               'Please install festival and launch again.')
        return False
    
    return True
    
def check_files():
    '''
    Check that all the necessary images exist in the images folder.
    '''
    
    for image in files['images']:
        try:
            f = open('images/' + image, 'r')
            f.close()
        except IOError:
            tkMessageBox.showerror('Error', 'You are missing the file ' +
                                   image + '. Please reinstall.')
            return False
        
    return True

if __name__ == '__main__':
    if check_files() and check_festival():
        # Create the widgets.
        root = Tk()
        root.resizable(False, False)
        logon = Logon(root)
        logon.pack()

#        if check_first_run():
##            fr = FirstRun(root, btncolumn=0)
##            fr.pack()
#        else:

        # Enter the mainloop and begin the program.
        root.mainloop()
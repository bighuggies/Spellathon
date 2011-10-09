from aid.views import Logon
from Tkinter import Tk
import subprocess
import tkMessageBox
import os
import tools.database as db

# List of all the files necessary to run the program.
files = {'images' :['example.gif', 'go.gif', 'main.gif', 'score.gif',
                    'spbee.gif', 'speak.gif', 'stop.gif', 'submit.gif'], 'config': ['.config']}

def check_festival():
    '''
    Try run festival to check if it's installed. If not. show an error and don't
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
    Check that all the necessary images exist in the images folder and that the
    administrator specified in the config file exists.
    '''
    try:
        f = open('.config', 'r')
        admin = f.readline().split('=')[1]
        f.close()
        
        um = db.get_user_manager()
        
        # If the specified admin is not in the database, delete the config.
        # This will cause the logon screen to re-prompt user to create an admin
        # account.
        if not um.retrieve_user(admin):
            os.remove('.config')
    except IOError:
        # If the config doesn't exist, we don't care because the logon screen
        # will prompt the user to create an admin account.
        pass
    
    for image in files['images']:
        # Check that each image exists
        try:
            f = open('images/' + image, 'r')
            f.close()
        except IOError:
            tkMessageBox.showerror('Error', 'You are missing the file ' +
                                   image + '. Please reinstall.')
            return False
        
    return True

if __name__ == '__main__':
    '''Run spellathon.'''
    if check_files() and check_festival():
        # Create the widgets.
        root = Tk()
        root.resizable(False, False)
        logon = Logon(root)
        logon.pack()

        # Enter the mainloop and begin the program.
        root.mainloop()
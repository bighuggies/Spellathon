'''
Module to build each view and manage behaviour of the Spellathon application.

Exported classes:

Logon -- Initial screen of the application where users log on.
WelcomeScreen -- First screen of the student part of the application where
students can choose to start spelling or see their scores.
SpellingAid -- Spelling aid game.
SpellingComplete -- Summary of the students performance after a game.
Score -- Scores of a student for all available lists.
Administration -- Frame to hold list and user management tabs.
ListManagement -- Let administrators edit, import, delete and create new lists.
NewList -- Dialog where new list information is given by the user.
ListEdit -- Add and remove words from lists.
NewWord -- Dialog where new word information is given by the user.
UserManagement -- Let administrators delete users, create new users, and view
user scores.
NewUser -- Dialog where new user information is given by the user.

'''
from Tkinter import *
import hashlib
import tkFileDialog
import random
import tools.database as database
from widgets import Dialog, ScrollListbox, TabBar, MultiScrollListbox, DateEntry
from models import *
from tools.speech import Speech
from user import User
from game import Session
from words import Word

'''
Option constants for widgets

'''
pad2 = {'padx' : 2, 'pady' : 2}
pad5 = {'padx' : 5, 'pady' : 5}
helv12 = {'font' : ('Helvetica', 12)}
helv16 = {'font' : ('Helvetica', 16)}
difficulties = ['CL1', 'CL2', 'CL3', 'CL4', 'CL5', 'CL6', 'CL7', 'CL8', 'AL1', 'AL2']

class Logon(Frame):
    '''Initial screen of the application where users log on.

    Public functions:
    user_added -- Called by the database when an administrator is added.

    '''
    def __init__(self, master=None):
        '''Create the logon screen.'''
        Frame.__init__(self, master)
        
        # Set the title of the root window.
        self.master.title('Spellathon Logon')
        
        # Bind enter to log on.
        self.master.bind('<Return>', self._validate)
        
        # Create the logon screen.
        self._build()
        self._arrange()
        
        # Get access to the user database to let the class validate log on
        # attempts.
        self.um = database.get_user_manager()
        
        # Set the initial focos to the username field.              
        self.username_ebx.focus_set()
        
    def _build(self):
        '''Create logon widgets.'''
        # Spellathon logo, header.
        self.heading_lbl = Label(self, text='SPELLATHON', **helv16)
        self.logo = PhotoImage(file='images/main.gif')
        self.logo_lbl = Label(self, image=self.logo)
        
        # All of the usual login fields.
        self.loginframe = LabelFrame(self, text='Login', **pad5)
        self.username_lbl = Label(self.loginframe, text='Username:', width=35)
        self.password_lbl = Label(self.loginframe, text='Password:')
        self.username_ebx = Entry(self.loginframe)
        self.password_ebx = Entry(self.loginframe, show='*')
        
        # Buttons to log in, create new users, and administrate.
        self.login_btn = Button(self.loginframe, text='Login',
                                command=self._validate)
        
        self.new_user_btn = Button(self.loginframe, text='New user',
                                   command=self._new_user)
        
        self.administrate_btn = Button(self.loginframe, text='Administrate',
                                       command=self._validate_admin)

        # List of login elements for easier arrangement.
        self.login_elements = [self.username_lbl, self.username_ebx,
                               self.password_lbl, self.password_ebx,
                               self.login_btn, self.new_user_btn, 
                               self.administrate_btn]

        # List of elements for easier arrangement.
        self.elements = [self.logo_lbl, self.heading_lbl, self.loginframe]
        
    def _arrange(self):
        '''Place the widgets on the form.'''
        # Arrange the picture, the login fields, and the administration panel
        for i, element in enumerate(self.elements):
            element.grid(column=0, row=i, sticky='we', **pad5)
                
        # Arrange the login labels and fields
        for i, widget in enumerate(self.login_elements):
            widget.grid(column=0, row=i, sticky='we', **pad2)
                                        
    def _new_user(self):
        '''Create a new user dialog.'''
        nu = NewUser(self, btncolumn=0, title='New user')
        
    def _welcome(self, user):
        '''Create the welcome frame and destroy this one.'''
        ws = WelcomeScreen(user, master=self.master)
        self.destroy()
        ws.pack()
                
    def _administrate(self):
        '''Create the administration frame and destroy this one.'''
        admin = Administration(self.master)
        self.destroy()
        admin.pack()

    def _validate(self, *args):
        '''Check the login details.'''
        # Fetch the information from the fields.
        username = self.username_ebx.get()
        password = hashlib.sha224(username + self.password_ebx.get()).hexdigest()
        
        # Get the user object from the database.
        user = self.um.retrieve_user(username)
        
        # Check if the details are correct. Show error dialogs if they are not.
        if user:
            if user.password == password:
                self._welcome(user)
            else:
                tkMessageBox.showerror('Error', 'Incorrect password')
        else:
            tkMessageBox.showerror('Error', 'No such user')
            
    def _validate_admin(self):
        '''Validate administrator details.'''
        # Get the name of the admin account from the configuration file.
        admin = self._load_config()
        
        # Check if an admin has been specified.
        if admin:
            username = self.username_ebx.get()
            
            # If the provided username matches the administrator username, check
            # the password and show the administration view.
            if username == admin:
                password = hashlib.sha224(username + 
                                          self.password_ebx.get()).hexdigest()
                user = self.um.retrieve_user(username)
                
                if user:
                    if user.password == password:
                        self._administrate()
                    else:
                        tkMessageBox.showerror('Error', 'Incorrect password')
                else:
                    tkMessageBox.showerror('Error', 'No such user')        
            else:
                tkMessageBox.showerror('Error', 'You are not an administrator')
                
        # If no admin has been specified, prompt the user to make an
        # administrator account.
        else:
            tkMessageBox.showerror('Error', 'It appears that this is the' +
                                   ' first time you have launched Spellathon.' +
                                   ' In order to manage users and word lists,' +
                                   ' you will need to create an administrator' +
                                   ' account. Make sure you take note' +
                                   ' of the username and password, because' +
                                   ' it will not be recoverable.')
            self._new_admin()
    
    def _load_config(self):
        '''Load the configuration file.
        
        Returns:
        The name of the administrator account.
        
        '''
        try:
            cfg = open('.config', 'r')
            admin = cfg.readline().split('=')
            cfg.close()
            if admin[0] == 'admin':
                return admin[1]
            else:
                return None
        except IOError:
            return None
            
    def _new_admin(self):
        '''Prompt the user to create a new admin and listen for completion.'''
        # Begin listening for account creation.
        self.um.add_listener(self)
        # Prompt the user to create the admin account.
        nu = NewUser(self, btncolumn=0, title='New administrator')
        # Stop listening for account creation, so that future accounts which may
        # be created do not get set as admin accounts.
        self.um.remove_listener(self)

    def user_added(self, user):
        '''Save the administrator account name to a configuration file.'''
        cfg = open('.config', 'w')
        cfg.write('admin=' + user.username)
        cfg.close
        
class WelcomeScreen(Frame):
    '''The view that is presented to a student after they have logged in, which
    allows them to subsequently being spelling or view their scores.'''
    def __init__(self, user, master=None):
        '''Create the welcome screen.
        
        Arguments:
        user -- Keep track of the logged in user.
        master -- Parent window.
        
        '''
        Frame.__init__(self, master)
        # Set the window title and bind enter to begin spelling and escape to
        # log out.
        self.master.title('Welcome to Spellathon')
        self.master.bind('<Return>', self._spelling_aid)
        self.master.bind('<Escape>', self._log_out)

        # Keep track of which user is logged in.
        self.user = user
        
        self._build()
        self._arrange()
        
        #Set the initial focus to begin spelling.
        self.spelling_btn.focus_set()
        
    def _build(self):
        '''Create the widgets.'''
        # Images for buttons
        self.spelling_img = PhotoImage(file='images/spbee.gif')
        self.score_img = PhotoImage(file='images/score.gif')
        
        # Buttons
        self.welcome_frame = LabelFrame(self, text='Welcome', **pad5)
        self.welcome_lbl = Label(self.welcome_frame, text='Welcome ' + self.user.realname + '!', **helv16)
        self.spelling_btn = Button(self.welcome_frame, text='Begin Spelling', 
                                   command=self._spelling_aid, image=self.spelling_img, compound=BOTTOM, **helv16)
        self.score_btn = Button(self.welcome_frame, text='View Scores', 
                                command=self._score_frame, image=self.score_img, compound=BOTTOM, **helv16)
        self.logout_btn = Button(self, text='Log out', command=self._log_out, **pad5)
        
    def _arrange(self):
        '''Arrange the widgets.'''
        self.welcome_frame.grid(**pad5)
        self.welcome_lbl.grid(**pad2)
        self.spelling_btn.grid(sticky='we', **pad2)
        self.score_btn.grid(sticky='we', **pad2)
        self.logout_btn.grid(sticky='we', **pad5)
        
    def _spelling_aid(self):
        '''Create the spelling aid view and destroy this one.'''
        sa = SpellingAid(self.user, master=self.master)
        self.destroy()
        sa.pack()
        
    def _score_frame(self):
        '''Show the score dialog.'''
        sc = Score(self.user, master=self, title=self.user.realname + ' Scores')
        
    def _log_out(self, *args):
        '''Return to the login screen.'''
        if tkMessageBox.askokcancel('Log out',
                                    'Are you sure you want to log out?'):
            
            ln = Logon(master=self.master)
            
            # Unbind escape so if it is pressed after this window is destroyed,
            # no error is thrown.
            self.master.unbind('<Escape>')
            
            self.destroy()
            ln.pack()

class SpellingAid(Frame):
    '''Spelling aid game.
    
    Public functions:
    session_ended -- Called when a spelling session has finished.
    update -- Update the word and score interface elements.
    
    '''
    def __init__(self, user, master=None):
        '''Create the Spelling Aid view.
        
        Arguments:
        user -- Keep track of the logged in user.
        master -- Parent window.
        
        '''
        Frame.__init__(self, master)
        self.master.title('Spellathon Spelling Aid')
        self.master.bind('<Return>', self._submit)
        self.master.bind('<Escape>', self._exit)
        
        self.user = user
        self.session = None

        self._build()
        self._arrange()
        
        self.start_spelling_btn.focus_set()
        
    def _build(self):
        '''Build the component widgets.'''
        # Components to select the list to spell.
        self.lists_frame = Frame(self, **pad5)
        self.lists_lbl = Label(self.lists_frame, text='Choose a list to begin spelling!', **helv12)
        self.lists_var = StringVar()
        self.lists_opt = OptionMenu(self.lists_frame, self.lists_var, '')
        self.lists_opt.config(anchor='w')
        self.lists_model = TLDROptionMenuModel(self.lists_opt, self.lists_var)
        
        # Button to begin a spelling session.
        self.start_spelling_img = PhotoImage(file='images/go.gif')
        self.stop_spelling_img = PhotoImage(file='images/stop.gif')
        self.start_spelling_btn = Button(self.lists_frame, text='Start', command=self._start_session, 
                                         image=self.start_spelling_img, compound=CENTER, font=('Helvetica', '14'), relief=FLAT)
        
        # Word entry widgets where the user will make spelling attempts.
        self.word_lbl = Label(self, text='Enter the word you hear and click _submit!', **helv16)
        self.word_ebx= Entry(self, font=('Helvetica', '24'), width=30, state=DISABLED)
        self.word_submit_img = PhotoImage(file='images/_submit.gif')

        # Buttons to submit the attempt, speak the word, and speak the example.
        self.buttons = Frame(self, padx=5, pady=20)
        self.word_submit_btn = Button(self.buttons, text='Submit', compound=TOP,
                                      image=self.word_submit_img, command=self._submit, state=DISABLED, relief=FLAT, font=('Helvetica', '10'))
        self.speak_img = PhotoImage(file='images/speak.gif')
        self.speak_again_btn = Button(self.buttons, text='Speak again', state=DISABLED,
                                      image=self.speak_img, compound=TOP, relief=FLAT, font=('Helvetica', '10'))
        self.example_img = PhotoImage(file='images/example.gif')
        self.example_btn = Button(self.buttons, text='Example', state=DISABLED,
                                  image=self.example_img, compound=TOP, relief=FLAT, font=('Helvetica', '10'))
        
        # Word metadata labels.
        self.word_metadata = Frame(self)
        self.word_definition_lbl = Text(self.word_metadata, height=5, state=DISABLED, font=('Helvetica', '10'))
        self.definition_lbl= Label(self.word_metadata, text='Definition:', **helv12)
        
        # Score information.
        self._score_frame = LabelFrame(self, text='Score', **pad5)
        self.score_lbl = Label(self._score_frame, text='Score:', **helv12)
        self.current_score_lbl= Label(self._score_frame, text='0/0', **helv16)
        self.high_score_lbl = Label(self._score_frame, text='High score:', **helv12)
        self.current_high_score_lbl = Label(self._score_frame, text='n/a', **helv16)
        self.score_elements = [self.score_lbl, self.current_score_lbl,
                               self.high_score_lbl, self.current_high_score_lbl]
        
        # Exit button.
        self.exit_btn= Button(self, text='Exit', command=self._exit)
            
    def _arrange(self):
        '''Place the widgets within the frame.'''
        self.lists_frame.grid(column=0, row=0, **pad5)
        
        self.lists_lbl.grid(column=1, row=0, sticky='nswe', padx=5, pady=2)
        self.lists_opt.grid(column=1, row=1, sticky='nswe', padx=5, pady=2)
        self.start_spelling_btn.grid(column=0, row=0, rowspan=2, padx=5, pady=2)
        
        self.word_lbl.grid(column=0, row=2, columnspan=2, sticky='nswe', padx=20, pady=2)
        self.word_ebx.grid(column=0, row=3, padx=20, pady=2)
        self.word_submit_btn.grid(column=2, row=0, sticky='we', padx=20, pady=2)
        self.buttons.grid(column=0, row=5, columnspan=2)
        self.word_metadata.grid(column=0, row=6, sticky='we', columnspan=2, **pad5)
        
        self._score_frame.grid(column=0, row=7, sticky='we', columnspan=2, **pad5)
        
        self.exit_btn.grid(column=0, row=8, sticky='we', padx=5, pady=2)
        
        for i, widget in enumerate(self.score_elements):
            widget.grid(column=i, row=0, sticky='w', **pad2)
                    
        self.definition_lbl.grid(column=0, row=0, sticky='nw', **pad2)
        self.word_definition_lbl.grid(column=0, row=1, sticky='w', **pad2)
        
        self.speak_again_btn.grid(column=0, row=0, sticky='nswe', **pad2)
        self.example_btn.grid(column=1, row=0, sticky='nswe', **pad2)
        
    def _exit(self, *args):
        '''End the session and return to the welcome screen.'''
        if tkMessageBox.askokcancel('Exit', 'Are you sure you want to _exit? Your progress will be saved.'):
            if self.session:
                # If there was an ongoing session, end it.
                self._end_session()
            
            # Create the welcome screen, destroy this view, show the welcome
            # screen.
            ws = WelcomeScreen(self.user, master=self.master)
            self.destroy()
            ws.pack()
        
    def _start_session(self):
        '''Begin a spelling session when the 'start spelling' button is
        pressed.'''
        if self.lists_model.get_list():
            # Change 'start spelling' button to 'stop spelling' button.
            self.start_spelling_btn.config(text='Stop', command=self._end_session, image=self.stop_spelling_img)
            
            # Begin a spelling session.
            self.session = Session(self, self.lists_model.get_list(), self.user)
            
            # Enable the speech buttons.
            self.speak_again_btn.config(command=self.session.speak_word)
            self.example_btn.config(command=self.session.speak_example)
            
            # Disable the list selection optionmenu while spelling is ongoing.
            self.lists_opt.config(state=DISABLED)
            
            # Enable all the spelling aid controls.
            self.speak_again_btn.config(state=NORMAL)
            self.example_btn.config(state=NORMAL)
            self.word_ebx.config(state=NORMAL)
            self.word_submit_btn.config(state=NORMAL)
            
            # Set the focus to the submission box and start the session.
            self.word_ebx.focus_set()
            self.session.start()
        else:
            # If no word lists have been created, show an error.
            tkMessageBox.showerror('Error', 'There are no word lists! Get your teacher to make some for you!')
        
    def _end_session(self):
        '''End the session. If the session ends successfully, session_ended will
        be called.'''
        self.session.end()
    
    def _submit(self, *args):
        '''Submit the attempt to be checked and empty the submission box.'''
        self.session.check(self.word_ebx.get())
        self.word_ebx.delete(0, END)
        
    def session_ended(self, score, highscore, newhighscore, attempts):
        '''Called when a session has ended. Return the interface to a non-active
        state.
        
        Arguments:
        score -- The score achieved during the session (no. correct attempts).
        highscore -- The high score of the user for this list.
        newhighscore -- Boolean representing whether or not a new high score was
        set.
        attempts -- The submissions made by the user during the spelling
        session.
        
        '''
        # 'Stop spelling' button becomes 'start spelling' button.
        self.start_spelling_btn.config(text='Start', command=self._start_session, image=self.start_spelling_img)
        
        # Score information is reset.
        self.current_score_lbl.config(text='0/0')
        self.current_high_score_lbl.config(text='n/a')
        
        # Word submission box is cleared.
        self.word_ebx.delete(0, END)
        
        # Have to enable the word definition text box in order to clear it, then
        # it is disabled again.
        self.word_definition_lbl.config(state=NORMAL)
        self.word_definition_lbl.delete(1.0, END)
        self.word_definition_lbl.config(state=DISABLED)
        
        # Reset the instruction label.
        self.word_lbl.config(text='Enter the word you hear and click _submit!', fg='black')
        
        # Enable the list selection option menu.
        self.lists_opt.config(state=NORMAL)
        
        # Disable the spelling aid controls.
        self.speak_again_btn.config(state=DISABLED)
        self.example_btn.config(state=DISABLED)
        self.word_ebx.config(state=DISABLED)
        self.word_submit_btn.config(state=DISABLED)
        
        # Show the statistics from the completed session.
        sc = SpellingComplete(self, self.lists_model.get_list_name(), score, highscore, newhighscore, attempts)
        
        self.session = None
        
    def update(self, definition, score, highscore, correct):
        '''Update the score information and word metadata. Usually called after
        a submission when a new word is available to spell.
        
        Arguments:
        definition -- The definition of the new word being spelled.
        score -- The current score of the user for the session.
        highscore -- The current high score of the user for the list.
        correct -- Boolean representing whether or not the previous submission
        was correct.
        '''
        # Have to enable the text box to update it and then disable it again to
        # prevent users typing in it.
        self.word_definition_lbl.config(state=NORMAL)
        self.word_definition_lbl.delete(1.0, END)
        self.word_definition_lbl.insert(END, definition)
        self.word_definition_lbl.config(state=DISABLED)
        
        self.current_score_lbl.config(text=score)
        self.current_high_score_lbl.config(text=highscore)
        
        if correct == True:
            self.word_lbl.config(text='Well done!', fg='green')
        elif correct == False:
            self.word_lbl.config(text='Better luck next time', fg='red')
        elif correct == None:
            self.word_lbl.config(text='Enter the word you hear and click _submit!', fg='black')

class SpellingComplete(Dialog):
    def __init__(self, master, listname, score, highscore, newhighscore, attempts):
        self.list = listname
        self.score = score
        self.highscore = highscore
        self.newhighscore = newhighscore
        self.attempts = attempts
        
        Dialog.__init__(self, master, 'Well done', 0)  
                    
    def _build(self):
        self.list_complete_lbl = Label(self, text='You have completed ' + self.list)

        self._score_frame = LabelFrame(self, text='Score', **pad5)
        self.score_lbl = Label(self._score_frame, text='Score:', **helv12)
        self.current_score_lbl= Label(self._score_frame, text=str(self.score), **helv16)
        self.high_score_lbl = Label(self._score_frame, text='High score:', **helv12)
        self.current_high_score_lbl = Label(self._score_frame, text=str(self.highscore), **helv16)
        self.score_elements = [self.score_lbl, self.current_score_lbl,
                               self.high_score_lbl, self.current_high_score_lbl]
        
        self.attempts_frame = LabelFrame(self, text='Your attempts', **pad5)
        
        self.attempt_keys = []
        self.attempt_values = []
        
        for key, value in self.attempts.iteritems():
            if key == value:
                self.attempt_keys.append(Label(self.attempts_frame, text=key + ':', **helv12))
                self.attempt_values.append(Label(self.attempts_frame, text=value, **helv12))
            else:
                self.attempt_keys.append(Label(self.attempts_frame, text=key + ':', fg='red', **helv12))
                self.attempt_values.append(Label(self.attempts_frame, text=value, fg='red', **helv12))

        if self.newhighscore:
            self.congratulations_lbl = Label(self, text='New high score!', fg='orange', **helv16)
        else:
            self.congratulations_lbl = Label(self, text='Well done!', fg='brown', font=('Helvetica', '14'))
        
    def _arrange(self):
        self.list_complete_lbl.grid(column=0, row=0, **pad2)
        
        self._score_frame.grid(column=0, row=1, sticky='we', **pad5)
        
        self.congratulations_lbl.grid(column=0, row=2, **pad2)
        
        self.attempts_frame.grid(column=0, row=3, sticky='we', **pad5)
        
        j = 1
        for i, l in enumerate(self.attempt_keys):
            l.grid(column=j, row=i%10, sticky='w', **pad5)
            if i%10 == 9:
                j += 2
            
        j = 2
        for i, l in enumerate(self.attempt_values):
            l.grid(column=j, row=i%10, sticky='w', **pad5)
            if i%10 == 9:
                j+= 2

        for i, widget in enumerate(self.score_elements):
            widget.grid(column=0, row=i, sticky='w', **pad2)

class Score(Dialog):
    def __init__(self, user, master=None, title=None):
        self.user = user
        Dialog.__init__(self, master, btncolumn=0, title=title)
          
    def _build(self):        
        self.list_metadata = LabelFrame(self, text='Score', **pad5)
        
        self.num_words_lbl = Label(self.list_metadata, text='Number of words:', **helv12)
        self.difficulty_lbl = Label(self.list_metadata, text='Average word length:', **helv12)
        self.num_attempts_lbl = Label(self.list_metadata, text='Number of attempts:', **helv12)
        self.high_score_lbl = Label(self.list_metadata, text='High score:', **helv12)
        self.list_metadata_labels = [self.num_words_lbl, self.difficulty_lbl, 
                                     self.num_attempts_lbl, self.high_score_lbl]
        
        self.list_num_words_lbl = Label(self.list_metadata, text='0', **helv16)
        self.list_difficulty_lbl = Label(self.list_metadata, text='None', **helv16)
        self.list_num_attempts_lbl = Label(self.list_metadata, text='0', **helv16)
        self.list_high_score_lbl = Label(self.list_metadata, text='0', **helv16)
        self.list_metadata_fields = [self.list_num_words_lbl, self.list_difficulty_lbl,
                                     self.list_num_attempts_lbl, self.list_high_score_lbl]
        
        self.lists_frame = LabelFrame(self, text='Lists', **pad5)
        self.lists_var = StringVar()
        self.lists_opt = OptionMenu(self.lists_frame, self.lists_var, '')
        self.lists_opt.config(anchor='w')
        
        self.lists_model = TLDROptionMenuModel(self.lists_opt, self.lists_var)
        self.lists_var.trace('w', self.update_metadata)
        
        # Dirty hack to cause the metadata to update on the initial opening of
        # the window.
        self.lists_var.set(self.lists_var.get())
        
    def _arrange(self):
        self.lists_frame.grid(column=0, row=0, sticky='nswe', **pad5)
        self.lists_opt.grid(sticky='we', **pad2)
        
        self.list_metadata.grid(column=0, row=1, sticky='nswe', **pad5)
                
        for i, label in enumerate(self.list_metadata_labels):
            label.grid(column=0, row=i, sticky='w', **pad2)
        
        for i, label in enumerate(self.list_metadata_fields):
            label.grid(column=1, row=i, sticky='w',  **pad2)
            
    def update_metadata(self, *args):
        wordlist = self.lists_model.get_list()

        self.list_num_words_lbl.config(text=str(len(wordlist.words)))
        
        length = 0
        
        for key in wordlist.words.iterkeys():
            length += len(key)
            
        difficulty = length/len(wordlist.words.keys())
        
        self.list_difficulty_lbl.config(text=str(difficulty))
        
        try:
            attempts = len(self.user.scores[wordlist.name])
        except KeyError:
            attempts = 0
            
        self.list_num_attempts_lbl.config(text=str(attempts))
        
        highscore = self.user.high_score(wordlist.name)
        self.list_high_score_lbl.config(text=str(highscore))

class Administration(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Administration')
        self._build()
        self._arrange()
        
    def _build(self):
        um = UserManagement(self)
        lm = ListManagement(self)
                
        tabs = {'Manage Users': um, 'Manage Lists': lm}
        
        self.tabs = TabBar(self, tabs=tabs)
        self.logout = Button(self, text="Log out", command=self._log_out)
        
    def _arrange(self):
        self.tabs.grid(row=0, column=0, sticky="we")
        self.logout.grid(row=2, column=0, sticky="e", **pad5)
        
    def _log_out(self):
        if tkMessageBox.askokcancel('Log out', 'Are you sure you want to log out?'):
            logon = Logon(self.master)
            self.destroy()
            logon.grid()
            
class ListManagement(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self._build()
        self._arrange()
        
    def _build(self):
        items = [(0, 0, 0, 0)]
        
        self.manage_lists_frame = LabelFrame(self, text='Manage lists', **pad5)
        
        headers =['List name', 'List author', 'Date last edited', 'Number of words']
        self.list_lbx = MultiScrollListbox(self.manage_lists_frame, items, headers)
        self.list_model = TLDRMultiScrollListbox(self.list_lbx)
        
        self.new_list_btn = Button(self.manage_lists_frame, text='New list', command=self.new_list)
        self.delete_list_btn = Button(self.manage_lists_frame, text='Delete list', command=self.delete_list)
        self.edit_list_btn = Button(self.manage_lists_frame, text='Edit list', command=self.list_edit)
        self.import_list_btn = Button(self.manage_lists_frame, text='Import list', command=self.import_list)
        
        self.controls = [self.new_list_btn, self.delete_list_btn,
                         self.edit_list_btn, self.import_list_btn]

    def _arrange(self):
        self.manage_lists_frame.grid(**pad5)
        
        self.list_lbx.grid(column=0, row=0, rowspan=4, **pad5)
        
        for i, control in enumerate(self.controls):
            control.grid(column=1, row=i, sticky='we', padx=5, pady=2)
            
    def new_list(self):
        nl = NewList(master=self, title='New list', btncolumn=0)
        self.list_model.update_items()
            
    def delete_list(self):
        if tkMessageBox.askokcancel('Delete list', 'Are you sure you want to delete the currently selected list?'):
            self.list_model.delete()
            
    def list_edit(self):
        if self.list_lbx.get():
            le = ListEdit(self.list_lbx.get(), master=self)
        else:
            tkMessageBox.showerror('Error', 'Please select a list to edit.')
        
    def import_list(self):
        listfile = tkFileDialog.askopenfilename(filetypes=[('tldr files', '.tldr')])
        self.list_model.import_list(listfile)

class NewList(Dialog):    
    def _build(self):
        self.list_information_frame = LabelFrame(self, text='List details', **pad5)
        self.name_lbl = Label(self.list_information_frame, text='Name:')
        self.author_lbl = Label(self.list_information_frame, text='Author:')
        
        self.name_ebx = Entry(self.list_information_frame)
        self.author_ebx = Entry(self.list_information_frame)
        
        self.labels = [self.name_lbl, self.author_lbl]
        self.fields = [self.name_ebx, self.author_ebx]

    def _arrange(self):
        self.list_information_frame.grid(column=0, row=0, sticky='nswe', **pad5)
        
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i, sticky='nw', **pad2)
            
        for i, field in enumerate(self.fields):
            field.grid(column=1, row=i, sticky='we', **pad2)
        
    def _validate(self):
        name = self.name_ebx.get()
        author = self.author_ebx.get()
        
        if name == '':
            tkMessageBox.showerror('Error', 'Please enter a list name.')
            return False
        
        if author == '':
            tkMessageBox.showerror('Error', 'Please enter a list author')
            return False
        
        return True
        
    def _apply(self):
        name = self.name_ebx.get()
        author = self.author_ebx.get()
        path = 'wordlists/' + name + '.tldr'
        
        tldr.generate_empty_tldr(path, name, author)
        
class ListEdit(Dialog):
    def __init__(self, listname, master=None):
        self.listname = listname
        self.word = None
        
        Dialog.__init__(self, master, title='Edit list', btncolumn=0)
    
    def _build(self):
        self.source_frame = LabelFrame(self, text='Source', **pad5)
        self.destination_frame = LabelFrame(self, text=self.listname, **pad5)
        
        self.source_var = StringVar()
        self.source_opt = OptionMenu(self.source_frame, self.source_var, *difficulties)

        self.source_words_lbx = ScrollListbox(self.source_frame)
        self.source_filter_var = StringVar()
        self.source_filter_ebx = Entry(self.source_frame, textvariable=self.source_filter_var)
        
        self.source_model = WordSourceModel(self, self.source_opt, self.source_var, self.source_words_lbx, self.source_filter_ebx, self.source_filter_var)
        
        self.source_var.set('CL1')

        
        self.control_column = Frame(self)
        self.add_btn = Button(self.control_column, text='Add word >', command=self.add_word)
        self.add_all_btn = Button(self.control_column, text='Add all words >>', command=self.add_all_words)
        self.add_x_btn = Button(self.control_column, text='Add x words >', command=self.add_x_words)
        self.x_ebx = Entry(self.control_column, width=10)
        self.x_ebx.insert(END, 'x')
        self.remove_btn = Button(self.control_column, text='Remove word', command=self.remove_word)
        self.remove_all_btn = Button(self.control_column, text='Remove all words', command=self.remove_all_words)
        self.new_word_btn = Button(self.control_column, text='Add new word', command=self.new_word)
        
        self.control_column_elements = [self.add_btn, self.add_all_btn, self.add_x_btn, self.x_ebx,
                                        self.remove_btn, self.remove_all_btn, self.new_word_btn]
        
        self.destination_lbl = Label(self.destination_frame, text='List contents:')
        self.destination_lbx = ScrollListbox(self.destination_frame)
        self.destination_filter_var = StringVar()
        self.destination_filter_ebx = Entry(self.destination_frame, textvariable=self.destination_filter_var)
        
        self.destination_model = WordDestinationModel(self, self.listname, self.destination_lbx, self.destination_filter_ebx, self.destination_filter_var)
        
        self.word_metadata = LabelFrame(self, text='Word', **pad5)
                
        self.definition_lbl= Label(self.word_metadata, text='Definition:')
        self.example_lbl = Label(self.word_metadata, text='Example:')
        self.word_definition_lbl = Label(self.word_metadata, text='No definition', wraplength=500, justify=LEFT)
        self.word_example_lbl = Label(self.word_metadata, text='No example', wraplength=500,justify=LEFT)
        self.speak_btn = Button(self.word_metadata, text='Speak', command=self.speak)
                
    def _arrange(self):
        self.source_frame.grid(column=0, row=0, sticky='nswe', **pad5)
        
        self.source_opt.grid(column=0, row=0, sticky='we', **pad2)
        self.source_words_lbx.grid(column=0, row=1, sticky='nswe', **pad2)
        self.source_filter_ebx.grid(column=0, row=2, sticky='nswe', **pad2)
        
        self.control_column.grid(column=1, row=0, sticky='nswe', **pad5)
        
        for i, button in enumerate(self.control_column_elements):
            button.grid(column=0, row=i, sticky='we', **pad2)
            
        self.destination_frame.grid(column=2, row=0, sticky='nswe', **pad5)
        
        self.destination_lbl.grid(column=0, row=0, sticky='nsw', **pad2)
        self.destination_lbx.grid(column=0, row=1, sticky='nswe', **pad2)
        self.destination_filter_ebx.grid(column=0, row=2, sticky='nswe', **pad2)
        
        self.word_metadata.grid(column=0, row=1, columnspan=3, sticky='we', **pad5)
        
        self.definition_lbl.grid(column=0, row=0, sticky='nw', **pad2)
        self.example_lbl.grid(column=0, row=1, sticky='nw', **pad2)
        self.word_definition_lbl.grid(column=1, row=0, sticky='nw', **pad2)
        self.word_example_lbl.grid(column=1, row=1, sticky='nw', **pad2)
        self.speak_btn.grid(column=0, row=2, sticky='nw', columnspan=2, **pad2)
        
    def add_word(self):
        if self.word:
            self.destination_model.add_word(self.source_model.get_word())
        else:
            tkMessageBox.showerror('Error', 'No word selected')

    def add_all_words(self):
        self.destination_model.add_words(self.source_model.get_words())
    
    def add_x_words(self):
        try:
            x = int(self.x_ebx.get())
            words = self.source_model.get_words()
            
            keys = words.keys()
            random.shuffle(keys)
            
            try:
                for i in range(0, x):
                    self.destination_model.add_word(words[keys.pop()])
            except IndexError:
                pass
                        
        except ValueError:
            tkMessageBox.showerror('Error', 'Please enter a number')
            
    def remove_word(self):
        if self.word:
            self.destination_model.remove_word(self.word)
        else:
            tkMessageBox.showerror('Error', 'No word selected')
            
    def remove_all_words(self):
        self.destination_model.remove_all_words()
                    
    def speak(self):
        if self.word:
            speech = Speech()
            speech.speak(self.word.word)
        else:
            tkMessageBox.showerror('Error', 'No word selected')
        
    def update_metadata(self, word):
        self.word = word
        self.word_definition_lbl.config(text=word.definition)
        self.word_example_lbl.config(text=word.example)
        
    def reset_metadata(self):
        self.word = None
        self.word_definition_lbl.config(text='No definition')
        self.word_example_lbl.config(text='No example')
        
    def new_word(self):
        nw = NewWord(self.destination_model, master=self)
        
    def _validate(self):
        return tkMessageBox.askokcancel('Save new list', 'Save changes to ' + self.listname + '?')
    
    def _apply(self):
        self.destination_model.save()
        self.master.list_model.update_items()

class NewWord(Dialog):
    def __init__(self, model, master=None):
        self.model = model
        
        Dialog.__init__(self, master, title='New word', btncolumn=0)
    
    def _build(self):
        self.word_information_frame = LabelFrame(self, text='Word details', **pad5)
        self.word_lbl = Label(self.word_information_frame, text='Word:')
        self.definition_lbl = Label(self.word_information_frame, text='Definition:')
        self.example_lbl = Label(self.word_information_frame, text='Example:')
        self.difficulty_lbl = Label(self.word_information_frame, text='Difficulty:')
        self.difficulty_var = StringVar()
        self.difficulty_opt = OptionMenu(self.word_information_frame, self.difficulty_var, *difficulties)
        self.difficulty_var.set('CL1')
        
        self.word_ebx = Entry(self.word_information_frame)
        self.definition_ebx = Text(self.word_information_frame, width=30, height=4)
        self.example_ebx = Text(self.word_information_frame, width=30, height=4)
        
        self.labels = [self.word_lbl, self.definition_lbl, self.example_lbl, self.difficulty_lbl]
        self.fields = [self.word_ebx, self.definition_ebx, self.example_ebx, self.difficulty_opt]
        
    def _arrange(self):
        self.word_information_frame.grid(column=0, row=0, sticky='nswe', **pad5)
        
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i, sticky='nw', **pad2)
            
        for i, field in enumerate(self.fields):
            field.grid(column=1, row=i, sticky='we', **pad2)
            
    def _validate(self):
        if self.word_ebx.get() == "":
            tkMessageBox.showerror('Error', 'Please enter a word.')
            return False
            
        if self.definition_ebx.get(1.0, END) == "":
            tkMessageBox.showerror('Error', 'Please enter a definition.')
            return False

        if self.example_ebx.get(1.0, END) == "":
            tkMessageBox.showerror('Error', 'Please enter an example.')
            return False

        return True
    
    def _apply(self):
        word = Word(self.word_ebx.get(), self.definition_ebx.get(1.0, END).strip(), self.example_ebx.get(1.0, END).strip(), self.difficulty_var.get())
        self.model.add_word(word)
            
class UserManagement(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self._build()
        self._arrange()
        
    def _build(self):
        #####
        items = []
    
        for i in range(1,50):
            items.append((i, i, i))
        #####
        
        self.manage_users_frame = LabelFrame(self, text='Manage users', **pad5)
        headers = ['Username', 'Real name', 'Date of birth']
        
        self.user_lbx = MultiScrollListbox(self.manage_users_frame, items, headers)
        self.user_model = UserListModel(self.user_lbx)
        
        self.new_user_btn = Button(self.manage_users_frame, text='New user', command=self._new_user)
        self.delete_user_btn = Button(self.manage_users_frame, text='Delete user', command=self.delete_user)
        self.user_score_btn = Button(self.manage_users_frame, text='View scores', command=self.scores)
        
        self.controls = [self.new_user_btn, self.delete_user_btn,
                         self.user_score_btn]

    def _arrange(self):
        self.manage_users_frame.grid(**pad5)
        
        self.user_lbx.grid(column=0, row=0, rowspan=4, **pad5)
        
        for i, control in enumerate(self.controls):
            control.grid(column=1, row=i, sticky='we', padx=5, pady=2)
            
    def _new_user(self):
        nu = NewUser(self, btncolumn=0, title="Add user")
        self.user_model.update_items()
        
    def delete_user(self):
        self.user_model.delete_user()
        
    def scores(self):
        sc = Score(self.user_model.user, master=self, title="Scores")

class NewUser(Dialog):
    def _build(self):
        self.register_frame = LabelFrame(self, text='New user', **pad5)
        
        self.username_lbl = Label(self.register_frame, text='Username:')
        self.realname_lbl = Label(self.register_frame, text='Real name:')
        self.password_lbl = Label(self.register_frame, text='Password:')
        self.password_confirmation_lbl = Label(self.register_frame, text='Confirm password:')
        self.dob_lbl = Label(self.register_frame, text='Date of birth:')
        self.photo_lbl = Label(self.register_frame, text='Photo:')
        
        self.labels = [self.username_lbl, self.realname_lbl, self.password_lbl, 
                       self.password_confirmation_lbl, self.dob_lbl,
                       self.photo_lbl]
        
        self.username_ebx = Entry(self.register_frame)
        self.realname_ebx = Entry(self.register_frame)
        self.password_ebx = Entry(self.register_frame, show='*')
        self.password_confirmation_ebx = Entry(self.register_frame, show='*')
        self.dob_ebx = DateEntry(self.register_frame)
        
        self.photo_fields = Frame(self.register_frame)
        self.photo_btn = Button(self.photo_fields, text='Browse', command=self.get_photo)
        self.photo_ebx = Entry(self.photo_fields, state=DISABLED)
        
        self.fields = [self.username_ebx, self.realname_ebx, self.password_ebx,
                       self.password_confirmation_ebx, self.dob_ebx,
                       self.photo_fields]
        
    def _arrange(self):
        self.register_frame.grid(column=0, row=0, **pad5)
                
        self.photo_ebx.grid(column=0, row=0, sticky='we')
        self.photo_btn.grid(column=1, row=0, padx=2, sticky='e')
        
        for i, widget in enumerate(self.labels):
            widget.grid(column=0, row=i, sticky='w', **pad2)
            
        for i, widget in enumerate(self.fields):
            widget.grid(column=1, row=i, sticky='we', **pad2)
            
    def get_photo(self):
        self.photo_ebx.config(state=NORMAL)
        self.photo_ebx.insert(END, tkFileDialog.askopenfilename(filetypes=[('image files', '.gif')]))
        self.photo_ebx.config(state='readonly')
            
    def _validate(self):
        username = self.username_ebx.get()
        realname = self.realname_ebx.get()
        password = hashlib.sha224(username + self.password_ebx.get()).hexdigest()
        confpassword = hashlib.sha224(username + self.password_confirmation_ebx.get()).hexdigest()
        dob = self.dob_ebx.get()
        photo = self.photo_ebx.get()
        
        if username == '':
            tkMessageBox.showerror('Error', 'Please enter a username.')
            return False

        if realname == '':
            tkMessageBox.showerror('Error', 'Please enter your real name.')
            return False
        
        if self.password_ebx.get() == '':
            tkMessageBox.showerror('Error', 'Please provide a password.')
            return False

        if password != confpassword:
            tkMessageBox.showerror('Error', 'Passwords do not match.')
            return False
        
        self.user = User(username, realname, password, dob, photo)
        self.um = database.get_user_manager()
        
        if not self.um.add_user(self.user):
            tkMessageBox.showerror('Error', 'A user with that username already exists.')
            return False
        
        return tkMessageBox.askyesno('New user', 'Create user ' + username + '?')
        
    def _apply(self):
        self.um.commit()
        tkMessageBox.showinfo('User added', 'User ' + self.user.username + ' added successfully.')

        

'''
Module to build each view and manage behaviour of the Spellathon application.

Exported classes:

Initial -- The screen seen on the first run which prompts to create admin.
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
import tools.config as config
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

class Initial(Frame):
    '''Screen seen on the first run of the application which prompts the user to
    create an administrative account in order to be able to manage lists and 
    users.'''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.master.title("Welcome to Spellathon")
        
        # If an admin has been created, go to logon. Else, prompt to create
        # admin account.
        if not config.get_admin():
            # Boolean to track whether or not admin created.
            self.admin_created = False
            # Get the user manager and begin listening for new users.
            self.um = database.get_user_manager()
            self.um.add_listener(self)
            # Create the frame.
            self._build()
            self._arrange()
            # Set the focus on the new admin button and bind return to it.
            self.new_admin_btn.focus_set()
            self.master.bind('<Return>', self._new_admin)
            # Display this frame.
            self.pack()
        else:
            self._logon()
        
    def _build(self):
        '''Create the initial frame widgets.'''
        self.info_frame = LabelFrame(self, text='First run')
        self.info_lbl = Label(self.info_frame, text='It appears that this is the' +
                       ' first time you have launched Spellathon.' +
                       ' In order to manage users and word lists,' +
                       ' you will need to create an administrator' +
                       ' account. Make sure you take note' +
                       ' of the username and password, because' +
                       ' it will not be recoverable.', wraplength=300, justify=LEFT)
        self.new_admin_btn = Button(self.info_frame, text='Create Administrator',
                                    command=self._new_admin)
        
    def _arrange(self):
        '''Arrange the initial frame widgets.'''
        self.info_frame.grid(**pad5)
        self.info_lbl.grid(**pad2)
        self.new_admin_btn.grid(**pad5)
                    
    def _new_admin(self):
        '''Prompt the user to create a new admin and listen for completion.'''        
        # Prompt the user to create the admin account.
        while self.admin_created == False:
            nu = NewUser(self, btncolumn=0, title='New administrator')
        # Stop listening for account creation, so that future accounts which may
        # be created do not get set as admin accounts.
        self.um.remove_listener(self)
        self._logon()
        
    def user_added(self, user):
        '''When a user is added, write their name to the config as an admin.'''
        config.set_admin(user)
        self.admin_created = True
        
    def _logon(self):
        '''Create the logon view and destroy this one.'''
        logon = Logon(self.master)
        logon.pack()
        self.master.unbind('<Return>')
        self.destroy()

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
        self.um.add_listener(self)
        
        # Set the initial focos to the username field.              
        self.username_ebx.focus_set()
                
    def _build(self):
        '''Create logon widgets.'''
        # Spellathon logo, header.
        self.heading_lbl = Label(self, text='SPELLATHON', font=('Helvetica', 32))
        self.logo = PhotoImage(file='images/main.gif')
        self.logo_lbl = Label(self, image=self.logo)
        
        # All of the usual login fields.
        self.loginframe = LabelFrame(self, text='Login', **pad5)
        self.username_lbl = Label(self.loginframe, text='Username:', width=35)
        self.password_lbl = Label(self.loginframe, text='Password:')
        self.username_ebx = Entry(self.loginframe, **helv16)
        self.password_ebx = Entry(self.loginframe, show='*', **helv16)
        
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
        self._destroy()
        ws = WelcomeScreen(user, master=self.master)
        ws.pack()
                
    def _administrate(self):
        '''Create the administration frame and destroy this one.'''
        self._destroy()
        admin = Administration(self.master)
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
        admin = config.get_admin()
        
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
        # administrator account. This is necessary in case the user accidentally
        # cancelled the initial administrator account creation process.
        else:
            self._new_admin()
            
    def _destroy(self):
        '''Perform necessary cleanup on the destruction of this widget.'''
        self.master.unbind('<Return>')
        self.um.remove_listener(self)
        self.destroy()
                
    def user_added(self, user):
        '''Populate the username entrybox with the created user name.'''
        self.username_ebx.delete(0, END)
        self.username_ebx.insert(END, user.username)
        
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
        self.welcome_lbl.grid(column=0, row=0, columnspan=2, **pad2)
        self.spelling_btn.grid(column=0, row=1, sticky='nswe', **pad2)
        self.score_btn.grid(column=1, row=1, sticky='nswe', **pad2)
        self.logout_btn.grid(column=0, row=2, columnspan=2, sticky='nswe', **pad5)
        
    def _spelling_aid(self, *args):
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
        self.master.bind('<Return>', self._start_session)
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
        self.word_lbl = Label(self, text='Enter the word you hear and click submit!', **helv16)
        self.word_ebx= Entry(self, font=('Helvetica', '24'), width=30, state=DISABLED)
        self.word_submit_img = PhotoImage(file='images/submit.gif')

        # Buttons to submit the attempt, _speak the word, and _speak the example.
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
        if tkMessageBox.askokcancel('Exit', 'Are you sure you want to exit? Your progress will be saved.'):
            if self.session:
                # If there was an ongoing session, end it.
                self._end_session()
            
            # Create the welcome screen, destroy this view, show the welcome
            # screen.
            ws = WelcomeScreen(self.user, master=self.master)
            self.destroy()
            ws.pack()
        
    def _start_session(self, *args):
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
            
            # Bind return to submitting a word.
            self.master.bind('<Return>', self._submit)
            
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
        self.word_lbl.config(text='Enter the word you hear and click submit!', fg='black')
        
        # Enable the list selection option menu.
        self.lists_opt.config(state=NORMAL)
        
        # Disable the spelling aid controls.
        self.speak_again_btn.config(state=DISABLED)
        self.example_btn.config(state=DISABLED)
        self.word_ebx.config(state=DISABLED)
        self.word_submit_btn.config(state=DISABLED)
        
        # Show the statistics from the completed session.
        sc = SpellingComplete(self, self.lists_model.get_list_name(), score, highscore, newhighscore, attempts)
        
        # Bind return to begin session button.
        self.master.bind('<Return>', self._start_session)
        
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
            self.word_lbl.config(text='Enter the word you hear and click submit!', fg='black')

class SpellingComplete(Dialog):
    '''Summary of the students performance after a spelling session.'''
    def __init__(self, master, listname, score, highscore, newhighscore, attempts):
        '''Create the spelling complete dialog.
        
        Arguments:
        master -- Parent window.
        listname -- Name of the list that was being played.
        score -- The final score of the seesion.
        highscore -- The high score of the list being played.
        newhighscore -- Boolean representing whether or not the user set a new
        high score.
        attempts -- The words that the user submitted during the session.
        
        '''
        self.list = listname
        self.score = score
        self.highscore = highscore
        self.newhighscore = newhighscore
        self.attempts = attempts
        
        Dialog.__init__(self, master, 'Well done', 0)  
                    
    def _build(self):
        '''Create the dialog widgets.'''
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
        
        # Print the attempts in a two columned list with red text for an
        # incorrect submission.
        for key, value in self.attempts.iteritems():
            if key == value:
                self.attempt_keys.append(Label(self.attempts_frame, text=key + ':', **helv12))
                self.attempt_values.append(Label(self.attempts_frame, text=value, **helv12))
            else:
                self.attempt_keys.append(Label(self.attempts_frame, text=key + ':', fg='red', **helv12))
                self.attempt_values.append(Label(self.attempts_frame, text=value, fg='red', **helv12))

        if self.newhighscore:
            # If a new highscore was set, congratulate the user.
            self.congratulations_lbl = Label(self, text='New high score!', fg='orange', **helv16)
        else:
            # Otherwise, be less nice.
            self.congratulations_lbl = Label(self, text='Well done!', fg='brown', font=('Helvetica', '14'))
        
    def _arrange(self):
        '''Arrange the dialog widgets.'''
        self.list_complete_lbl.grid(column=0, row=0, **pad2)
        
        self._score_frame.grid(column=0, row=1, sticky='we', **pad5)
        
        self.congratulations_lbl.grid(column=0, row=2, **pad2)
        
        self.attempts_frame.grid(column=0, row=3, sticky='we', **pad5)
        
        # Arrange the submitted attempts in a two column list which will
        # overflow into two more columns after ten entries.
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
    '''Scores of a student for all available lists.
    
    Public functions:
    update_metadata -- Get and show the score information about a list.
    
    '''
    def __init__(self, user, master=None, title=None):
        '''Create the dialog.
        
        Arguments:
        user -- User whose scores to look up.
        master -- Parent window.
        title -- Title of the dialog window.
        
        '''
        self.user = user
        Dialog.__init__(self, master, btncolumn=0, title=title)
          
    def _build(self):
        '''Create the score dialog widgets.'''
        self.list_metadata = LabelFrame(self, text='Score', **pad5)
        
        # Labels
        self.num_words_lbl = Label(self.list_metadata, text='Number of words:', **helv12)
        self.difficulty_lbl = Label(self.list_metadata, text='Average word length:', **helv12)
        self.num_attempts_lbl = Label(self.list_metadata, text='Number of attempts:', **helv12)
        self.high_score_lbl = Label(self.list_metadata, text='High score:', **helv12)
        self.list_metadata_labels = [self.num_words_lbl, self.difficulty_lbl, 
                                     self.num_attempts_lbl, self.high_score_lbl]
        
        # Score data
        self.list_num_words_lbl = Label(self.list_metadata, text='0', **helv16)
        self.list_difficulty_lbl = Label(self.list_metadata, text='0', **helv16)
        self.list_num_attempts_lbl = Label(self.list_metadata, text='0', **helv16)
        self.list_high_score_lbl = Label(self.list_metadata, text='0', **helv16)
        self.list_metadata_fields = [self.list_num_words_lbl, self.list_difficulty_lbl,
                                     self.list_num_attempts_lbl, self.list_high_score_lbl]
        
        # Option menu to choose the list which is being inspected.
        self.lists_frame = LabelFrame(self, text='Lists', **pad5)
        self.lists_var = StringVar()
        self.lists_opt = OptionMenu(self.lists_frame, self.lists_var, '')
        self.lists_opt.config(anchor='w')
        
        # Model to get information about the tldr lists.
        self.lists_model = TLDROptionMenuModel(self.lists_opt, self.lists_var)
        self.lists_var.trace('w', self.update_metadata)
        
        # Dirty hack to cause the metadata to update on the initial opening of
        # the window.
        self.lists_var.set(self.lists_var.get())
        
    def _arrange(self):
        '''Arrange the score dialog widgets.'''
        self.lists_frame.grid(column=0, row=0, sticky='nswe', **pad5)
        self.lists_opt.grid(sticky='we', **pad2)
        
        self.list_metadata.grid(column=0, row=1, sticky='nswe', **pad5)
                
        for i, label in enumerate(self.list_metadata_labels):
            label.grid(column=0, row=i, sticky='w', **pad2)
        
        for i, label in enumerate(self.list_metadata_fields):
            label.grid(column=1, row=i, sticky='w',  **pad2)
            
    def update_metadata(self, *args):
        '''Update the score information.'''
        # Get the currently selected list from the option menu.
        wordlist = self.lists_model.get_list()

        if wordlist:
            # Set the number of words label.
            self.list_num_words_lbl.config(text=str(len(wordlist.words)))
        
            # Calculate the total length of all words in the list.
            length = 0
            for key in wordlist.words.iterkeys():
                length += len(key)
            
            # Calculate the average word length.
            if length == 0:
                difficulty = 0
            else:
                difficulty = length/len(wordlist.words.keys())
            
            self.list_difficulty_lbl.config(text=str(difficulty))
            
            try:
                # Get the number of attempts the user has made at this list.
                attempts = len(self.user._scores[wordlist.name])
            except KeyError:
                # If they haven't made any attempts then:
                attempts = 0
                
            self.list_num_attempts_lbl.config(text=str(attempts))
            
            # Get the user high score.
            highscore = self.user.high_score(wordlist.name)
            self.list_high_score_lbl.config(text=str(highscore))
        else:
            pass

class Administration(Frame):
    '''Frame to hold list and user management tabs.'''
    def __init__(self, master=None):
        '''Build the administration frame.'''
        Frame.__init__(self, master)
        self.master.title('Administration')
        self._build()
        self._arrange()
        
    def _build(self):
        '''Create the list and user management views and the tabs to control
        switching between them.'''
        um = UserManagement(self)
        lm = ListManagement(self)
                
        tabs = {'Manage Users': um, 'Manage Lists': lm}
        
        self.tabs = TabBar(self, tabs=tabs)
        
        # Create the logout button.
        self.logout = Button(self, text='Log out', command=self._log_out)
        
    def _arrange(self):
        '''Arrange the widgets. The tab bar handles arranging the user and list
        management views.'''
        self.tabs.grid(row=0, column=0, sticky='we')
        self.logout.grid(row=2, column=0, sticky='e', **pad5)
        
    def _log_out(self):
        '''Return to the logon screen.'''
        if tkMessageBox.askokcancel('Log out', 'Are you sure you want to log out?'):
            logon = Logon(self.master)
            self.destroy()
            logon.grid()
            
class ListManagement(Frame):
    '''Let administrators edit, import, delete and create new lists.

    Public functions:
    new_list -- Open the new list dialog.
    delete_list -- Move a list to the trash.
    list_edit -- Open the list edit dialog.
    import_list -- Import a tldr from an outside source.

    '''
    def __init__(self, master=None):
        '''Build and arrange the list management view.'''
        Frame.__init__(self, master)
        self._build()
        self._arrange()
        
    def _build(self):
        '''Build the widgets.'''
        # Create a list containing a 4-tuple in order to initialise the multi-
        # column listbox with four columns.
        items = [(0, 0, 0, 0)]
        
        # Create the headers to pass to the multi-column listbox.
        headers =['List name', 'List author', 'Date last edited', 'Number of words']
        
        # Multi-column listbox and it's underlying model.
        self.manage_lists_frame = LabelFrame(self, text='Manage lists', **pad5)
        self.list_lbx = MultiScrollListbox(self.manage_lists_frame, items, headers)
        self.list_model = TLDRMultiScrollListbox(self.list_lbx)
        
        # List controls.
        self.new_list_btn = Button(self.manage_lists_frame, text='New list', command=self.new_list)
        self.delete_list_btn = Button(self.manage_lists_frame, text='Delete list', command=self.delete_list)
        self.edit_list_btn = Button(self.manage_lists_frame, text='Edit list', command=self.list_edit)
        self.import_list_btn = Button(self.manage_lists_frame, text='Import list', command=self.import_list)
        
        self.controls = [self.new_list_btn, self.delete_list_btn,
                         self.edit_list_btn, self.import_list_btn]

    def _arrange(self):
        '''Arrange the widgets.'''
        self.manage_lists_frame.grid(**pad5)
        
        self.list_lbx.grid(column=0, row=0, rowspan=4, **pad5)
        
        for i, control in enumerate(self.controls):
            control.grid(column=1, row=i, sticky='we', padx=5, pady=2)
            
    def new_list(self):
        '''Open the new list dialog.'''
        nl = NewList(master=self, title='New list', btncolumn=0)
        new_lists = self.list_model.update_items()
        
        # If a list was created, open the list edit window to let the user
        # add words.
        if new_lists:         
            self.list_edit(new_lists[0])
            
    def delete_list(self):
        '''Delete a list.'''
        if tkMessageBox.askokcancel('Delete list', 'Are you sure you want to delete ' + self.list_lbx.get() + '?'):
            self.list_model.delete()
            
    def list_edit(self, list=None):
        '''Open the list edit dialog.
        
        Arguments:
        list - The name of the list to be edited.
        
        '''
        if list:
            le = ListEdit(list, master=self)
        elif self.list_lbx.get():
            le = ListEdit(self.list_lbx.get(), master=self)
        else:
            tkMessageBox.showerror('Error', 'Please select a list to edit.')
        
    def import_list(self):
        '''Open a file dialog to find a list to import.'''
        listfile = tkFileDialog.askopenfilename(filetypes=[('tldr files', '.tldr')])
        if listfile != '':
            self.list_model.import_list(listfile)

class NewList(Dialog):
    '''Dialog where new list information is given by the user.'''
    def _build(self):
        '''Create the widgets.'''
        # Field labels.
        self.list_information_frame = LabelFrame(self, text='List details', **pad5)
        self.name_lbl = Label(self.list_information_frame, text='Name:')
        self.author_lbl = Label(self.list_information_frame, text='Author:')
        
        # Entry fields for list information.
        self.name_ebx = Entry(self.list_information_frame)
        self.author_ebx = Entry(self.list_information_frame)
        
        self.labels = [self.name_lbl, self.author_lbl]
        self.fields = [self.name_ebx, self.author_ebx]

    def _arrange(self):
        '''Arrange the widgets.'''
        self.list_information_frame.grid(column=0, row=0, sticky='nswe', **pad5)
        
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i, sticky='nw', **pad2)
            
        for i, field in enumerate(self.fields):
            field.grid(column=1, row=i, sticky='we', **pad2)
        
    def _validate(self):
        '''Check that a name and author were supplied.'''
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
        '''Generate an empty word list with the given information.'''
        name = self.name_ebx.get()
        author = self.author_ebx.get()
        path = 'wordlists/' + name + '.tldr'
        
        tldr.generate_empty_tldr(path, name, author)
        
class ListEdit(Dialog):
    '''Add and remove words from lists.
    
    Public functions:
    update_metadata -- Update the word metadata labels.
    reset_metadata -- Reset the word metadata labels to show no information.
    
    '''
    def __init__(self, listname, master=None):
        ''' Create the list edit dialog.
        
        Arguments:
        listname -- Name of the list being edited.
        master -- Parent window.
        
        '''
        self.listname = listname
        self.word = None
        
        Dialog.__init__(self, master, title='Edit ' + listname, btncolumn=0)
    
    def _build(self):
        '''Create the list edit dialog widgets.'''
        self.source_frame = LabelFrame(self, text='Source', **pad5)
        # Optionmenu containing all of the word sources.
        self.source_var = StringVar()
        self.source_opt = OptionMenu(self.source_frame, self.source_var, *difficulties)
        # Listbox containing the words from the source and a filter to help
        # find words.
        self.source_words_lbx = ScrollListbox(self.source_frame)
        self.source_filter_var = StringVar()
        self.source_filter_ebx = Entry(self.source_frame, textvariable=self.source_filter_var)
        # Underlying model of the source words.
        self.source_model = WordSourceModel(self, self.source_opt, self.source_var, self.source_words_lbx, self.source_filter_ebx, self.source_filter_var)
        
        self.source_var.set('CL1')

        # Control column to let the user add and remove words from the
        # destination list.
        self.control_column = Frame(self)
        self.add_btn = Button(self.control_column, text='Add word >', command=self._add_word)
        self.add_all_btn = Button(self.control_column, text='Add all words >>', command=self._add_all_words)
        self.add_x_btn = Button(self.control_column, text='Add x words >', command=self._add_x_words)
        self.x_ebx = Entry(self.control_column, width=10)
        self.x_ebx.insert(END, 'x')
        self.remove_btn = Button(self.control_column, text='Remove word', command=self._remove_word)
        self.remove_all_btn = Button(self.control_column, text='Remove all words', command=self._remove_all_words)
        self.new_word_btn = Button(self.control_column, text='Add new word', command=self._new_word)
        
        self.control_column_elements = [self.add_btn, self.add_all_btn, self.add_x_btn, self.x_ebx,
                                        self.remove_btn, self.remove_all_btn, self.new_word_btn]
        
        # Destination list widgets.
        self.destination_frame = LabelFrame(self, text=self.listname, **pad5)
        self.destination_lbl = Label(self.destination_frame, text='List contents:')
        # Listbox containing all of the words currently in the destination list
        # that match the filter.
        self.destination_lbx = ScrollListbox(self.destination_frame)
        self.destination_filter_var = StringVar()
        self.destination_filter_ebx = Entry(self.destination_frame, textvariable=self.destination_filter_var)
        # Underlying model of the destination list.
        self.destination_model = WordDestinationModel(self, self.listname, self.destination_lbx, self.destination_filter_ebx, self.destination_filter_var)
        
        # Information about the currently selected word.
        self.word_metadata = LabelFrame(self, text='Word', **pad5)
        self.definition_lbl= Label(self.word_metadata, text='Definition:')
        self.example_lbl = Label(self.word_metadata, text='Example:')
        self.word_definition_lbl = Label(self.word_metadata, text='No definition', wraplength=500, justify=LEFT)
        self.word_example_lbl = Label(self.word_metadata, text='No example', wraplength=500,justify=LEFT)
        self.speak_btn = Button(self.word_metadata, text='Speak', command=self._speak)
                
    def _arrange(self):
        '''Place the list edit dialog widgets.'''
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
        
    def _add_word(self):
        '''Add the selected word from the source list to the destination
        list.'''
        if self.word:
            self.destination_model._add_word(self.source_model.get_word())
        else:
            tkMessageBox.showerror('Error', 'No word selected')

    def _add_all_words(self):
        '''Add all words that match the source filter to the destination list.'''
        self.destination_model.add_words(self.source_model.get_words())
    
    def _add_x_words(self):
        '''Add a random selected of words from the selected source to the
        destination list.'''
        try:
            x = int(self.x_ebx.get())
            words = self.source_model.get_words()
            
            keys = words.keys()
            random.shuffle(keys)
            
            try:
                for i in range(0, x):
                    self.destination_model._add_word(words[keys.pop()])
            except IndexError:
                pass
                        
        except ValueError:
            tkMessageBox.showerror('Error', 'Please enter a number')
            
    def _remove_word(self):
        '''Remove the currently selected word from the destination list.'''
        if self.word:
            self.destination_model._remove_word(self.word)
        else:
            tkMessageBox.showerror('Error', 'No word selected')
            
    def _remove_all_words(self):
        '''Remove all words from the destination list.'''
        self.destination_model._remove_all_words()
                    
    def _speak(self):
        '''Speak the currently selected word.'''
        if self.word:
            speech = Speech()
            speech._speak(self.word.word)
        else:
            tkMessageBox.showerror('Error', 'No word selected')
                
    def _new_word(self):
        '''Open the new word dialog.'''
        nw = NewWord(self.destination_model, master=self)
        
    def _validate(self):
        '''Ask the user if they want to save their changes to the destination
        list.'''
        return tkMessageBox.askokcancel('Save new list', 'Save changes to ' + self.listname + '?')
    
    def _apply(self):
        '''Save changes to the destination list and update the list management
        view to reflect them.'''
        self.destination_model.save()
        self.master.list_model.update_items()

    def update_metadata(self, word):
        '''Update the word metadata.
        
        Arguments:
        word -- Word obect containing the necessary metadata.
        
        '''
        self.word = word
        self.word_definition_lbl.config(text=word.definition)
        self.word_example_lbl.config(text=word.example)
        
    def reset_metadata(self):
        '''Reset the metadata to show no information. Usually called after a
        word has been deleted.'''
        self.word = None
        self.word_definition_lbl.config(text='No definition')
        self.word_example_lbl.config(text='No example')

class NewWord(Dialog):
    '''Dialog where new word information is given by the user.'''
    def __init__(self, model, master=None):
        '''Create the new word dialog.
        
        Arguments:
        model -- Model of the destination list of the list edit dialog.
        master -- Parent window.
        
        '''
        self.model = model
        
        Dialog.__init__(self, master, title='New word', btncolumn=0)
    
    def _build(self):
        '''Create the new word dialog widgets.'''
        # Labels
        self.word_information_frame = LabelFrame(self, text='Word details', **pad5)
        self.word_lbl = Label(self.word_information_frame, text='Word:')
        self.definition_lbl = Label(self.word_information_frame, text='Definition:')
        self.example_lbl = Label(self.word_information_frame, text='Example:')
        self.difficulty_lbl = Label(self.word_information_frame, text='Difficulty:')
        
        # Fields
        self.difficulty_var = StringVar()
        self.difficulty_opt = OptionMenu(self.word_information_frame, self.difficulty_var, *difficulties)
        self.difficulty_var.set('CL1')
        
        self.word_ebx = Entry(self.word_information_frame)
        self.definition_ebx = Text(self.word_information_frame, width=30, height=4)
        self.example_ebx = Text(self.word_information_frame, width=30, height=4)
        
        self.labels = [self.word_lbl, self.definition_lbl, self.example_lbl, self.difficulty_lbl]
        self.fields = [self.word_ebx, self.definition_ebx, self.example_ebx, self.difficulty_opt]
        
    def _arrange(self):
        '''Arrange the new word dialog widgets.'''
        self.word_information_frame.grid(column=0, row=0, sticky='nswe', **pad5)
        
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i, sticky='nw', **pad2)
            
        for i, field in enumerate(self.fields):
            field.grid(column=1, row=i, sticky='we', **pad2)
            
    def _validate(self):
        '''Check that a word, definition, and example were supplied.'''
        if self.word_ebx.get() == '':
            tkMessageBox.showerror('Error', 'Please enter a word.')
            return False
            
        if self.definition_ebx.get(1.0, END) == '':
            tkMessageBox.showerror('Error', 'Please enter a definition.')
            return False

        if self.example_ebx.get(1.0, END) == '':
            tkMessageBox.showerror('Error', 'Please enter an example.')
            return False

        return True
    
    def _apply(self):
        '''Create a new word object and add it to the model.'''
        word = Word(self.word_ebx.get(), self.definition_ebx.get(1.0, END).strip(), self.example_ebx.get(1.0, END).strip(), self.difficulty_var.get())
        self.model._add_word(word)
            
class UserManagement(Frame):
    '''Let administrators delete users, create new users, and view user
    scores.'''
    def __init__(self, master=None):
        '''Create the user management view.'''
        Frame.__init__(self, master)
        self._build()
        self._arrange()
        
    def _build(self):
        '''Build the user management widgets.'''
        # Construct a list with a 3-tuple to pass to the multi-column listbox
        # to initialise it with three columns.
        items = [(0, 0, 0)]
        
        # The list of column headers to pass to the multi-column listbox.
        headers = ['Username', 'Real name', 'Date of birth']

        self.manage_users_frame = LabelFrame(self, text='Manage users', **pad5)
        
        # The mult-column listbox and the underlying model.
        self.user_lbx = MultiScrollListbox(self.manage_users_frame, items, headers)
        self.user_model = UserListModel(self.user_lbx)
        
        # User controls.
        self.new_user_btn = Button(self.manage_users_frame, text='New user', command=self._new_user)
        self.delete_user_btn = Button(self.manage_users_frame, text='Delete user', command=self._delete_user)
        self.user_score_btn = Button(self.manage_users_frame, text='View scores', command=self._scores)
        
        self.controls = [self.new_user_btn, self.delete_user_btn,
                         self.user_score_btn]

    def _arrange(self):
        '''Arrange the user management widgets.'''
        self.manage_users_frame.grid(**pad5)
        
        self.user_lbx.grid(column=0, row=0, rowspan=4, **pad5)
        
        for i, control in enumerate(self.controls):
            control.grid(column=1, row=i, sticky='we', padx=5, pady=2)
            
    def _new_user(self):
        '''Open the new user dialog.'''
        nu = NewUser(self, btncolumn=0, title='Add user')
        # After a user has been added to the database, update the listbox items.
        self.user_model.update_items()
        
    def _delete_user(self):
        '''Remove a user.'''
        if tkMessageBox.askokcancel('Delete user', 'Delete ' + self.user_lbx.get() + '?'):
            self.user_model._delete_user()
        
    def _scores(self):
        '''Show user scores.'''
        sc = Score(self.user_model.user, master=self, title='Scores')

class NewUser(Dialog):
    '''Dialog where new user information is given by the user.'''
    def _build(self):
        '''Create the new user dialog widgets.'''
        self.register_frame = LabelFrame(self, text='New user', **pad5)
        
        # Labels
        self.username_lbl = Label(self.register_frame, text='Username:')
        self.realname_lbl = Label(self.register_frame, text='Real name:')
        self.password_lbl = Label(self.register_frame, text='Password:')
        self.password_confirmation_lbl = Label(self.register_frame, text='Confirm password:')
        self.dob_lbl = Label(self.register_frame, text='Date of birth:')
        self.photo_lbl = Label(self.register_frame, text='Photo:')
        
        self.labels = [self.username_lbl, self.realname_lbl, self.password_lbl, 
                       self.password_confirmation_lbl, self.dob_lbl,
                       self.photo_lbl]
        
        # Fields
        self.username_ebx = Entry(self.register_frame)
        self.realname_ebx = Entry(self.register_frame)
        self.password_ebx = Entry(self.register_frame, show='*')
        self.password_confirmation_ebx = Entry(self.register_frame, show='*')
        self.dob_ebx = DateEntry(self.register_frame)
        
        self.photo_fields = Frame(self.register_frame)
        self.photo_btn = Button(self.photo_fields, text='Browse', command=self._get_photo)
        self.photo_ebx = Entry(self.photo_fields, state=DISABLED)
        
        self.fields = [self.username_ebx, self.realname_ebx, self.password_ebx,
                       self.password_confirmation_ebx, self.dob_ebx,
                       self.photo_fields]
        
    def _arrange(self):
        '''Arrange the new user dialog widgets.'''
        self.register_frame.grid(column=0, row=0, **pad5)
                
        self.photo_ebx.grid(column=0, row=0, sticky='we')
        self.photo_btn.grid(column=1, row=0, padx=2, sticky='e')
        
        for i, widget in enumerate(self.labels):
            widget.grid(column=0, row=i, sticky='w', **pad2)
            
        for i, widget in enumerate(self.fields):
            widget.grid(column=1, row=i, sticky='we', **pad2)
            
    def _get_photo(self):
        '''Get the path of the photo to be associated with the new user.'''
        # Enable the photo entry box to put the path to the photo there.
        self.photo_ebx.config(state=NORMAL)
        # Get the photo path.
        self.photo_ebx.insert(END, tkFileDialog.askopenfilename(filetypes=[('image files', '.gif')]))
        # Disable the photo entry box.
        self.photo_ebx.config(state='readonly')
            
    def _validate(self):
        '''Check that a username, real name, matching passwords, date of birth
        were all provided.'''
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
        
        # Create a user object and add it to the database.
        self.user = User(username, realname, password, dob, photo)
        self.um = database.get_user_manager()
        
        if not self.um.add_user(self.user):
            tkMessageBox.showerror('Error', 'A user with that username already exists.')
            return False
        
        return tkMessageBox.askyesno('New user', 'Create user ' + username + '?')
        
    def _apply(self):
        '''Save the new user to the database.'''
        self.um.commit()
        tkMessageBox.showinfo('User added', 'User ' + self.user.username + ' added successfully.')
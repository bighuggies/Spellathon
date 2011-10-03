'''
Created on Sep 29, 2011

@author: ahug048
'''
from Tkinter import *
from widgets import Dialog, ScrollListbox, TabBar, MultiScrollListbox

pad2 = {'padx' : 2, 'pady' : 2}
pad5 = {'padx' : 5, 'pady' : 5}

class ListManagement(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.build()
        self.arrange()
        
    def build(self):
        #####
        items = []
    
        for i in range(1,50):
            items.append((i, i, i))
        #####
        
        self.manage_lists_frame = LabelFrame(self, text="Manage lists", **pad5)
        
        self.list_lbx = MultiScrollListbox(self.manage_lists_frame, items)
        
        self.new_list_btn = Button(self.manage_lists_frame, text="New list")
        self.delete_list_btn = Button(self.manage_lists_frame, text="Delete list")
        self.edit_list_btn = Button(self.manage_lists_frame, text="Edit list")
        self.import_list_btn = Button(self.manage_lists_frame, text="Import list")
        
        self.controls = [self.new_list_btn, self.delete_list_btn,
                         self.edit_list_btn, self.import_list_btn]

    def arrange(self):
        self.manage_lists_frame.grid(**pad5)
        
        self.list_lbx.grid(column=0, row=0, rowspan=4, **pad5)
        
        for i, control in enumerate(self.controls):
            control.grid(column=1, row=i, sticky="we", padx=5, pady=2)

class UserManagement(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.build()
        self.arrange()
        
    def build(self):
        #####
        items = []
    
        for i in range(1,50):
            items.append((i, i, i))
        #####
        
        self.manage_users_frame = LabelFrame(self, text="Manage users", **pad5)
        
        self.user_lbx = MultiScrollListbox(self.manage_users_frame, items)
        
        self.new_user_btn = Button(self.manage_users_frame, text="New user")
        self.delete_user_btn = Button(self.manage_users_frame, text="Delete user")
        self.edit_user_btn = Button(self.manage_users_frame, text="Edit user")
        self.user_score_btn = Button(self.manage_users_frame, text="View scores")
        
        self.controls = [self.new_user_btn, self.delete_user_btn,
                         self.edit_user_btn, self.user_score_btn]

    def arrange(self):
        self.manage_users_frame.grid(**pad5)
        
        self.user_lbx.grid(column=0, row=0, rowspan=4, **pad5)
        
        for i, control in enumerate(self.controls):
            control.grid(column=1, row=i, sticky="we", padx=5, pady=2)
        
class Administration(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.build()
        self.arrange()
        
    def build(self):
        um = UserManagement(self)
        lm = ListManagement(self)
                
        tabs = {"Manage Users": um, "Manage Lists": lm}
        
        self.tabs = TabBar(self, tabs=tabs)
        
    def arrange(self):
        self.tabs.grid(row=0, column=0)

class Logon(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.build()
        self.arrange()
        
    def build(self):
        self.logo = PhotoImage(file="placeholder.gif")
        self.logo_lbl = Label(self, image=self.logo)
        
        self.loginframe = LabelFrame(self, text="Login", **pad5)
        self.username_lbl = Label(self.loginframe, text="Username:", width=35)
        self.password_lbl = Label(self.loginframe, text="Password:")
        self.username_ebx = Entry(self.loginframe)
        self.password_ebx = Entry(self.loginframe, show="*")
        self.login_btn = Button(self.loginframe, text="Login")
        self.new_user_btn = Button(self.loginframe, text="New user")
        
        self.userinfo = [self.username_lbl, self.username_ebx, 
                         self.password_lbl, self.password_ebx, self.login_btn, self.new_user_btn]

        self.administrate_btn = Button(self, text="Administrate")

        self.elements = [self.logo_lbl, self.loginframe, self.administrate_btn]
        
    def arrange(self):
        # Arrange the picture, the login fields, and the administration panel
        for i, element in enumerate(self.elements):
            element.grid(column=0, row=i, sticky="we", **pad5)
                
        # Arrange the login labels and fields
        for i, widget in enumerate(self.userinfo):
            widget.grid(column=0, row=i, sticky="we", **pad2)

class UserRegistration(Dialog):        
    def build(self):
        self.register_frame = LabelFrame(self, text="New user", **pad5)
        
        self.username_lbl = Label(self.register_frame, text="Username:")
        self.password_lbl = Label(self.register_frame, text="Password:")
        self.password_confirmation_lbl = Label(self.register_frame, text="Confirm password:")
        self.age_lbl = Label(self.register_frame, text="Age:")
        self.photo_lbl = Label(self.register_frame, text="Photo:")
        self.user_type_lbl = Label(self.register_frame, text="User type:")
        
        self.labels = [self.username_lbl, self.password_lbl, 
                       self.password_confirmation_lbl, self.age_lbl,
                       self.photo_lbl, self.user_type_lbl]
        
        self.username_ebx = Entry(self.register_frame)
        self.password_ebx = Entry(self.register_frame, show="*")
        self.password_confirmation_ebx = Entry(self.register_frame, show="*")
        self.age_ebx = Entry(self.register_frame)
        
        self.photo_fields = Frame(self.register_frame)
        self.photo_btn = Button(self.photo_fields, text="Browse")
        self.photo_ebx = Entry(self.photo_fields)
        
        self.user_type_var = StringVar()
        self.user_type_var.set("Student")
        
        self.user_type = Frame(self.register_frame)
        
        self.student_rbn = Radiobutton(self.user_type, text="Student", variable=self.user_type_var, value="Student")
        self.teacher_rbn = Radiobutton(self.user_type, text="Teacher", variable=self.user_type_var, value="Teacher")

        self.fields = [self.username_ebx, self.password_ebx,
                       self.password_confirmation_ebx, self.age_ebx,
                       self.photo_fields, self.user_type]
        
        self.user_type_var = StringVar()
        
    def arrange(self):
        self.register_frame.grid(column=0, row=0, **pad5)
        
        self.student_rbn.grid(column=0, row=0, sticky="w", **pad2)
        self.teacher_rbn.grid(column=1, row=0, sticky="w", **pad2)
        
        self.photo_ebx.grid(column=0, row=0, sticky="we")
        self.photo_btn.grid(column=1, row=0, padx=2, sticky="we")
        
        for i, widget in enumerate(self.labels):
            widget.grid(column=0, row=i, sticky="w", **pad2)
            
        for i, widget in enumerate(self.fields):
            widget.grid(column=1, row=i, sticky="we", **pad2)
            
class Authoriser(Dialog):
    def build(self):
        self.authority_frame = LabelFrame(self, text="Provide authority", **pad5)
        self.password_lbl = Label(self.authority_frame, text="Enter administrator password:")
        self.password_ebx = Entry(self.authority_frame, show="*", width=25)
        
    def arrange(self):
        self.password_lbl.grid(sticky="w", **pad2)
        self.password_ebx.grid(sticky="we", **pad2)
        self.authority_frame.grid(column=0, row=0, sticky="we", **pad5)
        
class CreateAdmin(Dialog):
    def build(self):
        self.frame = LabelFrame(self, text="Create administrator", **pad5)
        self.info_lbl = Label(self.frame, text="Welcome to Spellathon! It appears " + 
                              "that you have not set an administrator " + 
                              "password. An administrator password is " + 
                              "necessary to create and manage word lists and " + 
                              "user records. Please set one now:", justify=LEFT, wraplength=300)
        self.password_lbl = Label(self.frame, text="Password:")
        self.password_confirm_lbl = Label(self.frame, text="Confirm password:")
        self.password_ebx = Entry(self.frame, show="*")
        self.password_confirm_ebx = Entry(self.frame, show="*")
        
    def arrange(self):
        self.info_lbl.grid(row=0, sticky="w", columnspan=2, **pad2)
        self.password_lbl.grid(column=0, row=1, sticky="w", **pad2)
        self.password_confirm_lbl.grid(column=0, row=2, sticky="w", **pad2)
        self.password_ebx.grid(column=1, row=1, sticky="w", **pad2)
        self.password_confirm_ebx.grid(column=1, row=2, sticky="w", **pad2)
        self.frame.grid(sticky="we", **pad5)
        
class WelcomeScreen(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.resizable(False, False)
        self.build()
        self.arrange()
        
    def build(self):
        self.welcome_frame = LabelFrame(self, text="Welcome", **pad5)
        self.welcome_lbl = Label(self.welcome_frame, text="Welcome! Choose your action:")
        self.spelling_btn = Button(self.welcome_frame, text="Begin Spelling", width=20, height=5)
        self.score_btn = Button(self.welcome_frame, text="View Scores", width=20, height=5)
        
    def arrange(self):
        self.welcome_frame.grid(**pad5)
        self.welcome_lbl.grid(**pad2)
        self.spelling_btn.grid(**pad2)
        self.score_btn.grid(**pad2)
        
class SpellingAid(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.resizable(False, False)
        self.build()
        self.arrange()
        
    def build(self):
        self.word_metadata = LabelFrame(self, text="Word")
        
        self.lists_var = StringVar()
        self.lists_var.set("test")
        self.lists_opt = OptionMenu(self, self.lists_var, "test", "test2")
        self.start_spelling_btn = Button(self, text="Start spelling")
        
        self.definition_lbl= Label(self.word_metadata, text="Definition:")
        self.example_lbl = Label(self.word_metadata, text="Example:")
        self.word_definition_lbl = Label(self.word_metadata, text="No definition", wraplength=200)
        self.word_example_lbl = Label(self.word_metadata, text="No example", wraplength=200)
        self.speak_again_btn = Button(self.word_metadata, text="Speak again")
        
        self.word_ebx= Entry(self, font=("Helvetica", 16), width=30)
        self.word_submit_btn = Button(self, text="Submit")
        
        self.score = LabelFrame(self, text="Score", **pad5)
        self.score_lbl = Label(self.score, text="Score:")
        self.current_score_lbl= Label(self.score, text="0/0")
        self.high_score_lbl = Label(self.score, text="High score:")
        self.current_high_score_lbl = Label(self.score, text="n/a")
        self.score_elements = [self.score_lbl, self.current_score_lbl,
                               self.high_score_lbl, self.current_high_score_lbl]
        
        self.exit_btn= Button(self, text="Exit")
        
    def arrange(self):
        self.lists_opt.grid(column=0, row=0, sticky="we", padx=5, pady=2)
        self.start_spelling_btn.grid(column=1, row=0, padx=5, pady=2)
        
        self.word_metadata.grid(column=0, row=1, sticky="we", columnspan=2, **pad5)

        self.word_ebx.grid(column=0, row=2, padx=5, pady=2)
        self.word_submit_btn.grid(column=1, row=2, sticky="we", padx=5, pady=2)
        
        self.score.grid(column=0, row=3, sticky="we", columnspan=2, **pad5)
        
        self.exit_btn.grid(column=1, row=4, sticky="we", padx=5, pady=2)
        
        for i, widget in enumerate(self.score_elements):
            widget.grid(column=i, row=0, sticky="w", **pad2)
                    
        self.definition_lbl.grid(column=0, row=0, sticky="w", **pad2)
        self.example_lbl.grid(column=0, row=1, sticky="w", **pad2)
        self.word_definition_lbl.grid(column=1, row=0, sticky="w", **pad2)
        self.word_example_lbl.grid(column=1, row=1, sticky="w", **pad2)
        self.speak_again_btn.grid(column=0, row=2, sticky="w", columnspan=2, **pad2)
        
class SpellingComplete(Dialog):
    def build(self):
        self.list_complete_lbl = Label(self, text="You have completed list x")
        

        self.score = LabelFrame(self, text="Score", **pad5)
        self.score_lbl = Label(self.score, text="Score:")
        self.current_score_lbl= Label(self.score, text="0/0")
        self.high_score_lbl = Label(self.score, text="High score:")
        self.current_high_score_lbl = Label(self.score, text="n/a")
        self.score_elements = [self.score_lbl, self.current_score_lbl,
                               self.high_score_lbl, self.current_high_score_lbl]
        
        self.highscore_lbl = Label(self, text="New highscore!")
        
    def arrange(self):
        self.list_complete_lbl.grid(column=0, row=0, **pad2)
        
        self.score.grid(column=0, row=1, sticky="we", **pad5)
        
        self.highscore_lbl.grid(column=0, row=2, **pad2)

        for i, widget in enumerate(self.score_elements):
            widget.grid(column=0, row=i, sticky="w", **pad2)

class Score(Dialog):        
    def build(self):
        self.list_frame = LabelFrame(self, text="Lists", **pad5)
        self.lists_lbx = ScrollListbox(self.list_frame)
        
        self.list_metadata = LabelFrame(self, text="Score", **pad5)
        
        self.num_words_lbl = Label(self.list_metadata, text="Number of words:")
        self.difficulty_lbl = Label(self.list_metadata, text="Difficulty:")
        self.num_attempts_lbl = Label(self.list_metadata, text="Number of attempts:")
        self.high_score_lbl = Label(self.list_metadata, text="High score:")
        self.list_metadata_labels = [self.num_words_lbl, self.difficulty_lbl, 
                                     self.num_attempts_lbl, self.high_score_lbl]
        
        self.list_num_words_lbl = Label(self.list_metadata, text="0")
        self.list_difficulty_lbl = Label(self.list_metadata, text="None")
        self.list_num_attempts_lbl = Label(self.list_metadata, text="0")
        self.list_high_score_lbl = Label(self.list_metadata, text="0")
        self.list_metadata_fields = [self.list_num_words_lbl, self.list_difficulty_lbl,
                                     self.list_num_attempts_lbl, self.list_high_score_lbl]
        
        
    def arrange(self):
        self.list_frame.grid(column=0, row=0, sticky="nswe", **pad5)
        self.lists_lbx.grid(**pad2)
        
        self.list_metadata.grid(column=1, row=0, sticky="nswe", **pad5)
        
        for i, label in enumerate(self.list_metadata_labels):
            label.grid(column=0, row=i, sticky="w", **pad2)
            
        for i, label in enumerate(self.list_metadata_fields):
            label.grid(column=1, row=i, sticky="w",  **pad2)
        
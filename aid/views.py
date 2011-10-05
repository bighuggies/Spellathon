'''
Created on Sep 29, 2011

@author: ahug048
'''
from Tkinter import *
import hashlib
import tkMessageBox
import tkFileDialog
from user import User
from database import *
from widgets import Dialog, ScrollListbox, TabBar, MultiScrollListbox, DateEntry

pad2 = {'padx' : 2, 'pady' : 2}
pad5 = {'padx' : 5, 'pady' : 5}

class NewWord(Dialog):
    def build(self):
        self.word_information_frame = LabelFrame(self, text="Word details", **pad5)
        self.word_lbl = Label(self.word_information_frame, text="Word:")
        self.definition_lbl = Label(self.word_information_frame, text="Definition:")
        self.example_lbl = Label(self.word_information_frame, text="Example:")
        
        self.word_ebx = Entry(self.word_information_frame)
        self.definition_ebx = Text(self.word_information_frame, width=30, height=4)
        self.example_ebx = Text(self.word_information_frame, width=30, height=4)
        
        self.labels = [self.word_lbl, self.definition_lbl, self.example_lbl]
        self.fields = [self.word_ebx, self.definition_ebx, self.example_ebx]
        
    def arrange(self):
        self.word_information_frame.grid(column=0, row=0, sticky="nswe", **pad5)
        
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i, sticky="nw", **pad2)
            
        for i, field in enumerate(self.fields):
            field.grid(column=1, row=i, sticky="we", **pad2)

class ListEdit(Dialog):
    def build(self):
        self.source_frame = LabelFrame(self, text="Source", **pad5)
        self.destination_frame = LabelFrame(self, text="Destination", **pad5)
        
        self.source_var = StringVar()
        self.source_opt = OptionMenu(self.source_frame, self.source_var, "test", "test2")
        self.source_words_lbx = ScrollListbox(self.source_frame)
        self.source_filter_ebx = Entry(self.source_frame)
        
        self.control_column = Frame(self)
        self.add_btn = Button(self.control_column, text="Add word >")
        self.add_all_btn = Button(self.control_column, text="Add all words >>")
        self.add_x_btn = Button(self.control_column, text="Add x words >")
        self.remove_btn = Button(self.control_column, text="Remove word")
        self.remove_all_btn = Button(self.control_column, text="Remove all words")
        self.new_word_btn = Button(self.control_column, text="Add new word")
        
        self.control_column_elements = [self.add_btn, self.add_all_btn, self.add_x_btn,
                                        self.remove_btn, self.remove_all_btn, self.new_word_btn]
        
        self.destination_lbl = Label(self.destination_frame, text="List contents:")
        self.destination_lbx = ScrollListbox(self.destination_frame)
        self.destination_filter_ebx = Entry(self.destination_frame)
        
        
        self.word_metadata = LabelFrame(self, text="Word", **pad5)
                
        self.definition_lbl= Label(self.word_metadata, text="Definition:")
        self.example_lbl = Label(self.word_metadata, text="Example:")
        self.word_definition_lbl = Label(self.word_metadata, text="No definition", wraplength=200)
        self.word_example_lbl = Label(self.word_metadata, text="No example", wraplength=200)
        self.speak_btn = Button(self.word_metadata, text="Speak")
        
    def arrange(self):
        self.source_frame.grid(column=0, row=0, sticky="nswe", **pad5)
        
        self.source_opt.grid(column=0, row=0, **pad2)
        self.source_words_lbx.grid(column=0, row=1, sticky="nswe", **pad2)
        self.source_filter_ebx.grid(column=0, row=2, sticky="nswe", **pad2)
        
        self.control_column.grid(column=1, row=0, sticky="nswe", **pad5)
        
        for i, button in enumerate(self.control_column_elements):
            button.grid(column=0, row=i, sticky="we", **pad2)
            
        self.destination_frame.grid(column=2, row=0, sticky="nswe", **pad5)
        
        self.destination_lbl.grid(column=0, row=0, sticky="nsw", **pad2)
        self.destination_lbx.grid(column=0, row=1, sticky="nswe", **pad2)
        self.destination_filter_ebx.grid(column=0, row=2, sticky="nswe", **pad2)
        
        self.word_metadata.grid(column=0, row=1, columnspan=3, sticky="we", **pad5)
        
        self.definition_lbl.grid(column=0, row=0, sticky="w", **pad2)
        self.example_lbl.grid(column=0, row=1, sticky="w", **pad2)
        self.word_definition_lbl.grid(column=1, row=0, sticky="w", **pad2)
        self.word_example_lbl.grid(column=1, row=1, sticky="w", **pad2)
        self.speak_btn.grid(column=0, row=2, sticky="w", columnspan=2, **pad2)

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
        self.resizable(False, False)
        self.build()
        self.arrange()
        
    def build(self):
        um = UserManagement(self)
        lm = ListManagement(self)
                
        tabs = {"Manage Users": um, "Manage Lists": lm}
        
        self.tabs = TabBar(self, tabs=tabs)
        
    def arrange(self):
        self.tabs.grid(row=0, column=0)

class Logon(Toplevel):
    def __init__(self, parent=None):
        Toplevel.__init__(self, parent)
        self.title("Spellathon Logon")
        self.resizable(False, False)
        self.bind("<Return>", self.validate)
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
        
        self.login_btn = Button(self.loginframe, text="Login", command=self.validate)
        self.new_user_btn = Button(self.loginframe, text="New user", command=self.new_user)
        
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
            
    def new_user(self):
        nu = NewUser(self, btncolumn=0)
        
    def welcome_screen(self):
        ws = WelcomeScreen(self.master)
        
    def validate(self, *args):
        username = self.username_ebx.get()
        password = hashlib.sha224(username + self.password_ebx.get()).hexdigest()
        
        um = UserManager()
        user = um.retrieve_user(username)
        
        if user:
            if user.password == password:
                self.welcome_screen()
                self.destroy()
            else:
                tkMessageBox.showerror("Error", "Incorrect password")
        else:
            tkMessageBox.showerror("Error", "No such user")

class NewUser(Dialog):        
    def build(self):
        self.register_frame = LabelFrame(self, text="New user", **pad5)
        
        self.username_lbl = Label(self.register_frame, text="Username:")
        self.realname_lbl = Label(self.register_frame, text="Real name:")
        self.password_lbl = Label(self.register_frame, text="Password:")
        self.password_confirmation_lbl = Label(self.register_frame, text="Confirm password:")
        self.dob_lbl = Label(self.register_frame, text="Date of birth:")
        self.photo_lbl = Label(self.register_frame, text="Photo:")
        
        self.labels = [self.username_lbl, self.realname_lbl, self.password_lbl, 
                       self.password_confirmation_lbl, self.dob_lbl,
                       self.photo_lbl]
        
        self.username_ebx = Entry(self.register_frame)
        self.realname_ebx = Entry(self.register_frame)
        self.password_ebx = Entry(self.register_frame, show="*")
        self.password_confirmation_ebx = Entry(self.register_frame, show="*")
        self.dob_ebx = DateEntry(self.register_frame)
        
        self.photo_fields = Frame(self.register_frame)
        self.photo_btn = Button(self.photo_fields, text="Browse", command=self.get_photo)
        self.photo_ebx = Entry(self.photo_fields, state=DISABLED)
        
        self.fields = [self.username_ebx, self.realname_ebx, self.password_ebx,
                       self.password_confirmation_ebx, self.dob_ebx,
                       self.photo_fields]
        
    def arrange(self):
        self.register_frame.grid(column=0, row=0, **pad5)
                
        self.photo_ebx.grid(column=0, row=0, sticky="we")
        self.photo_btn.grid(column=1, row=0, padx=2, sticky="e")
        
        for i, widget in enumerate(self.labels):
            widget.grid(column=0, row=i, sticky="w", **pad2)
            
        for i, widget in enumerate(self.fields):
            widget.grid(column=1, row=i, sticky="we", **pad2)
            
    def get_photo(self):
        self.photo_ebx.config(state=NORMAL)
        self.photo_ebx.insert(END, tkFileDialog.askopenfilename(filetypes=[("image files", ".gif")]))
        self.photo_ebx.config(state="readonly")
            
    def validate(self):
        username = self.username_ebx.get()
        realname = self.realname_ebx.get()
        password = hashlib.sha224(username + self.password_ebx.get()).hexdigest()
        confpassword = hashlib.sha224(username + self.password_confirmation_ebx.get()).hexdigest()
        dob = self.dob_ebx.get()
        photo = self.photo_ebx.get()
        
        if username == "":
            tkMessageBox.showerror("Error", "Please enter a username.")
            return False

        if realname == "":
            tkMessageBox.showerror("Error", "Please enter your real name.")
            return False
        
        if self.password_ebx.get() == "":
            tkMessageBox.showerror("Error", "Please provide a password.")
            return False

        if password != confpassword:
            tkMessageBox.showerror("Error", "Passwords do not match.")
            return False
        
        self.user = User(username, realname, password, dob, photo)
        self.um = UserManager()
        
        if not self.um.add_user(self.user):
            tkMessageBox.showerror("Error", "A user with that username already exists.")
            return False
        
        return tkMessageBox.askyesno("New user", "Create user " + username + "?")
        
    def apply(self):
        self.um.commit()
        tkMessageBox.showinfo("User added", "User " + self.user.username + " added successfully.")
            
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
        
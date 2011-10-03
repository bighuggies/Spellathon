'''
Created on Sep 29, 2011

@author: ahug048
'''
from Tkinter import *
from widgets import Dialog

pad2 = {'padx' : 2, 'pady' : 2}

class Logon(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.build()
        self.arrange()
        
    def build(self):
        self.logo = PhotoImage(file="placeholder.gif")
        self.logo_lbl = Label(self, image=self.logo)
        
        self.loginframe = LabelFrame(self, text="Login", padx=5, pady=5)
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
            element.grid(column=0, row=i, padx=5, pady=5, sticky="we")
                
        # Arrange the login labels and fields
        for i, widget in enumerate(self.userinfo):
            widget.grid(column=0, row=i, sticky="we", **pad2)

class UserRegistration(Dialog):        
    def build(self):
        self.register_frame = LabelFrame(self, text="New user", padx=5, pady=5)
        
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
        self.register_frame.grid(column=0, row=0, padx=5, pady=5)
        
        self.student_rbn.grid(column=0, row=0, sticky="w", **pad2)
        self.teacher_rbn.grid(column=1, row=0, sticky="w", **pad2)
        
        self.photo_ebx.grid(column=0, row=0, sticky="we")
        self.photo_btn.grid(column=1, row=0, padx=2, sticky="we")
        
        for i, widget in enumerate(self.labels):
            widget.grid(column=0, row=i, sticky="w", **pad2)
            
        for i, widget in enumerate(self.fields):
            widget.grid(column=1, row=i, sticky="we", **pad2)
            
class ProvideAuthority(Dialog):
    def build(self):
        self.authority_frame = LabelFrame(self, text="Provide authority", padx=5, pady=5)
        self.password_lbl = Label(self.authority_frame, text="Enter administrator password:")
        self.password_ebx = Entry(self.authority_frame, show="*", width=25)
        
    def arrange(self):
        self.password_lbl.grid(sticky="w", **pad2)
        self.password_ebx.grid(sticky="we", **pad2)
        self.authority_frame.grid(column=0, row=0, padx=5, pady=5, sticky="we")
        
class CreateAdmin(Dialog):
    def build(self):
        self.frame = LabelFrame(self, text="Create administrator", padx=5, pady=5)
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
        self.frame.grid(padx=5, pady=5, sticky="we")
        
class WelcomeScreen(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.build()
        self.arrange()
        
    def build(self):
        self.welcome_frame = LabelFrame(self, text="Welcome", padx=5, pady=5)
        self.welcome_lbl = Label(self.welcome_frame, text="Welcome! Choose your action:")
        self.spelling_btn = Button(self.welcome_frame, text="Begin Spelling", width=20, height=5)
        self.progress_btn = Button(self.welcome_frame, text="View Progress", width=20, height=5)
        
    def arrange(self):
        self.welcome_frame.grid(padx=5, pady=5)
        self.welcome_lbl.grid(**pad2)
        self.spelling_btn.grid(**pad2)
        self.progress_btn.grid(**pad2)
        
class SpellingAid(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.build()
        self.arrange()
        
    def build(self):
        self.lists_var = StringVar()
        self.lists_var.set("test")
        self.lists_opt = OptionMenu(self, self.lists_var, "test", "test2")
        self.start_spelling_btn = Button(self, text="Start spelling")
        self.definition_lbl= Label(self, text="Definition:")
        self.example_lbl = Label(self, text="Example:")
        self.word_definition_lbl = Label(self, text="No definition")
        self.word_example_lbl = Label(self, text="No example")
        self.speak_again_btn = Button(self, text="Speak again")
        self.word_ebx= Entry(self)
        
    def arrange(self):
        a=0
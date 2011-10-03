'''
Created on Sep 29, 2011

@author: ahug048
'''
from Tkinter import *
from widgets import Dialog  

class Logon(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.build()
        self.arrange()
        
    def build(self):
        self.loginframe = LabelFrame(self, text="Login")
        
        self.logo = PhotoImage(file="placeholder.gif")
        self.logo_lbl = Label(self, image=self.logo)
        
        self.username_lbl = Label(self.loginframe, text="Username:")
        self.password_lbl = Label(self.loginframe, text="Password:")
        
        self.username_ebx = Entry(self.loginframe)
        self.password_ebx = Entry(self.loginframe, show="*")
                
        self.buttonframe = Frame(self.loginframe)
        self.login_btn = Button(self.buttonframe, text="Login")
        self.new_user_btn = Button(self.buttonframe, text="New user")
        self.buttons = [self.login_btn, self.new_user_btn]
        
        self.userinfo = [self.username_lbl, self.username_ebx, 
                         self.password_lbl, self.password_ebx, self.buttonframe]

        self.administrate_btn = Button(self, text="Administrate")


        self.elements = [self.logo_lbl, self.loginframe, self.administrate_btn]
        
        
    def arrange(self):
        # Arrange the picture, the login fields, and the administration panel
        for i, element in enumerate(self.elements):
            element.grid(column=0, row=i, padx=5, pady=5, sticky="we")
        
        # Arrange the login and new user buttons
        for i, widget in enumerate(self.buttons):
            widget.grid(column=i, row=0, padx=2, pady=2, sticky="we")
        
        # Arrange the login labels and fields
        for i, widget in enumerate(self.userinfo):
            widget.grid(column=0, row=i, padx=2, pady=2, sticky="we")
            

class UserRegistration(Dialog):        
    def build(self, master):
        self.username_lbl = Label(self, text="Username:")
        self.password_lbl = Label(self, text="Password:")
        self.password_confirmation_lbl = Label(self, text="Confirm password:")
        self.age_lbl = Label(self, text="Age:")
        self.photo_lbl = Label(self, text="Photo:")
        self.user_type_lbl = Label(self, text="User type:")
        
        self.labels = [self.username_lbl, self.password_lbl, 
                       self.password_confirmation_lbl, self.age_lbl,
                       self.photo_lbl, self.user_type_lbl]
        
        self.username_ebx = Entry(self)
        self.password_ebx = Entry(self, show="*")
        self.password_confirmation_ebx = Entry(self, show="*")
        self.age_ebx = Entry(self)
        
        self.photo_fields = Frame(self)
        self.photo_btn = Button(self.photo_fields, text="Browse")
        self.photo_ebx = Entry(self.photo_fields)
        
        self.user_type_var = StringVar()
        self.user_type_var.set("Student")
        
        self.user_type = Frame(self)
        
        self.student_rbn = Radiobutton(self.user_type, text="Student", variable=self.user_type_var, value="Student")
        self.teacher_rbn = Radiobutton(self.user_type, text="Teacher", variable=self.user_type_var, value="Teacher")

        self.fields = [self.username_ebx, self.password_ebx,
                       self.password_confirmation_ebx, self.age_ebx,
                       self.photo_fields, self.user_type]
        
        self.user_type_var = StringVar()
        
    def arrange(self):
        self.student_rbn.grid(column=0, row=0, padx=2, pady=2, sticky="w")
        self.teacher_rbn.grid(column=1, row=0, padx=2, pady=2, sticky="w")
        
        self.photo_ebx.grid(column=0, row=0, sticky="we")
        self.photo_btn.grid(column=1, row=0, padx=2, sticky="we")
        
        for i, widget in enumerate(self.labels):
            widget.grid(column=0, row=i, padx=2, pady=2, sticky="w")
            
        for i, widget in enumerate(self.fields):
            widget.grid(column=1, row=i, padx=2, pady=2, sticky="we")
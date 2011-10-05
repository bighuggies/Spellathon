'''
Created on 4/10/2011

@author: andrew

'''
import sqlite3 as sqlite
import os
from user import User
from words import Word

INIT = """
CREATE TABLE "words" (
    "string" VARCHAR(96) PRIMARY KEY,
    "word" Word
);

CREATE TABLE "users" (
    "username" VARCHAR(96) PRIMARY KEY,
    "user" User
);
"""

class DBManager(object):
    def __init__(self):
        exists = False
        
        if os.path.isfile("spellingaid.db"):
            exists = True
            
        self.db = sqlite.connect("spellingaid.db", detect_types = sqlite.PARSE_DECLTYPES)
        self.c = self.db.cursor()
            
        if not exists:
            self.db.executescript(INIT)
            
        sqlite.register_adapter(User, lambda u : u.serialise())
        sqlite.register_adapter(Word, lambda w : w.serialise())
        
        sqlite.register_converter("User", User.deserialise)
        sqlite.register_converter("Word", Word.deserialise)
        
    def commit(self):
        self.db.commit()
        self.c.close()
        
    def discard(self):
        self.db.rollback()
        self.c.close()
            
class UserManager(DBManager):
    def add_user(self, user):
        try:
            self.c.execute("INSERT INTO users VALUES (?, ?)", (user.username, user))
            return True
        except sqlite.IntegrityError:
            return False
            
    def retrieve_user(self, user):        
        try:
            self.c.execute("SELECT user FROM users WHERE username=?", (user.username,))
        except AttributeError:
            self.c.execute("SELECT user FROM users WHERE username=?", (user,))
        
        users = self.c.fetchone()
        
        if users:
            return users[0]
        else:
            return None
            
    def retrieve_users(self):
        self.c.execute("SELECT user FROM users")
        
        users = []
        
        for row in self.c:
            users.append(row[0])
        
        return users
        
    def retrieve_usernames(self):
        self.c.execute("SELECT username FROM users")
        
        usernames = []
        
        for row in self.c:
            usernames.append(row[0])
            
        return usernames
            
    def remove_user(self, user):        
        try:
            self.c.execute("DELETE FROM users WHERE username=?", (user.username,))
        except AttributeError:
            self.c.execute("DELETE FROM users WHERE username=?", (user,))

class WordManager(DBManager):    
    def add_word(self, word):
        try:
            self.c.execute("INSERT INTO words VALUES (?, ?)", (word.word, word))
            return True
        except sqlite.IntegrityError:
            return False
        
    def retrieve_word(self, word):
        try:
            self.c.execute("SELECT word FROM words WHERE string=?", (word.word,))
        except AttributeError:
            self.c.execute("SELECT word FROM words WHERE string=?", (word,))
        
        word = self.c.fetchone()
        
        if word:
            return word[0]
        else:
            return None
        
    def retrieve_words_of_difficulty(self, difficulty):
        self.c.execute("SELECT word FROM words")
        
        words = []
        
        for row in self.c:
            if row[0].difficulty == difficulty:
                words.append(row[0])
        
        return words
   
    def remove_word(self, word):
        try:
            self.c.execute("DELETE FROM words WHERE string=?", (word.word,))
        except AttributeError:
            self.c.execute("DELETE FROM words WHERE string=?", (word,))

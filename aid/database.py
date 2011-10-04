'''
Created on 4/10/2011

@author: andrew

'''
import sqlite3 as sqlite
import os
from user import User

INIT = """
CREATE TABLE "words" (
    "id" INTEGER PRIMARY KEY,
    "word" VARCHAR(96),
    "definition" TEXT,
    "example" TEXT,
    "difficulty" VARCHAR(96),
    "source" VARCHAR(96)
);

CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY,
    "user" User
);
"""

class DBManager(object):
    def __init__(self):
        exists = False
        
        if os.path.isfile("spellingaid.db"):
            exists = True
            
        self.db = sqlite.connect("spellingaid.db", detect_types = sqlite.PARSE_DECLTYPES)
            
        if not exists:
            self.db.executescript(INIT)
            
        sqlite.register_adapter(User, lambda u : u.serialise())
        sqlite.register_converter("User", User.deserialise)
            
    def add_user(self, user):
        c = self.db.cursor()
        c.execute("INSERT INTO users VALUES (null, ?)", (user,))
        self.db.commit()
            
    def retrieve_user(self, user):        
        c = self.db.cursor()
        c.execute("SELECT * FROM users where user=?", (user,))
        
        return c.fetchone()
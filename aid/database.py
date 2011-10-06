'''
Handle the word and user tables in the Spellathon database.

Exported classes:
UserManager -- Manage the user table.
WordManager -- Manage the word table.

'''
import sqlite3 as sqlite
import os
from user import User
from words import Word

'''Initialisation script to create the tables if the database file is not found.
The primary key of a word record is the word itslf, associated with a word
object which contains the related metadata.

The primary key of a user record is the username, associated with a User object
which keeps track of the scores and details of the user.
'''

INIT = '''
CREATE TABLE 'words' (
    'string' VARCHAR(96) PRIMARY KEY,
    'word' Word
);

CREATE TABLE 'users' (
    'username' VARCHAR(96) PRIMARY KEY,
    'user' User
);
'''

class _DBManager(object):
    '''Abstract base class which implements committing and discarding database changes,
    as well as instantiation in the case where the database does not exist.
    
    Public functions:
    commit -- Save changes made to the database and close the cursor.
    discard -- Discard changes made to the database and close the cursor.
    
    '''
    def __init__(self):
        # Boolean to record whether the database exists. We need this because
        # we need to check if the db file exists in the file system before we
        # connect to the database.
        exists = False
        
        # Check if the database exists in the file system.
        if os.path.isfile('spellingaid.db'):
            exists = True
        
        # Connect to the database and create a cursor.
        self.db = sqlite.connect('spellingaid.db', detect_types = sqlite.PARSE_DECLTYPES)
        self.c = self.db.cursor()
        
        # If the database didn't exist, initialise the tables.
        if not exists:
            self.db.executescript(INIT)
        
        # Register adapters and converters to let the database work with User
        # and Word objects.
        sqlite.register_adapter(User, lambda u : u.serialise())
        sqlite.register_adapter(Word, lambda w : w.serialise())
        
        sqlite.register_converter('User', User.deserialise)
        sqlite.register_converter('Word', Word.deserialise)
        
    def commit(self):
        '''Save changes made to the database and close the cursor.'''
        self.db.commit()
        self.c.close()
        
    def discard(self):
        '''Discard changes made to the database and close the cursor.'''
        self.db.rollback()
        self.c.close()
            
class UserManager(_DBManager):
    '''Manage user records in the database.
    
    Public functions:
    add_user -- Add a user to the database.
    update_user -- Update a user record.
    retrieve_user -- Find and return individual User objects.
    retrieve_users -- Find and return a list of all User objects in the database.
    retrieve_usernames -- Find and return a list of all usernames.
    remove_user -- Remove a user from the database.
    
    '''
    def add_user(self, user):
        '''Add a user to the database.
        
        Arguments:
        user -- A User object representing a Spellathon user.
        
        Returns:
        True if successful, False if unsuccessful. Failure usually indicates
        that a user with that username already exists in the table.
        
        '''
        try:
            self.c.execute('INSERT INTO users VALUES (?, ?)', (user.username, user))
            return True
        except sqlite.IntegrityError:
            return False
        
    def update_user(self, user):
        '''Update a user in the database.
        
        Arguments:
        user -- A User object representing a Spellathon user.
        
        '''
        self.c.execute('UPDATE users SET user=? WHERE username=?', (user, user.username))
            
    def retrieve_user(self, user):
        '''Retrieve a User object from the database.
        
        Arguments:
        user -- A User object or username representing a Spellathon user.
        
        Returns:
        The User object representing the given user, or None if not found.
        
        '''       
        try:
            self.c.execute('SELECT user FROM users WHERE username=?', (user.username,))
        except AttributeError:
            self.c.execute('SELECT user FROM users WHERE username=?', (user,))
        
        users = self.c.fetchone()
        
        # Take index 0 of the row tuple, rather than returning the tuple.
        if users:
            return users[0]
        else:
            return None
            
    def retrieve_users(self):
        '''Retrieve all User objects from the database.
        
        Returns:
        The list of all Spellathon users.
        
        '''
        self.c.execute('SELECT user FROM users')
        
        users = []
        
        # Take index 0 of the row tuple, rather than returning the tuple.
        for row in self.c:
            users.append(row[0])
        
        return users
        
    def retrieve_usernames(self):
        '''Retrieve all usernames from the database.
        
        Returns:
        The list of all Spellathon users usernames.
        
        '''
        self.c.execute('SELECT username FROM users')
        
        usernames = []

        # Take index 0 of the row tuple, rather than returning the tuple.
        for row in self.c:
            usernames.append(row[0])
            
        return usernames
            
    def remove_user(self, user):
        ''' Remove a user from the database.
        
        Arguments:
        user -- A User object or username representing a Spellathon user.
        
        '''     
        try:
            self.c.execute('DELETE FROM users WHERE username=?', (user.username,))
        except AttributeError:
            self.c.execute('DELETE FROM users WHERE username=?', (user,))

class WordManager(_DBManager):
    '''Manage word records in the database.
    
    Public functions:
    add_word -- Add a word to the database.
    retrieve_word -- Find and return individual Word objects.
    retrieve_words_of_difficulty -- Retrieve a list of 
    all words of a given difficulty.
    remove_word -- Remove a given word.
    
    '''
    def add_word(self, word):
        '''Add a given word to the database.
        
        Arguments:
        word -- A Word object containing a word and the related metadata.
        
        Returns:
        True if successful, False if unsuccessful. Failure usually indicates
        that the given word already exists in the table.
        
        '''
        try:
            self.c.execute('INSERT INTO words VALUES (?, ?)', (word.word, word))
            return True
        except sqlite.IntegrityError:
            return False

    def retrieve_word(self, word):
        '''Retrieve a given word from the database.
        
        Arguments:
        word -- A string or Word object representing a word.
        
        Returns:
        The Word object representing the given word, or None if not found.
        
        '''
        try:
            self.c.execute('SELECT word FROM words WHERE string=?', (word.word,))
        except AttributeError:
            self.c.execute('SELECT word FROM words WHERE string=?', (word,))
        
        word = self.c.fetchone()

        # Take index 0 of the row tuple, rather than returning the tuple.
        if word:
            return word[0]
        else:
            return None
        
    def retrieve_words_of_difficulty(self, difficulty):
        '''Retrieve all words of a given difficulty from the database.
        
        Arguments:
        difficulty -- The difficulty of the words to be retrieved (CL1, AL1 etc).
        
        Returns:
        A list of word objects with the given difficulty.
        
        '''
        self.c.execute('SELECT word FROM words')
        
        words = []
        
        # For all words in the database, if the word has the requested
        # difficulty, add that word to the list to be returned.
        for row in self.c:
            if row[0].difficulty == difficulty:
                words.append(row[0])
        
        return words
   
    def remove_word(self, word):
        '''Remove a given word from the database.
        
        Arguments:
        word -- A string or Word object representing the word to be removed.
        
        '''
        try:
            self.c.execute('DELETE FROM words WHERE string=?', (word.word,))
        except AttributeError:
            self.c.execute('DELETE FROM words WHERE string=?', (word,))

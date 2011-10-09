'''
Module to keep track of a spelling session.

Exported classes:

Session -- Represents an individual attempt at spelling a given list.

'''
import random
import tools.database as database
from tools.speech import Speech

class Session(object):
    '''Represents an individual attempt at spelling a given list.
    
    Public functions:
    start -- Begins the spelling session.
    end -- Ends the spelling session.
    next -- Gets the next word to spell.
    speak_example -- Speaks the example associated with the current word.
    speak_word -- Speaks the current word.
    update_interface -- Tells the interface to update on a new word.
    check -- Check if the submitted word was spelled correctly.
    
    '''
    def __init__(self, interface, wordlist, user):
        '''Initialise a session.
        
        Arguments:
        interface -- The spelling aid interface.
        wordlist -- The list currently being spelled.
        user -- The current speller.
        
        '''
        self.interface = interface
        self.wordlist = wordlist
        self.user = user
        
        self.speech = Speech()
        self.highscore = self.user.high_score(wordlist.name)

        self.score = 0
        self.attempts = {}
        self.newhighscore = False
        self.correct = None
                
    def start(self):
        '''Begins the spelling session.'''
        # Create the list of words from the wordlist object and randomise it.
        self.words = self.wordlist.words.keys()
        self.list_length = len(self.words)
        random.shuffle(self.words)
        
        # Call next to update the interface to prompt the user to spell the
        # first word.
        self.next()
        
    def end(self):
        '''Ends the spelling session.'''
        # Add the score for the session to the user object.
        self.user.add_score(self.wordlist.name, self.score)
        
        # Update the user record in the database.
        um = database.get_user_manager()
        um.update_user(self.user)
        um.commit()
        
        # Tell the interface the score the user achieved so that it can display
        # a score window.
        self.interface.session_ended(str(self.score) + '/' + str(self.list_length), str(self.highscore) + '/' + str(self.list_length), self.newhighscore, self.attempts)
        
    def next(self):
        '''Gets the next word to spell.'''
        try:
            # Try to get the next word from the list of words and speak it. Then
            # update the interface.
            self.word = self.words.pop()
            self.speech.speak(self.word)
            self.update_interface()
        except IndexError:
            # If there are no more words, end the session.
            self.end()
            
    def speak_example(self):
        '''Speak the example of the current word.'''
        # If festival was already speaking, kill it.
        self.speech.kill()
        
        self.speech.speak(self.wordlist.words[self.word].example)
    
    def speak_word(self):
        '''Speak the current word.'''
        # If festival was already speaking, kill it.
        self.speech.kill()
        self.speech.speak(self.word)
    
    def update_interface(self):
        '''Tells the interface to update on a new word.'''
        # Tell the interface about the word and the player's score.
        self.interface.update(self.wordlist.words[self.word].definition, 
              str(self.score) + '/' + str(len(self.wordlist.words)),
              str(self.highscore) + '/' + str(len(self.wordlist.words)),
              self.correct)

    def check(self, word):
        '''Check that the submitted word was spelled correctly.
        
        Arguments:
        word -- The submitted word (a string).
        
        '''
        # Add the submission to the list of attempts so that it can be displayed
        # in the final summary.
        self.attempts[self.word] = word
        
        if self.word == word:
            # If the submission was correct, increment the score and check if
            # the new score is a high score so the user can be notified at the
            # end of the session. Finally, get the next word.
            self.score += 1
            self.correct = True
            if self.score > self.highscore:
                self.highscore = self.score
                self.newhighscore = True
            
            self.next()
            return True
        else:
            # If the submission was incorrect, mark them wrong so the interface
            # can update and get the next word.
            self.correct = False
            self.next()
            return False
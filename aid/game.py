'''
Created on 5/10/2011

@author: andrew
'''
import random
import database
from speech import Speech
#from user import User

class Session(object):
    def __init__(self, interface, listname, user):
        self.interface = interface
        self.wordlist = listname
        self.speech = Speech()
        self.user = user
        self.score = 0
        self.highscore = self.user.high_score(listname.name)
        self.attempts = {}
        self.newhighscore = False
        self.correct = None
                
    def start(self):
        self.words = self.wordlist.words.keys()
        self.list_length = len(self.words)
        random.shuffle(self.words)
        
        self.next()
        
    def end(self):
        self.user.add_score(self.wordlist.name, self.score)
        
        um = database.get_user_manager()
        um.update_user(self.user)
        um.commit()
                
        self.interface.session_ended(str(self.score) + '/' + str(self.list_length), str(self.highscore) + '/' + str(self.list_length), self.newhighscore, self.attempts)
        
    def next(self):
        
        try:
            self.word = self.words.pop()
            self.speech.speak(self.word)
            self.update_interface()
        except IndexError:
            self.end()
            
    def speak_example(self):
        self.speech.kill()
        self.speech.speak(self.wordlist.words[self.word].example)
    
    def speak_word(self):
        self.speech.kill()
        self.speech.speak(self.word)
    
    def update_interface(self):
        self.interface.update(self.wordlist.words[self.word].definition, 
              str(self.score) + '/' + str(len(self.wordlist.words)),
              str(self.highscore) + '/' + str(len(self.wordlist.words)),
              self.correct)

    def check(self, word):
        self.attempts[self.word] = word
        
        if self.word == word:
            self.score += 1
            self.correct = True
            if self.score > self.highscore:
                self.highscore = self.score
                self.newhighscore = True
            
            self.next()
            return True
        else:
            self.correct = False
            self.next()
            return False
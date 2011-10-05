'''
Created on 5/10/2011

@author: andrew
'''
import time
import random

class Session(object):
    def __init__(self, interface, list):
        self.interface = interface
        self.begintime = time.time()
        self.wordlist = list
                
    def start(self):
        self.words = self.wordlist.words.keys()
        random.shuffle(self.words)

        self.word = self.words.pop()
        print self.word

        self.interface.update(self.wordlist.words[self.word].definition, self.wordlist.words[self.word].example)
        
    def end(self):
        self.endtime = time.time()
        print (self.endtime - self.begintime)
        
    def next(self):
        self.word = self.words.pop()
        print self.word
        self.interface.update(self.wordlist.words[self.word].definition, self.wordlist.words[self.word].example)
        
    def check(self, word):
        if self.word == word:
            self.next()
            return True
        else:
            return False
            
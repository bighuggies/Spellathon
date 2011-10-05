'''
Created on 5/10/2011

@author: andrew
'''
import time

class Session(object):
    def __init__(self, interface, list):
        self.interface = interface
        self.begintime = time.time()
        self.wordlist = list        
        
        print self.begintime
        
    def start(self):
        words = sorted(self.wordlist.words.keys())
        for word in words:
            print word
        
    def end(self):
        self.endtime = time.time()
        print self.endtime - self.time
        
#    def check(self, word):
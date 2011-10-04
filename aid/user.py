'''
Created on Sep 29, 2011

@author: ahug048
'''
import pickle

class User(object):
    def __init__(self, username, realname, password, birthday, photo=None, scores=None):
        self.username = username
        self.realname = realname
        self.password = password
        self.birthday = birthday
        self.photo = photo
        
        if scores:
            self.scores = scores
        else:
            self.scores = {}
        
    def serialise(self):
        scores = pickle.dumps(self.scores)
        
        
        return "%s|%s|%s|%s|%s|%s" % (self.username,
                                      self.realname,
                                      self.password,
                                      self.birthday,
                                      self.photo,
                                      scores)
        
    @classmethod
    def deserialise(cls, string):
        parts = string.split("|")
        parts[-1] = pickle.loads(parts[-1])
        for item in parts:
            print item
        return cls(*parts)
        
        
        
    def add_score(self, list, score):
        try:
            self.scores[list].append(score)
        except KeyError:
            self.scores[list] = [score]
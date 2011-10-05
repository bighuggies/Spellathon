'''
Created on Sep 29, 2011

@author: ahug048
'''
import pickle

class User(object):
    def __init__(self, username, realname, password, dob, photo=None, scores=None):
        self.username = username
        self.realname = realname
        self.password = password
        self.dob = dob
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
                                      self.dob,
                                      self.photo,
                                      scores)
        
    @classmethod
    def deserialise(cls, string):
        parts = string.split("|")
        parts[-1] = pickle.loads(parts[-1])
        
        return cls(*parts)
        
    def add_score(self, list, score):
        try:
            self.scores[list].append(score)
        except KeyError:
            self.scores[list] = [score]
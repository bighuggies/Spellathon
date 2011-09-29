'''
Created on Sep 29, 2011

@author: ahug048
'''
class User(object):
    def __init__(self, username, realname, password, birthday, photo=None, type="Student", scores=None):
        self.username = username
        self.realname = realname
        self.password = password
        self.birthday = birthday
        self.photo = photo
        self.type = type
        self.scores = scores
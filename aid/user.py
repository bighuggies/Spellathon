'''
Module to represent users.

Exported classes:

User -- Class to represent users of the application.

'''
import pickle
import shutil

class User(object):
    '''Represents a user and keeps track of their _scores.
    
    Public functions:
    serialise -- Return a string representation of this object for storage.
    add_score -- Add a score after a session of spelling.
    high_score -- Return the high score for a given list.
    
    Class functions:
    deserialise -- Return a User instance given a string representation.
    
    '''
    def __init__(self, username, realname, password, dob, photo=None,
                 _scores=None):
        '''Create a user object
        
        Arguments:
        username -- The name that will be used to log in.
        realname -- Real name of the user.
        password -- Salted hashed password.
        dob -- String representing date of birth.
        photo -- Path to the user photo.
        _scores -- A dictionary containing lists of _scores for each word list.
        
        '''
        self.username = username
        self.realname = realname
        self.password = password
        self.dob = dob
        
        # Copy the user photo into the application directory if one is given,
        # otherwise use stock image.
        try:
            shutil.copy(photo, '.userimages/' + username + '.gif')
            self.photo = photo
        except IOError:
            self.photo = '.userimages/nophoto.gif'
        
        # If scores weren't given, make an empty dictionary.
        if _scores:
            self._scores = _scores
        else:
            self._scores = {}
        
    def serialise(self):
        '''Return a string representation of the user.'''
        # Turn the _scores dictionary into a string.
        _scores = pickle.dumps(self._scores)
        
        # Return the string.
        return '%s|%s|%s|%s|%s|%s' % (self.username,
                                      self.realname,
                                      self.password,
                                      self.dob,
                                      self.photo,
                                      _scores)
        
    @classmethod
    def deserialise(cls, string):
        '''Given a string representation of a user, return a User object.'''
        # Get the individual parts of the user.
        parts = string.split('|')
        # Turn the _scores back into a dictionary.
        parts[-1] = pickle.loads(parts[-1])
        # Create and return the user object.
        return cls(*parts)
        
    def add_score(self, list, score):
        '''Add a score to the user record.
        
        Paramaters:
        list -- The name of the list which the user played.
        score -- The score they achieved.
        
        '''
        # If the user already has _scores for the list, append the new score.
        # Otherwise, create a new list and add it to the dictionary.
        try:
            self._scores[list].append(score)
        except KeyError:
            self._scores[list] = [score]
            
    def high_score(self, list):
        '''Return the high score of the user for a given list. Returns 0 if the
        user hasn't played a list'''
        try:
            return max(self._scores[list])
        except KeyError:
            return 0
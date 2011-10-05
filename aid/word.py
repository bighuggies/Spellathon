'''
Created on 5/10/2011

@author: andrew
'''
class Word(object):
    """Represents a word with a related definition, example use, and difficulty
    level."""
    def __init__(self, word, definition = "no definition", example = "no example", difficulty = "none"):
        """Create a word with a definition, example use, and difficulty level.
        
        Arguments:
        
        word -- The word itself
        definition -- A definition of the word (default = "")
        example -- An example use of the word (default = "")
        difficulty -- An integer representation of the spelling difficulty.
        (default = -1)
                
        """
        self.word = word
        self.definition = definition
        self.example = example
        self.difficulty = difficulty
        
    def serialise(self):
        """Return a string which represents a word in the TLDR format."""
        return "{word}|{definition}|{example}|{difficulty}".format(**self.__dict__)
                
    @classmethod
    def deserialise(cls, line):
        """Take a string of TLDR format and create a Word representation."""
        return cls(*line.split("|"))
            
    def __str__(self):
        """Return the word itself as the string representation."""
        return self.word
'''
Module to represent words and lists of words

Exported classes:

Word -- Represents a word with a related definition, example use, and difficulty
level.
WordList -- Manages lists of words.

'''
class Word(object):
    '''Represents a word with a related definition, example use, and difficulty
    level.'''
    def __init__(self, word, definition='no definition', example='no example', difficulty='none'):
        '''Create a word with a definition, example use, and difficulty level.
        
        Arguments:
        
        word -- The word itself
        definition -- A definition of the word (default = '')
        example -- An example use of the word (default = '')
        difficulty -- An integer representation of the spelling difficulty.
        (default = -1)
                
        '''
        self.word = word
        self.definition = definition
        self.example = example
        self.difficulty = difficulty
        
    def serialise(self):
        '''Return a string which represents a word in the TLDR format.'''
        return ('{word}|{definition}|{example}|{difficulty}'.format(**self.__dict__)).encode("utf-8")
                
    @classmethod
    def deserialise(cls, line):
        '''Take a string of TLDR format and create a Word representation.'''
        return cls(*line.split('|'))
            
    def __str__(self):
        '''Return the word itself as the string representation.'''
        return self.word
    
class WordList(object):
    '''Manages lists of words.

    Public functions:
    add_word -- Adds a word to the list of words.
    del_word -- Deletes a word from the list of words.
    get_word -- Gets a word from the list of words.

    '''
    def __init__(self, name, source='', date_edited='', words=None):
        '''Creates a WordList object.
        
        Arguments:
        name -- The name of the listname of words
        source -- The author/source (optional)
        date_edited -- The date the word listname was last edited (optional)
        words -- A dictionary object containing Word objects (optional)
        
        '''
        self.name = name
        self.source = source
        self.date_edited = date_edited
        
        if words:
            self.words = words
        else:
            self.words = {}
        
    def add_word(self, word):
        '''Add a word to the list of words.
        
        Arguments:
        word -- string or Word() representation of a word
        
        '''
        try:
            self.words[word.word] = word
        except AttributeError:
            self.words[word] = Word(word, 'no definition', 'no example', 'none')
        
    def del_word(self, word):
        '''Delete a word from the list of words.
        
        Arguments:
        word -- string or Word() representation of a word
        
        Returns:
        A boolean where True represents successfully deleting a word.
        
        '''
        try:
            del self.words[word.word]
            return True
        except AttributeError:
            del self.words[word]
        except KeyError:
            return False
            
    def get_word(self, word):
        '''Get a word from the list of words.
        
        Arguments:
        word -- string or Word() representation of a word
        
        Returns:
        The word object representing a given word in the word list. If the word
        is not in the word list, returns an empty string.
        
        '''
        try:
            return self.words[word.word]
        except AttributeError:
            return self.words[word]
        except KeyError:
            return ''
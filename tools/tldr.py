'''
Module containing functions to generate and parse TLDR format files containing
lists of words.

'''

from aid.words import Word, WordList
import datetime
import glob

def parse_tldr(tldrfile, listname = 'default'):
    '''Gets each line from a tldr file and parses it into a WordList
    instance.
    
    Arguments:
    tldrfile -- The tldr file to read from
    listname -- The name of the word list to be generated from the tldr
            
    Returns:
    Returns the list of all words in the tldr file.
    
    '''
    # Get the data from the file all at once. (Should probably change this to
    # work line by line).
    tldr = open(tldrfile)
    data = tldr.readlines()
    tldr.close()
    
    wordlist = WordList(listname)

    for i, line in enumerate(data):
        # Take the first two lines of the filedata and parse them as metadata.
        if line[0] == '#':
            if i == 0:
                wordlist.source = line[1:].strip()
            if i == 1:
                wordlist.date_edited = line[1:].strip()       
        elif (line[0] != '#') and (len(line) > 3):
        # All other lines which are not comment lines are words, so add the word
        # to the wordlist.
            word = Word.deserialise(line)
            wordlist._add_word(word)
    
    return wordlist

def parse_tldr_files(path):
    '''Parse all tldr files in a given path.
    
    Arguments:
    path -- The path in which to look for tldr files.
    
    Returns:
    Dictionary containing each wordlist where the keys are the names of the
    lists.
    
    '''
    tldrs = {}
    
    # Get each tldr file in the directory and parse it into the dict of tldr
    # files to be returned.
    for t in glob.glob(path + '*.tldr'):
        name = t.split("/")[-1].split('.')[0]
        tldrs[name] = parse_tldr(t, name)

    return tldrs

def generate_tldr(wordlist, tldrfile):
    '''Generates a TLDR file given a WordList.
    
    Arguments:
    wordlist -- The wordlist to place in the file
    tldrfile -- The file to place the wordlist in
    
    '''
    try:
        f = open(tldrfile, 'w')
    except IOError:
        return False    
    
    # Write the metadata to the first three lines of the file.
    f.write('#' + wordlist.source + '\n')
    f.write('#' + str(datetime.datetime.now()) + '\n')
    f.write('#' + str(len(wordlist.words)) + '\n')
    
    keys = []
    
    # Sort the keys so that we can access the wordlist in proper alphabetical
    # order. That is, ignoring capitalisation.
    for string in sorted(wordlist.words.iterkeys(), key=str.lower):
        keys.append(string)
    
    # Write each word to the file. If the word doesn't end in a new line char,
    # add it to the end so that there is guaranteed to be at most one word
    # per line.
    for k in keys:
        newword = wordlist.words[k].serialise()
        if newword[-1] != '\n':
            newword += '\n'
        f.write(newword)
                
    f.close()
    
    return True

def generate_empty_tldr(path, name, author):
    '''Generate an empty tldr file.
    
    Arguments:
    path -- The directory to create the tldr file in.
    name -- The name of the file to create.
    author -- The author of the word list.

    '''
    f = open(path, 'w')
    
    f.write('#' + author + '\n')
    f.write('#' + str(datetime.datetime.now()) + '\n')
    f.write('#0')
    
    f.close()
    
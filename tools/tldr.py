from aid.words import Word, WordList
import datetime
import glob

def parse_tldr(tldrfile, list_name = 'default'):
    '''Gets each line from a tldr file and parses it into a WordList
    instance.
    
    Arguments:
    tldrfile -- The tldr file to read from
    list_name -- The name of the word list to be generated from the tldr
            
    Returns:
    Returns the list of all words in the tldr file.
    
    '''
    tldrFile = open(tldrfile)
    fileData = tldrFile.readlines()
    wordList = WordList(list_name)
    tldrFile.close()

    for i, line in enumerate(fileData):
        if line[0] == '#':
            if i == 0:
                wordList.source = line[1:].strip()
            if i == 1:
                wordList.date_edited = line[1:].strip()       
        elif (line[0] != '#') and (len(line) > 3):
            word = Word.deserialise(line)
            wordList.add_word(word)
    
    return wordList

def parse_tldr_files(path):
    tldrs = {}
    
    for t in glob.glob(path + '*.tldr'):
        tldrs[t[10:-5]] = parse_tldr(t, t[10:-5])

    return tldrs

def generate_tldr(words, tldrfile):
    '''Generates a TLDR file given a WordList.
    
    Arguments:
    words -- The words to place in the file
    file -- The file to place the words in
    
    '''
    try:
        f = open(tldrfile, 'w')
    except IOError:
        return False    

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    f.write('#' + words.source + '\n')
    f.write('#' + str(now) + str(year) + str(month) + str(day) + '\n')
    f.write('#' + str(len(words.words)) + '\n')
    
    keys = []
    for string in sorted(words.words.iterkeys(), key=str.lower):
        keys.append(string)
    
    for k in keys:
        newword = words.words[k].serialise()
        if newword[-1] != '\n':
            newword += '\n'
        f.write(newword)

    
    
#    for value in sorted(words.words.itervalues(), key=str.lower):
#        newword = value.serialise()
#        if newword[-1] != '\n':
#            newword += '\n'
#        f.write(newword)
        
    f.close()
    
    return True

def generate_empty_tldr(path, name, author):
    
    f = open(path, 'w')
    f.write('#' + author + '\n')
    f.write('#' + str(datetime.datetime.now()) + '\n')
    f.write('#0')
    
    f.close()
    
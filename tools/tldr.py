from aid.words import Word, WordList
import datetime

def parse_tldr(tldrfile, list_name = "default"):
    """Gets each line from a tldr file and parses it into a WordList
    instance.
    
    Arguments:
    tldrfile -- The tldr file to read from
    list_name -- The name of the word list to be generated from the tldr
            
    Returns:
    Returns the list of all words in the tldr file.
    
    """
    tldrFile = open(tldrfile)
    fileData = tldrFile.readlines()
    wordList = WordList(list_name)

    for i, line in enumerate(fileData):
        if line[0] == "#":
            if i == 0:
                wordList.source = line[1:]                    
            if i == 1:
                wordList.date_edited = line[1:]                    
        elif (line[0] != "#") and (len(line) > 3):
            word = Word.deserialise(line)
            wordList.add_word(word)
    
    return wordList

def generate_tldr(words, tldrfile):
    """Generates a TLDR file given a WordList.
    
    Arguments:
    words -- The words to place in the file
    file -- The file to place the words in
    
    """
    try:
        fileData = open(tldrfile, 'w')
    except IOError:
        return False
    
    #September 20th, 2011-09-20 - do the date
    

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    fileData.write("#" + "Custom list created by" + " " + words.source + "\n")
    fileData.write("#" + str(now) + str(year) + str(month) + str(day) + "\n")
    fileData.write("#" + str(len(words.words)) + " word(s)" + "\n")
    for key, value in sorted(words.words.iteritems()):
        newword = value.serialise()
        if newword[-1] != "\n":
            newword += "\n"
        fileData.write(newword)
        
    return True
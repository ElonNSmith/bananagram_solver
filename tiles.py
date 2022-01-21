class Tile:

    def __init__(self, val):
        self.charstring = val.upper()
        self.wordlist = []
        self.linkdict = {}
        self.populate_wordlist()
        self.populate_linkdict()


    def add_letter(self, val):
        self.charstring += (val.upper())
        self.populate_wordlist()
        self.populate_linkdict()

    def populate_wordlist(self):
        with open('scrabble dictionary.txt') as dictionary:
            for word in dictionary:
                word = word.rstrip()
                charstring_copy =  list(self.charstring).copy()
                word_valid = True
                for char in word:
                    if char not in charstring_copy:
                        word_valid = False
                        break
                    else:
                        charstring_copy.remove(char)
                if word_valid:
                    self.wordlist.append(word)

    def populate_linkdict(self):
        self.linkdict = {}
        for word in self.wordlist:
            self.linkdict[word] = self.intersecting_words(word)
        pass

    def intersecting_words(self, primary_word):
        out = []
        charstring_copy = list(self.charstring).copy()
        for char in primary_word:
            charstring_copy.remove(char)
        for char in primary_word:
            charstring_copy.append(char)
            for word in self.find_words(charstring_copy, self.wordlist):
                out.append(word)
            charstring_copy.remove(char)
        return out

    def find_words(self, charstring, wordlist) -> list:
        out = []
        for word in wordlist:
            word_valid = True
            charstring_copy = list(charstring).copy()
            for char in word:
                if char not in charstring_copy:
                    word_valid = False
                    break
                else:
                    charstring_copy.remove(char)
                    if word_valid:
                        out.append(word)
        return out

    def possible_word_sets(self, charstring, words_already:list):
        #charstring should have all the charecters not already used
        wordlist = []
        for word in words_already:
            wordlist.extend(self.linkdict[word])
        wordlist = list(set(wordlist))
        if len(charstring) == 0 :
            yield words_already
            for word  in wordlist:
                charstring_copy = list(charstring).copy()
                words_already_copy = words_already.copy()
                if self.is_valid_word_addition(word, ''.join(charstring_copy),list(words_already)):
                    for character in word:
                        if character in charstring_copy:
                            charstring_copy.remove(character)

                    words_already_copy.append(word)
                    yield possible_word_sets(self, ''.join(charstring_copy),words_already_copy)
        pass

    def is_valid_word_addition(self, word : str , charstring, words_already: list):
        missing_counter = 0
        missing_characters = []
        charstring_copy = list(charstring).copy()
        for char in word:
            if char in charstring_copy:
                charstring_copy.remove(char)
            else:
                missing_counter += 1
                missing_characters.append(char)
        if len(missing_characters) > 1:
            return False
        out = False
        for word in words_already:
            for char in word:
                if char in missing_characters:
                    return True

        return out

        
        #eturns a list of strings
    def combined_letters(self, word1, word2) -> list:
        word1 = word1.upper()
        word2 = word2.upper()
        print( word1 + word2)
        possible_intersecting_letterrs = set(word1).intersection(set(word2))
        out = []
        temp = word1+word2
        stringlist = list(temp)
        for character in possible_intersecting_letterrs:
            stringlist.remove(character)
            outstr = ''
            outstr = outstr.join(stringlist)
            out.append(outstr)
            stringlist.append(character)
        return out



if __name__ == '__main__':

    a = Tile('applebannanaorange')
    a.add_letter('S')
    a.populate_wordlist()
    print(a.wordlist)
    print(a.find_words('APE', a.wordlist))
    print(a.intersecting_words('APE'))
    a.populate_linkdict()
    #print(a.linkdict)
    print(a.combined_letters('ape','apple'))
    print(a.linkdict['APE'])
    b = a.possible_word_sets('ORANGE',['APE','APPLE','BANANA',])
    print('*************************************************8')
    for abc in  b:
        print(abc)

class Tile:

    def __init__(self, val):
        self.charstring = val.upper()
        self.wordlist = []
        self.populate_wordlist()
        self.wordlist.sort(key=len)
        self.wordlist.reverse()

    def add_letter(self, val):
        self.charstring += (val.upper())
        self.populate_wordlist()

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


    #yeilds strings of letters available after an intersection
    # intersecting_string('apple','pie') -> 'apleie','apleie', 'applpi'
    def intersecting_string(self, string1:str, string2:str):
        for character1 in string1:
            for character2 in string2:
                if character1 == character2:
                    index1 = string1.find(character1)
                    index2 = string2.find(character2)
                    yield string1[:index1]+string1[index1+1:]+string2[:index2]+string2[index2+1:]

    def intersecting_string_2(self, string1:str, string2:str, permitted_intersections:str):
        for character1 in string1:
            for character2 in string2:
                if character1 == character2:
                    if character1 in permitted_intersections:
                        index1 = string1.find(character1)
                        index2 = string2.find(character2)
                        yield string1[:index1]+string1[index1+1:]+string2[:index2]+string2[index2+1:]


    #despite it's name the set of words will be returned as a generator object (multiples allowed)
    #every characyer in characters_free represents an unused tile
    #every charecter in characters_available represents characters in words_already that can be built off` 
    def generate_possible_word_sets(self,characters_free:str,characters_available:str, words_already:list):
        if characters_free == '':
            words_already.sort()
            yield  words_already
        words_already_copy = words_already.copy()
        for word in self.wordlist:
            characters_free_copy = list(characters_free).copy()
            unfound_character_counter = 0
            permitted_intersections = ''
            for character in word:
                if character in characters_free_copy:
                    characters_free_copy.remove(character)
                else:
                    unfound_character_counter += 1
                    permitted_intersections += character
            if unfound_character_counter <= 1:
                outlist = words_already.copy()
                outlist.append(word)
                #recursion here, watch out
                for intersection in self.intersecting_string_2(characters_available,word,permitted_intersections):
                    yield from self.generate_possible_word_sets(''.join(characters_free_copy),intersection,outlist)

    def get_word_sets(self):
        for word in self.wordlist:
            charstring_copy = list(self.charstring).copy()
            for char in word:
                charstring_copy.remove(char)
            yield from self.generate_possible_word_sets(''.join(charstring_copy),word,[word])

    def get_ordered_set_of_word_sets(self):
        my_set = set(tuple(self.get_word_sets()))
        print('set made')
        my_sorted = sorted(my_set, key = len)
        return my_sorted


if __name__ == '__main__':
    a  = Tile('applepi')
    print(a.wordlist)
    for b in a.intersecting_string('apple','pie'):
        print(b)
    d = Tile('applepi')
    for b in d.get_word_sets():
        print(b)
    c = Tile('AOEGEUIDoiapnia')
    for b in c.get_ordered_set_of_word_sets():
        print(b)

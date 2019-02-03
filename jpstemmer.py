import re
class JPStemmer:
    def __init__(self):
        # These are the various lists that will be searched through to conjugate verbs and adjectives.
        # While conjugating, the index of a character is found in the appropriate list. Then, that character is replaced by a character
        # in a separate list with the same index.
        self.endinglist = [u"ませんでした", u"ました", u"ません", u"ます", u"ない", u"なかった"]
        self.nadjend = [u"です", u"だ", u"でした", u"だった", u"ではありません", u"ではない", u"ではありませんでした", u"ではなかった", u"じゃない"]
        self.iadjend = [u"くなかった", u"かった", u"くない"]
        self.wordlist = [u"わ", u"か", u"が", u"さ", u"ざ", u"た", u"だ", u"な", u"ま", u"は", u"ば", u"ぱ", u"ら", u"や"]
        self.ilist = [u"い", u"き", u"ぎ", u"し", u"じ", u"ち", u"ぢ", u"に", u"み", u"ひ", u"び", u"ぴ", u"り"]
        self.ulist = [u"う", u"く", u"ぐ", u"す", u"ず", u"つ", u"づ", u"ぬ", u"む", u"ふ", u"ぶ", u"ぷ", u"る", u"ゆ"]
        self.elist = [u"え", u"け", u"げ", u"せ", u"ぜ", u"て", u"で", u"ね", u"め", u"へ", u"べ", u"ぺ", u"れ"]
        self.olist = [u"お", u"こ", u"ご", u"そ", u"ぞ", u"と", u"ど", u"の", u"も", u"ほ", u"ぼ", u"ぽ", u"ろ", u"よ"]
        self.tte = [u"って", u"った", u"んで", u"んだ", u"いて", u"いた", u"きて", u"いで", u"いだ", u"ぎで"]
        
        # This is the variable containing the word to be stemmed.
        self.word = ""
        # wordg is the main variable the algorithm uses to define the word it's processing.
        self.wordg = [""]
        # ending is used to store the end characters of a word that need to be removed before conjugation.
        self.ending = ""
        # wordType is used to either show that the word is a verb or an adjective. This is used in step1 to make sure
        # verbs don't get conjugated like adjectives and vice-versa.
        self.wordType = ""
        # original is a variable to store the unmodified word for future use.
        self.original = ""

    def stemmer(self, a):
        """a == the word"""
        self.word = a
        self.original = self.word
        self.word.strip(".")
        self.gothrough = True
        self.step1()
        if self.wordg != ['']:
            self.word = self.word[:len(self.word) - len(self.ending)]
            if self.wordType == "vb":
                self.step2()
                self.step3()
                self.step4()
                self.step5()
                self.step6()
                self.step7()
                self.step8()
            else:
                self.step2a()
        return self.word

    # Checks what kind of verb the word is. If the word is not a verb, nothing happens
    def checkvb(self):
        # Checks for group 1 & 2verbs in polite present, past, negative, past negative and some plain negative forms
        self.checkEnd()
        self.checkPlain2()
        self.checkPlain1()
        self.checkCond()
        self.checkPot()
        self.checkCause()
        self.checkImp()
        self.checkVol()
        self.checkPass()
        self.checkTe()

    # Checks if the word is an adjective
    def checkadj(self):
        # this checks if the word is an adjective, which are easy to tell apart because they always end in い or in the
        # elements of the iadjend list.
        for i in self.iadjend:
            # It goes through these checks to make sure an adjective is not mistaken for a verb in past plain form.
            # This is checked by looking at the character before "なかった", if it is in self.wordlist it is a verb. This
            # is faciliated by the use of .endswith(), which is used throughout this code to check the end of the word.
            if self.word[-1] == u"い" and not self.word.endswith(u"じゃない"):
                if self.word[-2] != u"な":
                    self.wordg = ["i", "adjective"]
                    self.ending = u"い"
                    return True
                elif self.word[-3:] == u"くない":
                    self.wordg = ["i", "adjective"]
                    self.ending = u"くない"
                    return True
                else:
                    return False
            if self.word.endswith(i):
                if self.word.endswith(u"かった"):
                    if not self.word.endswith(u"くなかった"):
                        if self.word[-4] in self.wordlist:
                            return False
                # If this isn't true, it assigns wordg appropriately
                self.wordg = ["i", "adjective"]
                self.ending = i
                return True
            # A check to see if the adjective ends with "じゃな", anther telling of an adjective
            elif self.word.endswith(u"じゃな" + i):
                self.wordg = ["i", "adjective"]
                self.ending = u"じゃな" + i
                return True
        for i in self.nadjend:
            if self.word.endswith(i):
                self.wordg = ["na", "adjective"]
                self.ending = i

    def checkEnd(self):
        # This function checks the verb for any of the "normal" sentence endings. If the character it's looking for is
        # in one of the letter lists, it assignes wordg apropreatly.
        for i in self.endinglist:
            if self.word.endswith(i):
                if self.word[len(self.original) - len(i) - 1] in self.ilist:
                    if self.word.endswith(u"します"):
                        self.wordg = ["shimasu", "normal"]
                        self.ending = "ます"
                    else:
                        self.wordg = ["one", "normal"]
                        self.ending = i
                        
                elif i == 'ませんでした':
                    self.ending = i
                    if self.word[-len(i) - 1] in self.ilist:
                        self.wordg = ["one", "normal"]
                        self.ending = i
                    else:
                        self.wordg = ['two', "normal"]
                        self.ending = i
                elif self.word[len(self.original) - len(i) - 1] in self.wordlist:
                    self.wordg = ["one", "normal"]
                    self.ending = i

                elif self.word[len(self.original) - len(i) - 1] in self.elist:
                    self.wordg = ["two", "normal"]
                    self.ending = i
            
    def checkCond(self):
        # Checks for conditonal form in both group 1 and two verbs.
        for i in self.elist:
            # if the word ends with an "e" letter and "ば", it assignes wordg as "two" and "cond"
            if self.word.endswith(i + u"ば"):
                self.wordg = ["two", "cond"]
                self.ending = u"ば"
            # if it just ends with "ば", it assignes wordg as "one" and "cond"
            elif self.word[-1] == u"ば":
                self.wordg = ["one", "cond"]

    # The first function to check for plain form verbs,
    def checkPlain1(self):
        # Checks for group 1 plain verbs
        if self.ending not in self.endinglist:
            if self.word[len(self.original) - 1] in self.ulist:
                for i in self.wordlist:
                    if self.word.endswith(i + u"れる"):
                        self.wordg = ["one", "pot"]
                        self.ending = u"れる"
            if self.word.endswith(u"られる"):
                self.wordg = ["two", "pot"]
                self.ending = u"られる"
            else:
                if self.wordg == []:
                    self.wordg = ["one", "normal"]
                    self.ending = ""

    # This is the second function to check for plain verbs, and spesifically group 2 verbs.
    def checkPlain2(self):
        # Verbs with two characters inclusive of る are always group 2.
        if len(self.original) == 2 and self.word[1] == u"る":
            self.wordg = ["two", "normal"]
            self.ending = u"る"
        # Checks for group 2 plain verbs
        elif self.word[len(self.original) - 1] == u"る" and self.word[len(self.original) - 2] in self.elist and self.word[len(self.original) - 3] not in self.wordlist:
            self.wordg = ["two", "normal"]
            self.ending = u"る"
            self.ending = self.word[len(self.original) - 1]

    # Checks for causeative form
    def checkCause(self):
        # If the words ends in an "e" letter and "せる", wordg is assigned as "two" and "cause"
        if self.word.endswith(u"せる"):
            if self.word[-4] in self.elist:
                self.wordg = ["two", "cause"]
                self.ending = self.word[-4] + u"せる"
            # if the word ends in sn "a" letter and "せる, wordg is assigned as "one" and "cause".
            elif self.word[-3] in self.wordlist:
                self.wordg = ["one", "cause"]
                self.ending = u"せる"

    def checkPot(self):
        # Checks for potential form
        # Group 2 potential and passive forms are conjugated the same way, so this will work for both
        if self.word.endswith(u"られる"):
            self.wordg = ["two", "pot"]
            self.ending = u"られる"

    def checkImp(self):
        # Checks for imperitive form. As it is impossible to get the stem of a group 1 verb imperitive verb without the
        # use of a lookup table, this simply sets self.ending to "" do nothing is done to it later on in the code.
        # If the word ends in an "e" character, it sets wordg to "one", "imp".
        if self.word[-1] in self.elist:
            self.wordg = ["one", "imp"]
            self.ending = ""

        # Also checks for imperitive form, but for group 2.
        # If the last character is "ろ", wordg is assigned as "two", "imp" and ending is assigned as "ろ".
        elif self.word[-1] == u"ろ":
            self.wordg = ["two", "imp"]
            self.ending = u"ろ"

    def checkVol(self):
        # Checks for volitional form
        # If the word ends with "よう", it is automatically considered a group two volitional verb. wordg is updated to
        # reflect this.
        if self.word[-2] in self.olist:
            for i in self.olist:
                if self.word.endswith(u"よう"):
                    self.wordg = ["two", "vol"]
                    self.ending = u"よう"
                # After looping through list of "o" characters, if the ending of the word equals i + "う", wordg is set
                # as "one", "vol" and ending assinged as i + "う".
                elif self.word.endswith(i + u"う") and self.wordg != ["two", "vol"]:
                    self.wordg = ["one", "vol"]
                    self.ending = i + u"う"

    def checkPass(self):
        # Checks for group 1 passive form
        # This function checks if the word ends with an "i" character + "れる", and sets wordg to "one", "pass" and
        # ending to "れる". This does not have an extra if statement for group 2 verbs, because they would be conjugated
        # correctly anyway.
        for i in self.wordlist:
            if self.word.endswith(i + u"れる"):
                self.wordg = ["one", "pass"]
                self.ending = u"れる"

    def checkTe(self):
        # Checks for te form.
        # This looks at the end of the word, if it's ending is in the "tte" list wordg will be set as "one". "tte" and
        # ending will be set as i. If the word just ends in "て" or "た" it is considerd a group two verb.
        if self.wordg == [""]:
            for i in self.tte:
                if self.word.endswith(i):
                    self.wordg = ["one", "tte"]
                    self.ending = i
                else:
                    if self.word.endswith(u"て"):
                        self.ending = u"て"
                    elif self.word.endswith(u"た"):
                        self.ending = "た"

    # This is where the code mainly starts. It calls the checkadj method, if it is successful in detecting an adjective
    # it will set the word type variable to "adj". If it does not detect an adjective, it wordType to "vb" and assumes
    # the word is a verb. It will then do the checks in checkverb()
    def step1(self):
        if re.search(u'[\u3040-\u309F]', self.word):
            if self.checkadj() == True:
                self.wordType = "adj"
            else:
                self.wordType = "vb"
                self.checkvb()
        else:
            self.wordg = ['']

    # Conjugates the polite, negative, past and past negative forms
    def step2(self):
        # Conjugates group one "normal" verbs.
        # First it checks wordg for the type of verb.
        if self.wordg[1] == "normal":
            if self.wordg[0] == "two" and self.word[-1] not in self.ulist or self.word[-1] != u"る":
                # Conjugates plain neg forms. It tooks at what list the last character is in (Either "a", "e", "i", "o" or "u"),
                # finds the index of that character in that character's list, and replaces it with an appropriate
                # charater of the same index in the list it needs to conjugate to. This method is used repeatedly
                # throughout the algoruthm.

                if self.word[len(self.original) - (len(self.ending) + 1)] in self.wordlist:
                    # In the case of a negative verb (which always end with an "a" character before the suffix), this
                    # removes the "a" character and replaces it with an "u" character in order to conjugate it to plain form.
                    self.word = self.word[:-1] + self.ulist[self.wordlist.index(self.word[-1])]
                # Conjugates polite forms.
                # This does the same as the previous if statement, but for "i" characters.
                elif self.word[len(self.original) - (len(self.ending) + 1)] in self.ilist:
                    self.word = self.word[:-1] + self.ulist[self.ilist.index(self.word[-1])]
            # This conjugates in the case of a group two verb, which just need to have "る" added to the end.
            if self.wordg[0] == "two":
                self.word += u"る"
        if self.wordg[0] == "shimasu":
            self.word += u"る"
        
    def step2a(self):
        # This conjugates adjectives, if wordg == "i", "adjective" it simply adds "い" to the end.
        if self.wordg[1] == "adjective":
            if self.wordg[0] == "i":
                self.word += u"い"
            if self.wordg[0] == "na":
                self.word -= len(self.ending)

    # Conjugates te form / ta form
    def step3(self):
        if self.wordg[1] == "tte":
            if self.wordg[0] == "one":
                self.word = self.original
            elif self.wordg[0] == "two":
                self.word += u"る"
        
    # Conjugates potential form
    def step4(self):
        if self.wordg[1] == "pot":
            if self.wordg[0] == "one":
                    pass
                #self.word = self.word[:-1] + self.ulist[self.wordlist.index(self.word[-1])] += u"る"
        
    # Conjugates imperative form
    def step5(self):
        # This only works for group two imperative verbs because it isn't possible to recognise group one verbs without
        # mistaking for a different kind of verb.
        # This only adds "る" to the end of the word.
        if self.wordg[1] == "imp" and self.wordg[0] == "two":
            self.word += u"る"

    # Conjugates volitional form
    def step6(self):
        # If wordg == "vol" and "one", it gets the last character's index in it's appropriate list and replaces it with
        # a character in "u" list that has the same index.
        if self.wordg[1] == "vol":
            if self.wordg[0] == "one":
                self.word += self.ulist[self.olist.index(self.ending[0])]
            # If the word is group two, it adds "る" to the end.
            elif self.wordg[0] == "two":
                self.word += u"る"
        
    # Conjugates passive form
    def step7(self):
        # If wordg == "one" and "pass", it gets the last character's index in it's appropriate list and replaces it with
        # a character in "u" list with the same index.
        if self.wordg[1] == "pass":
            if self.wordg[0] == "one":
                self.word = self.word[:-1] + self.ulist[self.wordlist.index(self.word[-1])]
        # Not how step7 doesn't process group 2 verbs, that is because it is also impossible to tell group two passive
        # verbs from other kinds of verbs.
        
    # Conjugates causative
    def step8(self):
        # This functions the same as most of the other steps, using the index of a character in a list to change it with
        # a character with the same index in a different list.
        if self.wordg[1] == "cause":
            if self.wordg[0] == "one":
                self.word = self.word[:-1] + self.ulist[self.wordlist.index(self.word[-1])]
            # "る" is added to the end here as well.
            elif self.wordg[0] == "two":
                self.word += u"る"
        
def stemming(w):
    stem = JPStemmer()
    return stem.stemmer(w)

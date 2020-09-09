#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 05:40:56 2018

@author: Rizo Rakhmanov
"""
import string




def CaesarCipher(message, n):
    """Encrypts/decrypts an input message using Caesar Cipher, applying a 
    constant shift of n. Does not change input message.
    
    Preconditions:
        message: a (possibly empty) string. Symbols, spaces, and uppercase
            letters are allowed, but the output won't contain either of the listed
            (uppercase letters will be flattened, the rest - removed).
        n: an integer; can be less than 0.
    """
    import string
    
    assert type(message) == str and type(n) == int, "invalid input!"
    
    if len(message) == 0:
        return ""
    
    input_string = ""
    output_string = ""
    
    for i in range(len(message)):
        if message[i] in string.ascii_uppercase:
            input_string += message[i].lower()
        elif message[i] in string.ascii_lowercase:
            input_string += message[i]
    
    for j in range(len(input_string)):
        number = string.ascii_lowercase.find(input_string[j])
        number += n
        number = number % 26
        newValue = string.ascii_lowercase[number]
        output_string += newValue
    
    return output_string
    

def VigenereCipher(message, keyWord, action = "decrypt"):
    """Encrypts/decrypts an input message using Vigenere Cipher, applying a 
    changing shift derived from a key word. Does not change input values.
    Action is the order to whether do encryption or decryption, using the 
    key word. Action can whether be "encrypt" or "decrypt" (set by default).
    
    Preconditions:
        message: a (possibly empty) string. Symbols, spaces, and uppercase
            letters are allowed, but the output won't contain either of the 
            listed (uppercase letters will be flattened, the rest - removed).
        key_word: a non-empty string that only contains letters. Uppercase letters
            will be flattened
        action: a string, whether "encrypt" or "decrypt". By default it is set
        to "decrypt".
    """
    import string
    
    assert type(message) == str and type(keyWord) == str and len(keyWord) != 0, "invalid input!"
    for i in range(len(keyWord)):
        assert keyWord[i] in string.ascii_letters, "invalid key word!"
    
    if len(message) == 0:
        return ""
    
    input_string = ""
    input_word = ""
    output_string = ""
    shift_values = []
    counter = 0


    for i in range(len(message)):
        if message[i] in string.ascii_uppercase:
            input_string += message[i].lower()
        elif message[i] in string.ascii_lowercase:
            input_string += message[i]
    
    for j in range(len(keyWord)):
        if keyWord[j] in string.ascii_uppercase:
            input_word += keyWord[j].lower()
        elif keyWord[j] in string.ascii_lowercase:
            input_word += keyWord[j]
    
    for k in range(len(input_word)):
        shiftValue = string.ascii_lowercase.find(input_word[k])
        shift_values.append(shiftValue)
    
    for index in range(len(input_string)):
        position = string.ascii_lowercase.find(input_string[index])
        if action == "encrypt":
            position += shift_values[counter]
        elif action == "decrypt":
            position -= shift_values[counter]
        position = position % 26
        value = string.ascii_lowercase[position]
        output_string += value
        counter += 1
        counter = counter % len(input_word)
    
    return output_string

    
class Letter():
    """A helper Letter Class, which has two components: x- and y- coordinates."""
        
    def __init__(self, letter, x, y):
        self.letter = letter
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "Letter " + str(self.letter) + "; x: " + str(self.x) + "; y: " + str(self.y)

def PolybiusSquareCipherDecrypt(message, letterCompressed = "I", isReversed = False):
    """Applies Polybius Square Cipher to decrypt a given message. Because 
    Polybius Square only contains 25 cells, one of the 26 alphabetical letters
    has to be compressed. The first of the two compressed letters have to be
    given (e.g. if "I" is given as letterCompressed, one of the squares will
    be "I/J"). By default, the row number ("y-coodinate") goes first, column
    number ("x-coordinate") - second. If needed vice versa, "True" has to 
    be given for isReversed. 
    Function does not change any of the inputs.
    
    Preconditoins:
        message: a (possibly empty) string that only contains numbers. If the
        length of message is odd, the last element is ignored.
        letterCompressed: a non-empty string that ONLY contains one of the two 
        letters that are to be compressed. Can be either upper- or lowercase.
        isReversed: a boolean.
    """
    
    assert type(message) == str and type(letterCompressed) == str and \
    len(letterCompressed) == 1 and type(isReversed) == bool, "invalid input!"
    
    inputList = []
    pairedList = []
    inputLetter = letterCompressed.upper()
    output = ""
    #create a new Polybius Square using Letter class objects
    lettersList = createPolybiusSquare(5, 5, inputLetter)
    
    if len(message) % 2 != 0:
        upperValue = len(message) - 1
    else:
        upperValue = len(message)
        
    for i in range(upperValue):
        inputList.append(int(message[i]))
    
    for j in range(len(inputList) // 2):
        pairedList.append([inputList[j*2], inputList[j*2+1]])
    
    
    if isReversed:
        xCorPos = 0
        yCorPos = 1
        
    else:
        xCorPos = 1
        yCorPos = 0
    
    for element in pairedList:
        elementXPos = element[xCorPos]
        elementYPos = element[yCorPos]
        lettersFound = findLetterInListByPosition(elementXPos, elementYPos, lettersList)
        if type(lettersFound) == list:
            output += "("
            for i in range(len(lettersFound)):
                output += lettersFound[i].letter
                if i != len(lettersFound) - 1:
                    output += "/"
            output += ")"
        else:
            output += lettersFound.letter
    
    return output
        
    
    
def createPolybiusSquare(rows = 5, columns = 5, letterCompressed = "I"):
    """Helper function for Polybius Square Cipher. Creates a Polybius Square
    with given number of rows and columns. Returns a list of the Letter class
    objects.

    Preconditions:
        rows, columns: integers > 0;
        letterCompressed: a non-empty string containing ONE UPPERCASE letter
    """
    
    xPosSetup = 1
    yPosSetup = 1
    lettersList = []
    
    divider = string.ascii_uppercase.find(letterCompressed)
    for k in range(divider + 1):
        letter = Letter(string.ascii_uppercase[k], xPosSetup, yPosSetup)
        lettersList.append(letter)
        if k == divider:
            additionalLetter = Letter(string.ascii_uppercase[k+1], xPosSetup, yPosSetup)
            lettersList.append(additionalLetter)
        xPosSetup += 1
        if xPosSetup > columns:
            xPosSetup = 1
            yPosSetup += 1
            if yPosSetup > rows: 
                break
    for k in range(divider + 2, 26):
        letter = Letter(string.ascii_uppercase[k], xPosSetup, yPosSetup)
        lettersList.append(letter)
        xPosSetup += 1
        if xPosSetup > columns:
            xPosSetup = 1
            yPosSetup += 1
            if yPosSetup > rows: 
                break
    
    return lettersList
   

def findLetterInListByPosition(x, y, letterList):
    """Helper function for Polybius Square Cipher. finds a letter by its 
    x and y positions in a list of Letter class objects. In case there are 
    several letters on the same position, returns a list of the Letter objects.
    In other cases, returns a single Letter object. Returns '_' if not found.
    
    Preconditions:
    x, y: integers > 0;
    letterList: a non-empty list of Letter objects
    """
    output = []
    for letter in letterList:
        if letter.x == x and letter.y == y:
            output.append(letter)
    if len(output) == 0:
        return "_"
    if len(output) == 1:
        return output[0]
    else:
        return output
    

        
def convertToBase10(number, base = 2):
    """Converts an input number from a given base (2 by default) 
    to base 10. Returns an integer.
    
    Preconditions: 
        number: is whether an integer or a string representing
                an integer that only contains digits 0 through 3, inclusively.
        base: a positive integer <= 10.
    """
    #assert type of input is right
    assert type(number) == int or type(number) == str, "invalid input!"
    
    #a parameter keeping the information about input type
    isString = False
    if type(number) == str:
        isString = True

    #string version of input, which is going to be used in the function
    stringValue = str(number)
        
    #a parameter keeping the information about whether input is negative or not
    isNegative = False
    if isString:
        if stringValue[0] == "-":
            isNegative = True
            #need to remove "-" sign from stringValue
            stringValue = stringValue[1:]
    else:
        if number < 0:
            isNegative = True
            #need to remove "-" sign from stringValue
            stringValue = stringValue[1:]

    #checking that, in case if input is a string, it only contains integers
    if isString:
        for i in range(len(stringValue)):
            try:
                int(stringValue[i])
            except ValueError:
                raise ValueError("input has to contain integers only!")
    
    #checking that only integers below base maximum are used
    for i in range(len(stringValue)):
        assert int(stringValue[i]) < base, "no digits bigger than %r allowed!" %(base - 1)


    #actual value calculation part
    outputValue = 0
    
        
    for i in range(len(stringValue)):
        power = (len(stringValue) - 1) - i
        value = (base ** power) * int(stringValue[i])
        outputValue += value
    
    if isNegative:
        outputValue *= -1
    
    return outputValue
            
 
def convertFromBase10(number, base = 2, outputLength = 0):
    """Converts an input number from base 10 to a given base (2 by default).
    Returns a string of length outputLength ("-" sign does not count)
    representing a number.
    
    Preconditions: 
        number: is whether an integer or a string representing
                an integer that only contains digits 0 through 3, inclusively;
        base: a positive integer <= 10;
        outputLength: a positive integer.
    """
    #assert type of input is right
    assert type(base) == int and type(outputLength) == int and \
    (type(number) == int or type(number) == str), "invalid input!"
    
    #assert outputLength is not negative
    assert outputLength >= 0, "output length cannot be negative!"
    
    #a parameter keeping the information about input type
    isString = False
    if type(number) == str:
        isString = True

    #string version of input, which is going to be used in the function
    stringValue = str(number)
        
    #a parameter keeping the information about whether input is negative or not
    isNegative = False
    if isString:
        if stringValue[0] == "-":
            isNegative = True
            #need to remove "-" sign from stringValue
            stringValue = stringValue[1:]
    else:
        if number < 0:
            isNegative = True
            #need to remove "-" sign from stringValue
            stringValue = stringValue[1:]

    #checking that, in case if input is a string, it only contains integers
    if isString:
        for i in range(len(stringValue)):
            try:
                int(stringValue[i])
            except ValueError:
                raise ValueError("input has to contain integers only!")
    


    #actual value calculation part
    inputValue = int(stringValue)
    outputString = ""
    
    
    while inputValue > 0:
       outputString = str(inputValue % base) + outputString
       inputValue //= base
    
    #making the final answer as long as needed
    if len(outputString) < outputLength:
        difference = outputLength - len(outputString)
        for i in range(difference):
            outputString = "0" + outputString
    
    if isNegative:
        outputString = "-" + outputString
    
    return outputString


def XOR(string1, string2):
    """Conducts an XOR operation on string1 vs string 2. Returns a binary
    output string. In case strings have different lengths, an output string
    will have a length same as that of a shorter input string.
    
    Preconditions:
        string1, string2: strings that only contain digits 1 and 0.
    """
    assert type(string1) == str and type(string2) == str, "Invalid input!"
    
    for i in range(len(string1)):
        assert string1[i] == "1" or string1[i] == "0", "only binary numbers!"
    for j in range(len(string2)):
        assert string2[j] == "1" or string2[j] == "0", "only binary numbers!"

    outputLength = min(len(string1), len(string2))
    outputString = ""
    
    for i in range(outputLength):
        booleanValue1 = (string1[i] == "1")
        booleanValue2 = (string2[i] == "1")
        if booleanValue1 != booleanValue2:
            currentValue = "1"
        else:
            currentValue = "0"
        outputString += currentValue
    
    return outputString
        
def convertTextToBinary(text, positiveValue = "vowels"):
    """A function that converts a given text into a binary. If "consonants" is
    given for positiveValue, each consonant will be converted to 1, and vowel
    will be converted to 0. By default, positiveValue is set to "vowels", i.e.
    each vowel is 1 and consonant is 0. Spaces and other symbols will be 
    ignored. Returns a string. Does not change input.
    Note: 'y' is approached as a vowel.
    
    Preconditions:
        text: a (possibly empty) string;
        positiveValue: a string, whether "vowels" or "consonants"
    """
    assert type(text) == str and (positiveValue == "vowels" or \
    positiveValue == "consonants"), "invalid input!"
    
    output = ""           
    vowels = "aeiouy"
    inputString = ""
    for i in range(len(text)):
        if text[i] in string.ascii_letters:
            element = text[i].lower()
            inputString += element
    
    for j in range(len(inputString)):
        if inputString[j] in vowels:
            output += "1"
        else:
            output += "0"
    
    return output


message0 = "20,33,22,21,00,33,30,01,02,20,22,02,32,20,11,33,03,30,03,32,03,00, \
            22,01,33,23,23,10,03,22,13,13,20,01,11,03,22,20,20,20,22,33,20,13,23, \
            13,33,22,30,33,01,20,21,10,12,11,00,32,23,13,22,02,00,10,31,02,33, \
            20,31,03,12,01,11,33,32,23,02,01,00,32,10,10,30,01,10,23,31,10,02, \
            00,30,23,31,10,03,03,01,02,33,02,23,21,30,12,03,12,22,00,03,13, \
            31,00,10,11,21,03,23,02,20,13,02,32,30,31,23,33,20,02,12,33,30, \
            00,30,12,30,13,03,01,03,03,23,22,02,30,20,03,22,23,32,23,02,02, \
            31,20,23,13,30,02"
    
initialCoordinatesList = message0.split(",")
for index in range(len(initialCoordinatesList)):
    if len(initialCoordinatesList[index]) > 2:
        length = len(initialCoordinatesList[index])
        initialCoordinatesList[index] = initialCoordinatesList[index][length - 2:] 


convertedList = []
for element in initialCoordinatesList:
    value = convertToBase10(element, 4)
    convertedList.append(value)
binaryList = []
for element in convertedList:            
    value = convertFromBase10(element, 2, 4)
    binaryList.append(value)
binaryNumber = ""
for element in binaryList:
    binaryNumber += element
    
article = "The whole grain goodness of blue chip dividend stocks has its \
limits. Utility stocks, consumer staples, pipelines, telecoms and real estate \
investment trusts have all lost ground over the past month, even while the \
broader market has been flat. With the bond market signalling an expectation \
of rising interest rates, the five-year rally for steady blue-chip dividend \
payers has stalled. Should you be scared if you own a lot of these stocks \
either directly or through mutual funds or exchange-traded funds? David \
Baskin, president of Baskin Financial Services, has a two-pronged answer: \
Keep your top-quality dividend stocks, but be prepared to follow his firm's \
example in trimming holdings in stocks such as TransCanada Corp., Keyera \
Corp. and Pembina Pipeline Corp.Let's have Mr. Baskin run us through his \
thinking on dividend stocks, which are a big part of the portfolios his firm \
puts together for clients." 

binaryArticle = convertTextToBinary(article, "vowels")
binaryXOR = XOR(binaryNumber, binaryArticle)

coordinatesList = []
length = len(binaryXOR) // 6
for i in range(length):
    coordinate1 = binaryXOR[6*i:6*i+3]
    coordinate2 = binaryXOR[6*i+3:6*i+6]
    coordinatesList.append([coordinate1, coordinate2])
    
convertedCoordinatesList = []
for i in range(len(coordinatesList)):
    coordinate1 = convertToBase10(coordinatesList[i][0], 2)
    coordinate2 = convertToBase10(coordinatesList[i][1], 2)
    convertedCoordinatesList.append([coordinate1, coordinate2])
    
#create Spiraled Polybius Square
def SpiraledPolybiusSquare():
    """Creates a spiraled 6x6 Polybius squared with rows and columns marked
    0 through 5.
    """
    spiralList = []
    counter = 0
    numCounter = 0
    xLower = 0
    xUpper = 6
    yLower = 0
    yUpper = 6
    xPosCounter = 0
    yPosCounter = 0

    #create order for rows and columns that stay constant
    positionsList = [0, 5, 1, 4, 2, 3]
    digits = "0123456789"

    #put in letters
    while True:
        for i in range(xLower, xUpper):
            if counter > 25:
                break
            letter = Letter(string.ascii_uppercase[counter], 5 - i, positionsList[yPosCounter])
            spiralList.append(letter)
            counter += 1
        yPosCounter += 1
        yLower += 1
        for j in range(yLower, yUpper):
            if counter > 25:
                break
            letter = Letter(string.ascii_uppercase[counter], positionsList[xPosCounter], j)
            spiralList.append(letter)
            counter += 1
        xPosCounter += 1
        xLower += 1
        for i in range(xLower, xUpper):
            if counter > 25:
                break
            letter = Letter(string.ascii_uppercase[counter], i, positionsList[yPosCounter])
            spiralList.append(letter)
            counter += 1
        yPosCounter += 1
        yUpper -= 1
        for j in range(yLower, yUpper):
            if counter > 25:
                break
            letter = Letter(string.ascii_uppercase[counter], positionsList[xPosCounter], 5 - j)
            spiralList.append(letter)
            counter += 1
        xPosCounter += 1
        xUpper -= 1
        if counter > 25:
            break
    #put in numbers
    for i in range(1, 5):
        number = Letter(digits[numCounter], i, 4)
        spiralList.append(number)
        numCounter += 1
    for j in range(2, 4):
        number = Letter(digits[numCounter], 4, 5 - j)
        spiralList.append(number)
        numCounter += 1
    for i in range(2, 4):
        number = Letter(digits[numCounter], 5 - i, 2)
        spiralList.append(number)
        numCounter += 1
    for j in range(3, 4):
        number = Letter(digits[numCounter], 2, j)
        spiralList.append(number)
        numCounter += 1
    for i in range(3, 4):
        number = Letter(digits[numCounter], i, 3)
        spiralList.append(number)
        numCounter += 1
    return spiralList

spiraledSquare = SpiraledPolybiusSquare()
finalMessage = ""
for element in convertedCoordinatesList:
    letter = findLetterInListByPosition(element[0], element[1], spiraledSquare)
    if type(letter) == str:
        finalMessage += letter
    else:
        finalMessage += letter.letter

finalAnswer = "Start. CIBC Bank. See Schematics for alarm and vault. \
Hit tomorrow at 10 AM, after alarm test. Vault code is 5567. Meet at Blackout. End."

message1 = "gluhtlishjrvbadvyyplkaohavbyjpwolypzavvdlhrvuuleatlzzhnlzdpajoavcpnlulyljpwolyrlfdvykpzaolopkkluzftivsvmklhaoputfmhcvypalovsilpuluk"
message2 = "vwduwljudeehghyhubwklqjlfrxogilqgsohdvhuhwxuqdqbeoxhsulqwviruydxowdqgdodupghvljqedvhgrqzklfkedqnbrxghflghrqldpvhwwlqjxsvdihkrxvhfr"
message3 = "Klkbnqlcytfysryucocphgbdizzfcmjwkuchzyeswfogmmetwwossdchrzyldsbwnydednzwnefydthtddbojicemlucdygicczhoadrzcylwadsxpilpiecskomoltejtkmqqymehpmmjxyolwpeewjckznpccpsvsxauyodhalmriocwpelwbcniyfxmwjcemcyrazdqlsomdbfljwnbijxpddsyoehxpceswtoxwbleecsaxcnuetzywfn"
message4 = "44541134541123335344541242434244325141212311311353155442544244424344325141534354324234411125513553341342432253431144543453432251343142143251341253341215541534513351444411225144425442444415345123551543213451111311212351425431533321424351445315341434512542531544335154325341443"
message5 = "43513544"

clue1Answer = "Start. I grabbed everything I could find. PLease return any \
              blueprints for vault and alarm design, based on which bank \
              you decide on. I am setting up safe house. Cozename Blackout \
              worried that our cipher is too weak. On next message switch \
              to Vigenere cipher. Keyword is the hidden symbol of death in \
              my favorite Holbein. End."

clue2Answer = "Start. Warning! I heard report of our break-in on the news! \
              Still waiting on alarm test schedules. I will report back \
              tomorrow with final plan. For extra security, I suggest we \
              burn our letters after reading and switch our letters to \
              numbers using Polybius Square. Drop messages under the bench \
              at train station. End."

clue3Answer = "Start. Almost finished Blackout. It is in Shed on Third Ave. \
              Working on a stronger cipher for future messages. It is surely \
              unbreakable! It combines our previous methods... News..."
            


#def updatePosition(xPos, yPos, columns = 5, rows = 5):
#    """Helper function for Polybius Square Cipher. Increments the position
#    of an element inside a square by 1. Goes back to the first position in a
#    square if the maximum position is reached. Returns nothing.
#    
#    Preconditions:
#        xPos, yPos, columns, rows: integers > 0.
#    """
#    xPos += 1
#    if xPos > columns:
#        xPos = 1
#        yPos +=1
#    if yPos > rows:
#        xPos = 1
#        yPos = 1
#    return
#first attempt at making a virtual engima machine
# Jan 2025
# Mark Reed

#NO NOTCH/TURNOVER YET, but it is working!!!!

#I could do with numbering my rotors 1 2 3, but I did it this way.

# R
# E         <-      R3      <-      R2      <-      R1      <-      E
# F
# L                                                                 T
# E         
# C         ->      R3      ->      R2      ->      R1      ->      W
# T

#Rotor settings from website https://enigma.virtualcolossus.co.uk/technical.html

#Wheel	ABCDEFGHIJKLMNOPQRSTUVWXYZ	Notch	Turnover	No. Notches
#ETW	ABCDEFGHIJKLMNOPQRSTUVWXYZ	 	 	 
#I	    EKMFLGDQVZNTOWYHXUSPAIBRCJ	  Y	        Q	        1
#II	    AJDKSIRUXBLHWTMCQGZNPYFVOE	  M	        E	        1
#III	BDFHJLCPRTXVZNYEIWGAKMUSQO	  D	        V	        1
#IV	    ESOVPZJAYQUIRHXLNFTGKDCMWB	  R	        J	        1
#V	    VZBRGITYUPSDNHLXAWMJQOFECK	  H	        Z	        1

# REFLECTORS
#       ABCDEFGHIJKLMNOPQRSTUVWXYZ	
#UKW-A	EJMZALYXVBWFCRQUONTSPIKHGD	 	  - NOT USING THIS ONE... 	 
#UKW-B	YRUHQSLDPXNGOKMIEBFZCWVJAT	 	 	 
#UKW-C	FVPJIAOYEDRZXWGCTKUQSBNMHL

#Testing done using virtual enigma machine!
# https://www.101computing.net/enigma/

#Tech details about ring settings, etc.
# https://www.ciphermachinesandcryptology.com/en/enigmatech.htm

ETW	        = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DEBUG = False
SPACING = 5

def LetterToPos(someLetter):
    val = ord(someLetter)
    return val - 65

def PosToLetter(somePos):
    letter = chr(somePos + 65)
    return letter

def MakeForwardsMappingList(someList):
    forwardsMapping = []
    pos = 0
    for letter in someList:
        diff = LetterToPos(letter) - pos
        forwardsMapping.append(diff)
        pos = pos + 1
    return forwardsMapping

def MakeBackwardsMappingList(someList):
    backwardsMapping = []
    for i in range(26):
        currentLetter = ETW[i]
        pos = someList.index(currentLetter)
        diff = pos - i
        backwardsMapping.append(diff)
    return backwardsMapping

if(DEBUG):
    pos = 0
    for letter in ETW:
        print(str(pos) + ":" + letter)
        pos = pos + 1

ROTOR_I     = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_I_NUMS = MakeForwardsMappingList(ROTOR_I)
ROTOR_I_NUMS_BACK = MakeBackwardsMappingList(ROTOR_I)

ROTOR_II    = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_II_NUMS = MakeForwardsMappingList(ROTOR_II)
ROTOR_II_NUMS_BACK = MakeBackwardsMappingList(ROTOR_II)

ROTOR_III   = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
ROTOR_III_NUMS = MakeForwardsMappingList(ROTOR_III)
ROTOR_III_NUMS_BACK = MakeBackwardsMappingList(ROTOR_III)

#ROTOR_IV    = ["E","S","O","V","P","Z","J","A","Y","Q","U","I","R","H","X","L","N","F","T","G","K","D","C","M","W","B"]
#ROTOR_V     = ["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"]
#UKW_A       = ["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"]	 	 	 
UKW_B       = "YRUHQSLDPXNGOKMIEBFZCWVJAT"	 
UKW_B_NUMS = MakeForwardsMappingList(UKW_B)

UKW_C       = ["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"]
UKW_C_NUMS = MakeForwardsMappingList(UKW_C)

class Rotor():
    def __init__(self,newRotorType,newPos):
        if(newRotorType == "I"):
            self.rotorMapping = ROTOR_I_NUMS
            self.rotorMappingBackwards = ROTOR_I_NUMS_BACK
            self.notch = "Y"
            self.turnover = "Q"
        elif(newRotorType == "II"):
            self.rotorMapping = ROTOR_II_NUMS
            self.rotorMappingBackwards = ROTOR_II_NUMS_BACK
            self.notch = "M"
            self.turnover = "E"
        elif(newRotorType == "III"):
            self.rotorMapping = ROTOR_III_NUMS
            self.rotorMappingBackwards = ROTOR_III_NUMS_BACK
            self.notch = "D"
            self.turnover = "V"
        
        self.InitialiseRotorPos(newPos)

    def InitialiseRotorPos(self,someLetter):
        somePos = ord(someLetter) - 65
        while(somePos > 0):
            self.Rotate()
            somePos = somePos - 1

    def GetMappingNumber(self,inputValue,forward=True):
        newPos = 0

        if(forward):
            newPos = inputValue + self.rotorMapping[inputValue]
        else:
            newPos = inputValue + self.rotorMappingBackwards[inputValue]

        if(newPos > 25):
            newPos = newPos - 26

        if(newPos < 0):
            newPos = 26 + newPos

        return newPos
        
    def Rotate(self):
        firstThing = self.rotorMapping.pop(0)
        self.rotorMapping.append(firstThing)

        firstThing = self.rotorMappingBackwards.pop(0)
        self.rotorMappingBackwards.append(firstThing)

        #Should really return true or false to say if notch is moving the next wheel across!
        #TODO

#TODO - inheritance?  The rotors are like the reflector but they have rotation too!
class Reflector():
    def __init__(self,newReflectorType):
        if(newReflectorType == "B"):
            self.reflectorMapping = UKW_B_NUMS
        elif(newReflectorType == "C"):
            self.reflectorMapping = UKW_C_NUMS

    def GetMappingNumber(self,inputValue):
        return self.reflectorMapping[inputValue]

class PlugBoard():
    def __init__(self):
        self.plugList = []
    
    def AddPlugPair(self,someNewPair):
        self.plugList.append(someNewPair)
    
    def CheckForPlugLink(self,someLetter):
        newLetter = someLetter

        for pair in self.plugList:
            first = pair[0]
            second = pair[1]

            if(someLetter == first):
                newLetter = second
                return newLetter
            elif(someLetter == second):
                newLetter = first
                return newLetter

        return newLetter

class Enigma():
    def __init__(self,newRotor1,newRotor2,newRotor3,newReflector,newPlugBoard):
        self.rotor1 = newRotor1
        self.rotor2 = newRotor2
        self.rotor3 = newRotor3
        self.reflector = newReflector
        self.thePlugBoard = newPlugBoard

    def PrintAllRotors(self):
        print(self.rotor1.rotorMapping)
        print(self.rotor2.rotorMapping)
        print(self.rotor3.rotorMapping)
        print(self.reflector.reflectorMapping)

    def scrambleMessage(self,incoming):

        cypher = ""
        letterCount = 1
        for letter in incoming:
            if(DEBUG):
                print("Working on letter : " + letter)
                print("---------------------")

            
            self.rotor1.Rotate()  #It rotates BEFORE the cypher happens!!!

            if(DEBUG):
                self.PrintAllRotors()

            #plugboard first time through...
            letterBeforePlugBoard = self.thePlugBoard.CheckForPlugLink(letter)
            r1In = LetterToPos(letterBeforePlugBoard)
            r1Out = self.rotor1.GetMappingNumber(r1In)
            r1OutLetter = PosToLetter(r1Out)
            if(DEBUG):
                print("<-R1 : " + letter + " -> " + PosToLetter(r1Out))
                print(str(r1In) + ">>" + str(r1Out))

            r2Out = self.rotor2.GetMappingNumber(r1Out)
            if(DEBUG):
                print("<-R2 : " + PosToLetter(r1Out) + " -> " + PosToLetter(r2Out))
                print(str(r1Out) + ">>" + str(r2Out))

            r3Out = self.rotor3.GetMappingNumber(r2Out)
            if(DEBUG):
                print("<-R3 : " + PosToLetter(r2Out) + " -> " + PosToLetter(r3Out))
                print(str(r2Out) + ">>" + str(r3Out))

            refOut =  self.reflector.GetMappingNumber(r3Out) + r3Out
            if(DEBUG):
                print("<Ref>: " + PosToLetter(r3Out) + " -> " + PosToLetter(refOut))
                print(str(r3Out) + ">>" + str(refOut))

            #Now pass the signal back wards through III, II, I rotors...
            r3BackOut =  self.rotor3.GetMappingNumber(refOut,False)
            if(DEBUG):
                print("r3->: " + PosToLetter(refOut) + " -> " + PosToLetter(r3BackOut))
                print(str(refOut) + ">>" + str(r3BackOut))

            r2BackOut =  self.rotor2.GetMappingNumber(r3BackOut,False)
            if(DEBUG):
                print("r2->: " + PosToLetter(r3BackOut) + " -> " + PosToLetter(r2BackOut))
                print(str(r3BackOut) + ">>" + str(r2BackOut))

            r1BackOut =  self.rotor1.GetMappingNumber(r2BackOut,False)
            if(DEBUG):
                print("r1->: " + PosToLetter(r2BackOut) + " -> " + PosToLetter(r1BackOut))
                print(str(r2BackOut) + ">>" + str(r1BackOut))

            if(DEBUG):
                print("---------------------")


            letterBeforePlugBoard = PosToLetter(r1BackOut)

            #Check for a final plugboard swap
            afterPlugBoard = self.thePlugBoard.CheckForPlugLink(letterBeforePlugBoard)
            
            cypher = cypher + afterPlugBoard
            
            if(letterCount == SPACING):
                letterCount = 1
                cypher = cypher + " "
            else:
                letterCount = letterCount + 1

            #TODO
            #ROTORS 2 and 3 HAVE TO MOVE - "NOTCHES" !!!! etc.

        return cypher

inText = "AAAAS SSS"
inTextWithoutSpaces = inText.upper().replace(" ", "")

if(DEBUG):
    print("Plain text : " + inText)

#Initial rotor settings - set by person sending the code
#This is AAA really, because it moves once before the first letter is encoded.
userSetting = "AAZ"

r1 = Rotor("I",userSetting[2])
r2 = Rotor("II",userSetting[1])
r3 = Rotor("III",userSetting[0])
ref = Reflector("B")
myPlugBoard = PlugBoard()
myPlugBoard.AddPlugPair(["A","W"])
myPlugBoard.AddPlugPair(["H","Z"])
myPlugBoard.AddPlugPair(["B","L"])

theEnigma = Enigma(r1,r2,r3,ref,myPlugBoard)

if(DEBUG):
    theEnigma.PrintAllRotors()

outText = theEnigma.scrambleMessage(inTextWithoutSpaces)

print("Plain text : " + inText)
print("Cypher     : " + outText)
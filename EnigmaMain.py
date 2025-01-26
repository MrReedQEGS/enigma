#first attempt at making a virtual engima machine
# Jan 2025
# Mark Reed

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
#UKW-A	EJMZALYXVBWFCRQUONTSPIKHGD	 	 	 
#UKW-B	YRUHQSLDPXNGOKMIEBFZCWVJAT	 	 	 
#UKW-C	FVPJIAOYEDRZXWGCTKUQSBNMHL

# NO PLUGBOARD / "STECKER" at this stage...my brain hurts already

#Testing done using virtual enigma machine!
# https://enigma.virtualcolossus.co.uk/VirtualEnigma/


#Tech details about ring settings, etc.
# https://www.ciphermachinesandcryptology.com/en/enigmatech.htm

def LetterToPos(someLetter):
    val = ord(someLetter)
    return val - 65

def PosToLetter(somePos):
    letter = chr(somePos + 65)
    return letter

def TurnRotorsLettersIntoMappingNumbers(someList):
    answer = []
    for letter in someList:
        answer.append(LetterToPos(letter))
    return answer

ETW	        = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ROTOR_I     = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_I_NUMS = TurnRotorsLettersIntoMappingNumbers(ROTOR_I)

ROTOR_II    = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_II_NUMS = TurnRotorsLettersIntoMappingNumbers(ROTOR_II)

ROTOR_III   = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
ROTOR_III_NUMS = TurnRotorsLettersIntoMappingNumbers(ROTOR_III)

print(ROTOR_I_NUMS)

#ROTOR_IV    = ["E","S","O","V","P","Z","J","A","Y","Q","U","I","R","H","X","L","N","F","T","G","K","D","C","M","W","B"]
#ROTOR_V     = ["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"]
#UKW_A       = ["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"]	 	 	 
UKW_B       = "YRUHQSLDPXNGOKMIEBFZCWVJAT"	 
UKW_B_NUMS = TurnRotorsLettersIntoMappingNumbers(UKW_B)

#UKW_C       = ["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"]

class Rotor():
    def __init__(self,newRotorType,newPos):
        if(newRotorType == "I"):
            self.rotorMapping = ROTOR_I_NUMS
            self.notch = "Y"
            self.turnover = "Q"
        elif(newRotorType == "II"):
            self.rotorMapping = ROTOR_II_NUMS
            self.notch = "M"
            self.turnover = "E"
        elif(newRotorType == "III"):
            self.rotorMapping = ROTOR_II_NUMS
            self.notch = "D"
            self.turnover = "V"
        
        self.InitialiseRotorPos(newPos)

    def InitialiseRotorPos(self,somePos):
        while(somePos > 0):
            self.Rotate()
            somePos = somePos - 1

    def GetMappedLetter(self,inputValue,forward=True):
        if(forward):
            return self.rotorMapping[inputValue]
        else:
            pos = self.rotorMapping.index(inputValue)
            return pos
        
    def Rotate(self):
        #Move once the rotor forwards once - This puts the end letter onto the front of the list and shuffles things along
        lastThing = self.rotorMapping.pop()
        self.rotorMapping.insert(0,lastThing)
        
        #Should really return true or false to say if notch is moving the next wheel across!
        #TODO

class Enigma():
    def __init__(self,newRotor1,newRotor2,newRotor3):
        self.rotor1 = newRotor1
        self.rotor2 = newRotor2
        self.rotor3 = newRotor3

    def scrambleMessage(self,incoming):

        cypher = ""
        for letter in incoming:
            pos = LetterToPos(letter)
            self.rotor1.Rotate()  #It rotates BEFORE the cypher happens!!!
            finalLetter = ""
            r1Out = self.rotor1.GetMappedLetter(pos)
            cypher = cypher + PosToLetter(r1Out)

            #TO DO - must pass through all rotors twice and reflector
            #ROTORS HAVE TO MOVE - NOTCHES DO THINGS, etc.

        return cypher

inText = "aaa".upper()
print("In  : " + inText)

r1 = Rotor("I",25)
r2 = Rotor("I",0)
r3 = Rotor("I",0)

theEnigma = Enigma(r1,r2,r3)
outText = theEnigma.scrambleMessage(inText)
print("Out : " + outText)




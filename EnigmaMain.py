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

def TurnLetterMappingIntoMappingNumbers(someList):
    answer = []
    for letter in someList:
        answer.append(LetterToPos(letter))
    return answer

ETW	        = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

pos = 0
for letter in ETW:
    print(str(pos) + ":" + letter)
    pos = pos + 1

ROTOR_I     = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_I_NUMS = TurnLetterMappingIntoMappingNumbers(ROTOR_I)

ROTOR_II    = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_II_NUMS = TurnLetterMappingIntoMappingNumbers(ROTOR_II)
print(ROTOR_II_NUMS)


ROTOR_III   = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
ROTOR_III_NUMS = TurnLetterMappingIntoMappingNumbers(ROTOR_III)



#ROTOR_IV    = ["E","S","O","V","P","Z","J","A","Y","Q","U","I","R","H","X","L","N","F","T","G","K","D","C","M","W","B"]
#ROTOR_V     = ["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"]
#UKW_A       = ["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"]	 	 	 
UKW_B       = "YRUHQSLDPXNGOKMIEBFZCWVJAT"	 
UKW_B_NUMS = TurnLetterMappingIntoMappingNumbers(UKW_B)

UKW_C       = ["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"]
UKW_C_NUMS = TurnLetterMappingIntoMappingNumbers(UKW_C)

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
            self.rotorMapping = ROTOR_III_NUMS
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

#TO DO - inheritance?  The rotors are like the reflector but they have rotation too!
class Reflector():
    def __init__(self,newReflectorType):
        if(newReflectorType == "B"):
            self.reflectorMapping = UKW_B_NUMS
        elif(newReflectorType == "C"):
            self.reflectorMapping = UKW_C_NUMS

    def GetMappedLetter(self,inputValue,forward=True):
        #I feel like this only needs to work one way...have a think about it.
        if(forward):
            return self.reflectorMapping[inputValue]
        else:
            pos = self.reflectorMapping.index(inputValue)
            return pos


class Enigma():
    def __init__(self,newRotor1,newRotor2,newRotor3,newReflector):
        self.rotor1 = newRotor1
        self.rotor2 = newRotor2
        self.rotor3 = newRotor3
        self.reflector = newReflector

    def PrintAllRotors(self):
        print(self.rotor1.rotorMapping)
        print(self.rotor2.rotorMapping)
        print(self.rotor3.rotorMapping)

    def scrambleMessage(self,incoming):

        cypher = ""
        for letter in incoming:
            print("Working on letter : " + letter)
            print("---------------------")
            r1In = LetterToPos(letter)
            self.rotor1.Rotate()  #It rotates BEFORE the cypher happens!!!

            self.PrintAllRotors()
            
            r1Out = self.rotor1.GetMappedLetter(r1In)
            r1OutLetter = PosToLetter(r1Out)
            print("<-R1 : " + letter + " -> " + PosToLetter(r1Out))
            print(str(r1In) + ">>" + str(r1Out))

            r2Out = self.rotor2.GetMappedLetter(r1Out)
            print("<-R2 : " + PosToLetter(r1Out) + " -> " + PosToLetter(r2Out))
            print(str(r1Out) + ">>" + str(r2Out))

            r3Out = self.rotor3.GetMappedLetter(r2Out)
            print("<-R3 : " + PosToLetter(r2Out) + " -> " + PosToLetter(r3Out))
            print(str(r2Out) + ">>" + str(r3Out))

            refOut =  self.reflector.GetMappedLetter(r3Out)
            print("<Ref>: " + PosToLetter(r3Out) + " -> " + PosToLetter(refOut))
            print(str(r3Out) + ">>" + str(refOut))

            #Now pass the signal back wards through III, II, I rotors...
            r3BackOut =  self.rotor3.GetMappedLetter(refOut,False)
            print("r3->: " + PosToLetter(refOut) + " -> " + PosToLetter(r3BackOut))
            print(str(refOut) + ">>" + str(r3BackOut))

            r2BackOut =  self.rotor2.GetMappedLetter(r3BackOut,False)
            print("r2->: " + PosToLetter(r3BackOut) + " -> " + PosToLetter(r2BackOut))
            print(str(r3BackOut) + ">>" + str(r2BackOut))

            r1BackOut =  self.rotor1.GetMappedLetter(r2BackOut,False)
            print("r1->: " + PosToLetter(r2BackOut) + " -> " + PosToLetter(r1BackOut))
            print(str(r2BackOut) + ">>" + str(r1BackOut))

            cypher = cypher + PosToLetter(r1BackOut)
            print("---------------------")
            #TO DO - must pass through all rotors twice and reflector
            #ROTORS HAVE TO MOVE - NOTCHES DO THINGS, etc.

        return cypher

inText = "B".upper()
print("Plain text : " + inText)

r1 = Rotor("I",25)
r2 = Rotor("II",0)
r3 = Rotor("III",0)
ref = Reflector("B")
theEnigma = Enigma(r1,r2,r3,ref)

outText = theEnigma.scrambleMessage(inText)

print("Plain text : " + inText)
print("Cypher     : " + outText)
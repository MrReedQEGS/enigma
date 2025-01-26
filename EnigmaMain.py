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


ETW	        = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
ROTOR_I     = ["E","K","M","F","L","G","D","Q","V","Z","N","T","O","W","Y","H","X","U","S","P","A","I","B","R","C","J"]
ROTOR_II    = ["A","J","D","K","S","I","R","U","X","B","L","H","W","T","M","C","Q","G","Z","N","P","Y","F","V","O","E"]
ROTOR_III   = ["B","D","F","H","J","L","C","P","R","T","X","V","Z","N","Y","E","I","W","G","A","K","M","U","S","Q","O"]
ROTOR_IV    = ["E","S","O","V","P","Z","J","A","Y","Q","U","I","R","H","X","L","N","F","T","G","K","D","C","M","W","B"]
ROTOR_V     = ["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"]
UKW_A       = ["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"]	 	 	 
UKW_B       = ["Y","R","U","H","Q","S","L","D","P","X","N","G","O","K","M","I","E","B","F","Z","C","W","V","J","A","T"]	 	 	 
UKW_C       = ["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"]

def LetterToPos(someLetter):
    val = ord(someLetter)
    return val - 65

class Rotor():
    def __init__(self,newRotorType,newPos):
        if(newRotorType == "I"):
            self.rotorList = ROTOR_I
            self.notch = "Y"
            self.turnover = "Q"
        elif(newRotorType == "II"):
            self.rotorList = ROTOR_II
            self.notch = "M"
            self.turnover = "E"
        elif(newRotorType == "III"):
            self.rotorList = ROTOR_III
            self.notch = "D"
            self.turnover = "V"
        
        self.InitialiseRotorPos(newPos)

    def InitialiseRotorPos(self,somePos):
        while(somePos > 0):
            self.Rotate()
            somePos = somePos - 1

    def GetLetter(self,someLetter):
        pos = LetterToPos(someLetter)
        return self.rotorList[pos]

    def Rotate(self):
        #Move once the rotor once
        endLetter = self.rotorList.pop()
        self.rotorList.insert(0,endLetter)
        

class Enigma():
    def __init__(self,newRotor1,newRotor2,newRotor3):
        self.rotor1 = newRotor1
        self.rotor2 = newRotor2
        self.rotor3 = newRotor3

    def scrambleMessage(self,incoming):
        cypher = ""
        for letter in incoming:
            finalLetter = ""
            r1Out = self.rotor1.GetLetter(letter)
            finalLetter = r1Out
            cypher = cypher + finalLetter
            self.rotor1.Rotate()

            #TO DO - must pass through all rotors twice and reflector
            #ROTORS HAVE TO MOVE - NOTCHES DO THINGS, etc.

        return cypher

inText = "zzz".upper()
print("In  : " + inText)

r1 = Rotor("I",0)
r2 = Rotor("I",0)
r3 = Rotor("I",0)

theEnigma = Enigma(r1,r2,r3)
outText = theEnigma.scrambleMessage(inText)
print("Out : " + outText)




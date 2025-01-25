
DICT_I = {"A":"A","B":"A","C":"A",
          "D":"A","E":"A","F":"A",
          "G":"A","H":"A","I":"A",
          "J":"A","K":"A","L":"A",
          "M":"A","N":"A","O":"A",
          "P":"A","Q":"A","R":"A",
          "S":"A","T":"A","U":"A",
          "V":"A","W":"A","X":"A",
          "Y":"A","Z":"A"
          }

class Rotor():
    def __init__(newRotorType):
        if(newRotorType == "I"):
            rotorDict = DICT_I
        elif(newRotorType == "II"):
            rotorDict = DICT_I
        elif(newRotorType == "III"):
            rotorDict = DICT_I


class Enigma():
    def __init__(newRotor1,newRotor2,newRotor3):
        rotor1 = newRotor1
        rotor2 = newRotor2
        rotor3 = newRotor3

inWord = "HELLO"
print("Making cypher text of : " + inWord)

for letter in inWord:
    print(DICT_I[letter])


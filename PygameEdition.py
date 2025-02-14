import pygame,sys,UsefulClasses

#NEXT JOB - SELECTING ROTOR NUMBERS AND RING SETTINGS SHOULD COME FIRST.
    #      - THEN SOME SORT OF BUTTON TO ALLOW THEM TO CHANGE
    #      - A RESET FUNCTION WILL BE NEEDED TO START IT ALL AGAIN WITH NEW SETTINGS
          

#PYGAME EDITION - This is a front end for the text based 
#enigma routine that I made.

#first attempt at making a virtual engima machine
# 26th Jan 2025
# Mr Reed

#NO NOTCH/TURNOVER YET, but it is working apart from that

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
#ETW	  ABCDEFGHIJKLMNOPQRSTUVWXYZ	 	 	 
#I	    EKMFLGDQVZNTOWYHXUSPAIBRCJ	  Y	        Q	        1
#II	    AJDKSIRUXBLHWTMCQGZNPYFVOE	  M	        E	        1
#III	  BDFHJLCPRTXVZNYEIWGAKMUSQO	  D	        V	        1
#IV	    ESOVPZJAYQUIRHXLNFTGKDCMWB	  R	        J	        1
#V	    VZBRGITYUPSDNHLXAWMJQOFECK	  H	        Z	        1

#NOTCH Info
# The position of the notch is different for each of the rotors. 
# In the table above we can see that rotor I has a notch on letter Y. 
# If this notch is positioned in front of the pawl, the letter Q is visible in the little window.
# This means as Q passes out of the window it will cause the rotor on its left to move by 1 position.
#
# The ring settings, or Ringstellung, are used to change the position of the alphabet ring relative to the 
# internal wiring. The notch and alphabet ring are fixed together. Changing the ring setting will therefore change 
# the positions of the wiring, relative to the turnover-point and start position.

#RING SETTINGS INFO...
#A "user setting" of AAZ is the same as a "ring setting" of AAB.  It goes the other way!!!!!
#This means that I can use my "user settings" code to deal with "ring settings" as long as I turn B into Z or C into Y, etc.
#The above only needs doing once at the start just like the "user settings" process.  Should be easy!!!


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

ROTOR_IV   = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
ROTOR_IV_NUMS = MakeForwardsMappingList(ROTOR_IV)
ROTOR_IV_NUMS_BACK = MakeBackwardsMappingList(ROTOR_IV)

ROTOR_V   = "VZBRGITYUPSDNHLXAWMJQOFECK"
ROTOR_V_NUMS = MakeForwardsMappingList(ROTOR_V)
ROTOR_V_NUMS_BACK = MakeBackwardsMappingList(ROTOR_V)


#ROTOR_V     = ["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"]
#UKW_A       = ["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"]	 	 	 
UKW_B       = "YRUHQSLDPXNGOKMIEBFZCWVJAT"	 
UKW_B_NUMS = MakeForwardsMappingList(UKW_B)

UKW_C       = ["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"]
UKW_C_NUMS = MakeForwardsMappingList(UKW_C)

class Rotor():
    def __init__(self,newRotorType,newUserSetting,newRingSetting):
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
        elif(newRotorType == "IV"):
            self.rotorMapping = ROTOR_IV_NUMS
            self.rotorMappingBackwards = ROTOR_IV_NUMS_BACK
            self.notch = "R"
            self.turnover = "J"
        elif(newRotorType == "V"):
            self.rotorMapping = ROTOR_V_NUMS
            self.rotorMappingBackwards = ROTOR_V_NUMS_BACK
            self.notch = "H"
            self.turnover = "Z"
        
        self.InitialiseRotorPos(newUserSetting)
        
        #ring settings are like user settings but the opposite rotation
        convertedRingSetting = self.ConvertRingSettingToUserSetting(newRingSetting)
        self.InitialiseRotorPos(convertedRingSetting)
        
    def ConvertRingSettingToUserSetting(self, newRingSetting):
        #ring settings are like user settings but the opposite rotation
        #A ring setting of AAB is like a user setting of AAZ
        
        #This function convers from ring setting to user setting so I can use the same
        #initialisation function for both.  :)
        
        #A -> A - Do nothing
        #B -> Z user setting
        #C -> Y
        #etc.
        
        ringSettingValue = ord(newRingSetting) - 66
        ordOfZ = ord("Z")
        
        finalValue = ordOfZ - ringSettingValue
        
        if(finalValue > 90):
          finalValue = finalValue - 26
        
        return chr(finalValue)
        
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
    
    def RotateBackwards(self):
        numOfThings = len(self.rotorMapping)
        lastThing = self.rotorMapping.pop(numOfThings-1)
        self.rotorMapping.insert(0,lastThing)

        numOfThings = len(self.rotorMappingBackwards)
        lastThing = self.rotorMappingBackwards.pop(numOfThings-1)
        self.rotorMappingBackwards.insert(0,lastThing)
    
    def Rotate(self):
        firstThing = self.rotorMapping.pop(0)
        self.rotorMapping.append(firstThing)

        firstThing = self.rotorMappingBackwards.pop(0)
        self.rotorMappingBackwards.append(firstThing)

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
  
    def PrintPlugPairs(self):
      print("Plug board  : ",end="")
      for pair in self.plugList:
        print(pair,end = ",")
      print()

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

            #It rotates BEFORE the cypher happens!!!
            #Rotate the right most rotor
            RotorForward(2)

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

def RotorForward(rotorNum):
  
  #This bit does the graphics on the screen
  global userSetting
  oldletter = userSetting[rotorNum]
  num = ord(oldletter)
  num = num + 1
  if(num >= 65 + 26):
    num = 65
  newletter = chr(num)
  userSetting[rotorNum] = newletter
  
  #Now do the actual enigma rotor internally
  if(rotorNum == 0):
    theEnigma.rotor3.Rotate()
  if(rotorNum == 1):
    theEnigma.rotor2.Rotate()
    #The notch might make rotor 2 move by one place!
    #Rotor I does this when Q moves out of the window
    #and this is called the turnover
    if oldletter.upper() == theEnigma.rotor2.turnover:
      RotorForward(0)
  if(rotorNum == 2):
    theEnigma.rotor1.Rotate()
    #The notch might make rotor 2 move by one place!
    #Rotor I does this when Q moves out of the window
    #and this is called the turnover
    if oldletter.upper() == theEnigma.rotor1.turnover:
      RotorForward(1)
  
def RotorBackwards(rotorNum):
  global userSetting
  letter = userSetting[rotorNum]
  num = ord(letter)
  num = num - 1
  if(num < 65):
    num = 65 + 25
  letter = chr(num)
  userSetting[rotorNum] = letter
  
   #Now do the actual enigma rotor internally
  if(rotorNum == 0):
    theEnigma.rotor3.RotateBackwards()
  if(rotorNum == 1):
    theEnigma.rotor2.RotateBackwards()
  if(rotorNum == 2):
    theEnigma.rotor1.RotateBackwards()
  
def ChangeRotorNum(rotorNum):
  global rotorNumbers
  currentNum = rotorNumbers[rotorNum]
  pos = ROTOR_NUM_LIST.index(currentNum)
  pos = pos + 1
  if(pos >= len(ROTOR_NUM_LIST)):
    pos = 0
  rotorNumbers[rotorNum] = ROTOR_NUM_LIST[pos]
  
def DrawRotorText():
  rotor1Text = my_font.render(userSetting[0], False, (0, 0, 0))
  scrn.blit(rotor1Text, (170,62))
  
  rotor2Text = my_font.render(userSetting[1], False, (0, 0, 0))
  scrn.blit(rotor2Text, (232,62))
  
  rotor3Text = my_font.render(userSetting[2], False, (0, 0, 0))
  scrn.blit(rotor3Text, (294,62))

def DrawRotorNumbers():
  rotor1Num = my_font_small.render(rotorNumbers[0], False, (0, 0, 0))
  scrn.blit(rotor1Num, (171,135))
  
  rotor2Num = my_font_small.render(rotorNumbers[1], False, (0, 0, 0))
  scrn.blit(rotor2Num, (235,136))
  
  rotor3Num = my_font_small.render(rotorNumbers[2], False, (0, 0, 0))
  scrn.blit(rotor3Num, (297,136))

def CheckForUserSettingsChange():
  pos = pygame.mouse.get_pos()
  #print(pos)
  x = pos[0]
  y = pos[1]
  if(x >= 160 and x <= 200 and y >= 85 and y<= 115):
    RotorForward(0)
  elif(x >= 160 and x <= 200 and y >= 20 and y<= 53):
    RotorBackwards(0)
  elif(x >= 214 and x <= 260 and y >= 85 and y<= 115):
    RotorForward(1)
  elif(x >= 214 and x <= 260 and y >= 20 and y<= 53):
    RotorBackwards(1)
  elif(x >= 275 and x <= 330 and y >= 85 and y<= 115):
    RotorForward(2)
  elif(x >= 275 and x <= 330 and y >= 20 and y<= 53):
    RotorBackwards(2)
  elif(x >= 166 and x <= 187 and y >= 135 and y<= 150):
    ChangeRotorNum(0)
  elif(x >= 230 and x <= 251 and y >= 135 and y<= 150):
    ChangeRotorNum(1)
  elif(x >= 290 and x <= 313 and y >= 135 and y<= 150):
    ChangeRotorNum(2)
    
def UpdateCursor():
  #Change cursor to a hand when on a rotor setting button or rotor num button
  pos = pygame.mouse.get_pos()
  #print(pos)
  x = pos[0]
  y = pos[1]

  #The first 6 places where the cursor changes are the up and down arrows on the 3 rotors
  if(x >= 160 and x <= 200 and y >= 85 and y<= 115):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 160 and x <= 200 and y >= 20 and y<= 53):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 214 and x <= 260 and y >= 85 and y<= 115):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 214 and x <= 260 and y >= 20 and y<= 53):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 275 and x <= 330 and y >= 85 and y<= 115):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 275 and x <= 330 and y >= 20 and y<= 53):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 166 and x <= 187 and y >= 135 and y<= 150):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 230 and x <= 251 and y >= 135 and y<= 150):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  elif(x >= 290 and x <= 313 and y >= 135 and y<= 150):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
  else:
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 

def draw_circle_alpha(surface, color, center, radius):
    #pygame does not support transparent circles directly.  This is a workaround.
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def HighlightKeys(theSurface):
  for letter in keysToHightLight:
    draw_circle_alpha(theSurface, HIGHTLIGHT_COL, higlightMapping[letter], HIGHLIGHT_SIZE)

def DrawPlainAndCypherText(theSurface):
  plain = my_font_small.render("PLAIN    : " + thePlainText, False, (255, 255, 255))
  scrn.blit(plain, (7,760))
  cypher = my_font_small.render("CYPHER : " + theCypherText, False, (255, 255, 255))
  scrn.blit(cypher, (5,780))

def LightUpAKey(somekey):
  #Only works for lowercase key presses
  global thePlainText,theCypherText
  somekey = somekey - 32
  if(somekey < 65 or somekey > 65 + 26):
    somekey = 65
    
  thePressedKey = chr(somekey)
  outText = theEnigma.scrambleMessage(thePressedKey)
  keysToHightLight.append(outText)    
  thePlainText = thePlainText + thePressedKey
  theCypherText = theCypherText + outText
      
#PYGAME BIT

def MuteButtonCallback():
  print("Hello")





#Coords of highlight circles
higlightMapping = {"A":(105,256),"B":(348,311),"C":(235,311),"D":(218,257),
                   "E":(199,203),"F":(274,257),"G":(329,257),"H":(386,258),
                   "I":(479,205),"J":(442,258),"K":(498,258),"L":(516,312),
                   "M":(461,312),"N":(404,311),"O":(535,205),"P":(67,310),
                   "Q":(88,203),"R":(255,203),"S":(161,256),"T":(311,203),
                   "U":(423,204),"V":(291,311),"W":(143,203),"X":(180,310),
                   "Y":(123,310),"Z":(367,204)}

HIGHLIGHT_SIZE= 15
HIGHTLIGHT_COL = (255, 255, 51, 80)
keysToHightLight = []

userSetting = ["A","A","A"]
rotorNumbers = ["III","II","I"]
ROTOR_NUM_LIST = ["I","II","III","IV","V"]

thePlainText = ""
theCypherText = ""

pygame.init()

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 28)
my_font_small = pygame.font.SysFont('Comic Sans MS', 20)
  
X = 600
Y = 800
 
# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))

muteImageGreyName = "./images/MuteGrey.jpg"
muteImageName = "./images/Mute.jpg"
muteImage = pygame.image.load(muteImageName).convert()
muteGreyImage = pygame.image.load(muteImageGreyName).convert()
theMuteButton = UsefulClasses.MyClickableCircleButton(28,575,20,scrn,MuteButtonCallback)
 
# set the pygame window name
#pygame.display.set_caption('image')
 
# create a surface object, image is drawn on it.
image = pygame.image.load("enigma3.png")
bigImage = pygame.transform.scale(image, (X, Y))
 
#PYGAME LOOP
# creating a bool value which checks 
# if game is running
running = True
 
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

ringSetting = "AAA" #Same as user setting but backwards - B is like Z, etc.

rotor1Type = rotorNumbers[2]
rotor2Type = rotorNumbers[1]
rotor3Type = rotorNumbers[0]
reflectorType = "B"

r1 = Rotor(rotor1Type,userSetting[2],ringSetting[2])
r2 = Rotor(rotor2Type,userSetting[1],ringSetting[1])
r3 = Rotor(rotor3Type,userSetting[0],ringSetting[0])
ref = Reflector(reflectorType)

myPlugBoard = PlugBoard()
#myPlugBoard.AddPlugPair(["A","W"])
#myPlugBoard.AddPlugPair(["H","Z"])
#myPlugBoard.AddPlugPair(["B","L"])
#myPlugBoard.AddPlugPair(["R","F"])

theEnigma = Enigma(r1,r2,r3,ref,myPlugBoard)

while running:
 
  for event in pygame.event.get():
    
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    if event.type == pygame.MOUSEMOTION:
      UpdateCursor() 
    if event.type == pygame.MOUSEBUTTONUP:  
      CheckForUserSettingsChange()
    
    #TODO - move this to a function and do every key!
    #Can this be done better with keys = pygame.key.get_pressed() <- list???
    if event.type == pygame.KEYDOWN:
        LightUpAKey(event.key)
        
    if event.type == pygame.KEYUP:
        keysToHightLight = []
          
  # Using blit to copy content from one surface to other
  scrn.blit(bigImage, (0, 0))
  
  DrawRotorText()
  DrawRotorNumbers()
  HighlightKeys(scrn)
  DrawPlainAndCypherText(scrn)

  theMuteButton.DrawSelf()

  pygame.display.flip()
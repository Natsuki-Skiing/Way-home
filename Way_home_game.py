import os

from clear import clear
hasReadChar = False 
hasSound = False
import sys
noMusic = ("--noMusic"  in sys.argv)
#DEBUG 

try:
    import readchar
    hasReadChar = True
    
except:
    pass
if (not noMusic):
    try:
        from soundController import *
        hasSound = True
    except:
        pass
else:
    hasSound = True
if(not hasSound or not hasReadChar):
    clear()
    print("Way Home")
    print("===========")
    print("There are missing requirements:")
    if(not hasReadChar):
        print("readchar")
    if(not hasSound):
        print("playSound3")
    print("Would you like me to install them for you? (Module requirements will also be installed) Y/N")
    choice = input(">").lower()
    
    if(choice == "y"):
        if(not hasReadChar):
            os.system("pip3 install readchar")
            import readchar
        if(not hasSound and not noMusic):
                os.system("pip3 install playsound3")
                from soundController import *
    else:
        print("Please install the required modules")
        exit()
from healthBar import healthBar
from creature import creature
from window import Window
from item import * 
from player import player
from mainUIWins import *
import platform
import time
import random
import pickle

from opp import opp
from battleSystem import battleSystem
from clock import clock
from names import names
import copy
from ascii import *
from town import *
from dungeon import *
from creatureManager import *
from mapClasses import *





worldPickables = [fish("Apple",1,"A healthy snack",2,4),fish("Fist of blackberries",2,"A small pile of blackberries",2,4),fish("Money",0,"",0,0),fish("Thornnut",1,"A decent sized groved hard shell nut. Prized by Dwarvern miners and Men for its energy and resitance to spoiling",2,50),fish("Foul Root",3,"A black hard root. It is used by the penentry to heal the size as they can scarcely afford better medicine. It's name is deserved",10,10)]
worldPickablesWeight = [5,5,1,4,3]

worldFish = [fish("ᛋᚪᛗ ᚻᛁᛞᛖ",7,"Large ugly fish plentyful in the cold lands of the North East.People have to desire to name it in the common tounge, they only care for it's good taste",25,8),
             fish("Forgorth's Delight",4,"As he sat on the Starsteel Throne, Forgorth commanded great quantities of this fish. The original name is forgotten",10,3),
             fish("Narflyn",1,"Small silver fish with a bright emarld tint. Eaten by many.Some people of the northern mountains have gods in it's image, as it alone carried them the the cold of dark times",6,8),
             fish("Therkain",2,"Only thing faster than this fish is the speed at which it is eaten.",6,8)]

        
        
   

def clear():
    if(platform.system()=="Windows"):
        os.system('cls')
    else:
        os.system('clear')
    

        
class mainMenu():
    def __init__(self):
        self.saves = False 
        
        if(len(os.listdir("saves"))>0):
            self.saves = True
    def main(self):
        done = False
        Ascii = ascii()
        Ascii.draw((0,0),"Way","R")
        Ascii.draw((0,8),"Home","Rand")
        while(not done):
            
            
            print("")
            print("(S)tart")
            if(self.saves):
                print("(L)oad")
            print("(H)elp")
            print("(A)bout")
            
            choice = str(input(">")).lower()
            
            match(choice):
                case 's':
                    return(None)
                case 'l':
                    name = self.loadMenu()
                    if(name != None):
                        return(name)
                case "a":
                    self.about()
                case "h":
                    self.help()
                case "help":
                    self.help()
    def help(self):
        print("Help")
        print("=====")
        print("")
        print("Menus")
        print("-----")
        print('''There are a lot of menus in this game. Most of them look like this:
              
              (O)ption
              (B)ack
              >o
              
To select an item in the menu type the letter/s in brackets(not case sensative) , not the full word 
except help on the main menu.In above example im selecting the first option''')
        print("\n")
        print("Controls")
        print("=========")
        print("Arrow Keys = movement")
        print("E          = Show Eqipt Items")
        print("Q          = Show Inventory")
        print("P          = Pause Menu")
        print("S          = Player Status")
        
        input("Press a key to return")
    def about(self):
        print("Help")
        print("=====")
        print("")
        print('''I started programming this game on the way home from my second term in my second year at lancaster univerity.
Most of the main data structures and concepts where written during the two hour Journey. Way Home is a simple game 
but it was started as just a bit of entertaiment for a car journy so what do you expect.
Thanks for checking it out-
            William.J.Orbine''')
        input("Press a key to return")
    def loadMenu(self):
        if(not self.saves):
            return
        else:
            
            files = os.listdir("saves")
            tempList = list()
            for file in files:
                file =file.split('.')[0]
                if file not in tempList and file !="":
                    
                    tempList.append(file)
                
            files = tempList
            
            done = False 
            while(not done):
                clear()
                print("Select Character to load")
                print("")
                count = 0
                for name in files:
                    print(str(count),": ",str(name))
                    count +=1 
                print("(B)ack")
                choice = str(input(">")).lower()
                if(choice == "b"):
                    return 
                else:
                    try :
                        
                        choice = int(choice)
                    except:
                        choice = -1
                    if(choice < 0 or choice > count):
                        print("Invalid number, pick between 0 & ",count)
                        time.sleep(2)
                    else:
                        return(files[choice])
            
class pauseMenu():
    def main(self,autoRun):
        
        done = False
        while(not done):
            clear()
            print("Pause Menu")
            print("===========")
            print("")
            print("(S)ave")
            print("(C)ontrols")
            print("(T)oggle auto run in overworld : ",str(autoRun))
            print("(B)ack")
            print("(Q)uit")
            choice = str(input(">")).lower()
            if choice == 's':
                return(1)
            if choice =='c':
                print("Controls")
                print("=========")
                print("Arrow Keys = movement")
                print("E          = Show Eqipt Items")
                print("Q          = Show Inventory")
                print("P          = Pause Menu")
                print("S          = Player Status")
                
                input("Press a key to return")
            # Not working i dont know why 
            if choice == "t":
                autoRun = not autoRun
            if choice == "q":
                sys.exit()
            if choice == "b":
                return(0)

class bookReader:
    def __init__(self,Book:book):
        self.Book = Book
        self.pages = dict() 
        size = os.get_terminal_size()
        self.width = 100
        self.height = 10
        self.currentPage = self.Book.page
        self.pageSize = self.height * self.width
        # testSize = int()
        # with open(self.Book.path, 'r', encoding='utf-8') as f:
        #     content = f.read()
        #     testSize = int(len(content)/self.pageSize)
        self.numberOfPage = int(os.path.getsize(self.Book.path)/self.pageSize)
        pass
    def loadPage(self,pageNumber:int):
        if pageNumber in self.pages.keys():
            return(self.pages[pageNumber])
        else:
            try:
                
                file = open(self.Book.path,'r')
                file.seek(pageNumber * self.pageSize)
                self.pages[pageNumber] = file.read(self.pageSize)
                return(self.pages[pageNumber])
                
            except:
                pass
    def changePage(self,dir:bool):
        #False go back 
        if(dir):
            if(self.currentPage != self.numberOfPage):
                self.currentPage +=1 
        else:
            if(self.currentPage > 0):
                self.currentPage -=1 
    def main(self):
        running = True
        while(running):
            clear()
            print("===== |",self.Book.name,"| Page ",str(self.currentPage)," / ",str(self.numberOfPage),"======")
            print(self.loadPage(self.currentPage)+"\n")
            print("===========================")
            print("Change Pages: <- -> ,(G)oto Page, (E)xit")
            
            match(readchar.readkey()):
                case 'e':
                    print("Would oyu like to remember the current page? (Y)es / (N)o")
                    choice = input(">").lower()
                    if(choice == "y"):
                        self.Book.page = self.currentPage 

                    running = False 
                case readchar.key.LEFT:
                    self.changePage(False)
                case readchar.key.RIGHT:
                    self.changePage(True)
                case 'g':
                    print("Which page?")
                    choice = input(">")
                    try:
                        choice = int(choice)
                    except:
                        choice = -1
                        
                    if(choice < 0 or choice > self.numberOfPage):
                        print("Invalid page number.Max page is ",self.numberOfPage)
                        time.sleep(2)
                    else:
                        self.currentPage = choice
                    
           
        pass               



class WayHome:
    def __init__(self,x:int,y:int):
        clear()
        self.Menu = mainMenu()
        
        if(not noMusic):
            self.MusicPlayer = musicPlayer("music/")
            self.MusicPlayer.start()
        load = self.Menu.main()
        self.World = None 
        self.Player = None
        self.autoRun = False
        self.pauseMenu = pauseMenu()
        
        if(load):
            #There is already as saved game player wants to load
            if(not self.loadGame(load)):
                print("Error Loading game from File")
                
            
        else:
            clear()
            print("New game")
            print("Input a name,leave blank and I'll pick one for you")
            name = input(">")
            if name == '' or name =='.':
                
                name = random.choice(names)
            clear()
            self.Player = player(name)
            self.World = world(x,y)
            self.GClock = clock()
            self.statWin = statWin((2+x),0,30,y-9,name,self.World.currentMap,self.Player,self.GClock.GetFullTime())
            self.intWin = interWin(x+2,(self.statWin.h+2),self.statWin.w,(y-self.statWin.h-2),"Actions")
            self.logWin = logWin(0,y+2,x+self.statWin.w+2,7,"Events Log")
            #used for town and dungeon chance generation
            self.sinceTown = 0
            self.sinceDun =0
            #Init player inventory play stuff
            self.Player.items.append(weapon("Kitchen Fork",10,1,1,"A kitchen fork, not a fancy one. Is made from steel. Handle has some rust on it, probbaly reduces the value"))
            self.Player.items.append(armour("Raggy top",1,3,"A raggy smelly top. Has more holes than not."))
            self.Player.items.append(fish("Apple",1,"A healthy snack",2,4))
            self.Player.equiptItems["weapon"] = self.Player.items[0]
            self.Player.equiptItems["armour"] = self.Player.items[1]
            self.itemManager = itemManager("items")
            self.CrManOver = creatureManager("Creatures","OverWorld")
            self.CrManDun = creatureManager("Creatures","Dungeon")
            self.saveGame()
            #start a new game
            pass
        self.mainLoop()
    def loadGame(self,name:str)->bool:
        success = False 
        try:
        # Load the World object from the file
            with open("saves/" + name + '.world', 'rb') as file:
                self.World = pickle.load(file)
            
            # Load the Player object from the file
            with open("saves/" + name + '.player', 'rb') as file:
                self.Player = pickle.load(file)
            
            success = True
        except Exception as e:
            print("Error loading files:", e)
            pass
        
        return(success)
    def calcDist(self)->int:
        # Higer level further from start
        # Rounding up always cuz i want to 
        dist = abs(self.World.currentMap[0]) + abs(self.World.currentMap[1])
        if dist <1:
            dist = 1
        return(dist)
    def battle(self):
        #TODO
        # Probbaly need to come up with a better system
        if(not self.autoRun):
            if(random.randint(0,8) ==1):
                
                
                battleSystem(self.Player,self.CrManOver,self.calcDist())
                clear()
                self.redrawAll()
    def saveGame(self):
        with open(("saves/"+self.Player.name+'.player'), 'wb') as file:
            pickle.dump(self.Player, file)
        with open(("saves/"+self.Player.name+'.world'), 'wb') as file:
            pickle.dump(self.World, file)
    def mainLoop(self):
        #DEBUG
        #self.Player.items.append(fishingRod("Test Rod",-1,"Testing"))
        #END
        self.World.maps[(0,0)] = map(self.World.mapX,self.World.mapY,True,True,town= town(self.itemManager),Dungeon=self.makeDungeon())
        self.Player.x ,self.Player.y = (0,0)
        self.World.placePlayer(self.Player.x, self.Player.y)
        self.World.drawCurrentMap()
        running = True
        
        # Setup for terminal control
        print("\033[?25l")  # Hide cursor
        clockCount = 1
        lastDay = self.GClock.day
        nextToWater = False
        while(running):
            key = readchar.readkey()
            update = 0
            
            
            match(key):
                case readchar.key.LEFT:
                    update = self.movePlayer(9)
                    self.battle()
                    
                case readchar.key.RIGHT:
                    update = self.movePlayer(3)
                    self.battle()
                case readchar.key.UP:
                    update = self.movePlayer(12)
                    self.battle()
                case readchar.key.DOWN:
                    update = self.movePlayer(6)
                    self.battle()
                case 'q':
                    self.Player.showInventoryMenu()
                    update = 2
                    
                case 's':
                    self.Player.showStatus()
                    update = 2
                    
                case 'e':
                    self.Player.showEquipItems()
                    update = 2
                    
                case 'p':
                    choice = self.pauseMenu.main(self.autoRun)
                    update = 2
                    
                    if choice == 1:
                        # Overwritting the save 
                        self.saveGame()
                        print("Game Saved!")
                        time.sleep(1.5)
                case 't':
                    if(self.World.tileSwap == townTile):
                        update = 2 
                        self.World.maps[self.World.currentMap].town.townMainLoop(self.GClock.GetFullTime(),self.Player)        
                case 'f':
                    # Will be able to fish
                    rod = None
                    if(nextToWater):
                        if("rod" in self.Player.equiptItems.keys()):
                            rod = self.Player.equiptItems["rod"]
                        else:
                            for item in self.Player.items:
                                if type(item) == fishingRod:
                                    rod = item 
                        
                        if (rod != None):
                            # Fishing stuff 
                            pass
                        else:
                            
                            self.logWin.addMsg("Need to equip a fishing rod")
                            update = 1
                case 'd':
                    if(self.World.tileSwap == dungeonTile and self.World.maps[self.World.currentMap].hasDungeon):
                        x,y = self.Player.x ,self.Player.y
                        update = 2 
                        self.World.maps[self.World.currentMap].Dungeon.mainLoop(self.GClock)
                        self.Player.x , self.Player.y = x ,y         
                case 'g':
                    try:
                    # Get items from food trees
                        if(type(self.World.maps[self.World.currentMap].tiles[(self.Player.x, self.Player.y)]) == type(foodTree)):
                            self.World.tileSwap = shrub
                            # setting the time it was last picked
                            self.World.maps[self.World.currentMap].shrubTimerDict[(self.Player.x,self.Player.y)] = [self.GClock.day,self.World.maps[self.World.currentMap].shrubTimerDict[(self.Player.x,self.Player.y)]][1]
                            picked = random.choices(worldPickables, weights=worldPickablesWeight, k=1)[0]
                            
                            if(picked.name == "Money"):
                                self.Player.gold += 3
                                self.logWin.addMsg(self.Player.name + "found £3!")
                            else:
                                self.Player.items.append(picked)
                                
                                self.logWin.addMsg(self.Player.name + " picked a " + picked.name)
                            
                            
                            update = 1
                    except: 
                        pass
                case 'q':
                    running = False
                    
                #Debug button 
                case 'd':
                    #DEBUG 
                    self.Player.hp = self.Player.hp /2 
                    self.statWin.update()
                    
                    
            # Check if player is next to water for fishing option
            temp = nextToWater
            nextToWater = self.World.maps[self.World.currentMap].nextToWater(self.Player.x, self.Player.y)
            
            # Clock stuff kinda expensive i guess 
            # I  dont want to run it every iteration so runs every 2 ig
            if(clockCount == 1):
                self.GClock.update() 
                newTime = self.GClock.GetFullTime()
                self.statWin.updateSetTime(newTime) 
                difDay = lastDay - newTime[0]
                if(difDay >0):
                    rottenItems = self.Player.rot(newTime)
                    if len(rottenItems) > 1:
                        for item in rottenItems:
                            self.logWin.addMsg((item+" has rotted")) 
                    lastDay = newTime[0]
                
                clockCount = 0 
            else :
                clockCount +=1
            if(temp != nextToWater):
                update = 2
            
            if(update != 0):
                self.World.placePlayer(self.Player.x, self.Player.y)
                
                if(update == 2):
                    # Full redraw needed (after menu, etc.)
                    clear()
                    
                    self.statWin.draw()
                    self.intWin.draw()
                    self.logWin.draw()
                    
                    self.statWin.update()
                    self.logWin.update()
                    self.intWin.update() 
                    self.World.Window.draw()
                    self.World.drawCurrentMap()
                else:
                    # Only update player position
                    self.World.drawOnlyPlayer((self.Player.x, self.Player.y), self.Player.prevLoc)
                
                
                # Show context-sensitive actions
                if self.World.tileSwap == dungeonTile:
                    self.intWin.addAction("(D)ungeon")
                else:
                    dunUpdate = self.intWin.removeAction("(D)ungeon")
                if self.World.tileSwap == foodTree:
                    self.intWin.addAction("(G)ather")
                    
                    
                else:
        
                   gatherUpdate = self.intWin.removeAction("(G)ather") 
                if self.World.tileSwap == townTile:
                    self.intWin.addAction("(T)own - "+self.World.maps[self.World.currentMap].town.name)
                else:
                    townUpdate = self.intWin.removeAction("(T)own")
                if nextToWater and temp != nextToWater:
                    self.intWin.addAction("(F)ish")
                else:
                    fishUpdate = self.intWin.removeAction("(F)ish")
                
                if gatherUpdate or fishUpdate or townUpdate or dunUpdate:
                    self.intWin.update()
            #Might no longer need this i dunno 
            #time.sleep(0.1)
    
        # Cleanup
        print("\033[?25h")  # Show cursor again
        
    def movePlayer(self,dir:int)->int:
        self.Player.prevLoc = (self.Player.x,self.Player.y)
        newCood = [self.Player.x,self.Player.y]
        match(dir):
            case 12:
                newCood[1] -= 1
                pass
            case 3:
                newCood[0] += 1
                pass 
            case 6:
                newCood[1] += 1
                pass
            case 9:
                newCood[0] -= 1
                pass 
        if(self.World.inBounds(newCood[0],newCood[1])):
            if(self.World.canWalk(newCood[0],newCood[1])):
                self.Player.x = newCood[0]
                self.Player.y = newCood[1]
                return 1 
            return 0
           
        else:
            #Generating a new world chunk
            match(dir):
                case 12:
                    newCood[1] = self.World.rY
                    self.Player.wY -=1
                    pass
                case 3:
                    newCood[0] = 0
                    self.Player.wX +=1
                    pass 
                case 6:
                    newCood[1] = 0
                    self.Player.wY +=1
                    pass
                case 9:
                    newCood[0] = self.World.rX
                    self.Player.wX -=1
                    pass
            #Need to replace the p in the map with the swap tile
            replaceKey = (self.Player.x ,self.Player.y)
            self.World.maps[self.World.currentMap].tiles[replaceKey] = self.World.tileSwap
            self.World.currentMap = (self.Player.wX ,self.Player.wY)
            self.Player.x = newCood[0]
            self.Player.y = newCood[1]
            #Still need to develope more world generation
            
            if self.World.currentMap not in self.World.maps.keys():#For it the ckunk already exists
                # Adding a town and or a dungeon to our new map
                hasDun = False 
                hasTown = False
                #Town
                if (random.randint(0,(7-self.sinceTown))) == 0:
                    hasTown = True
                    self.sinceTown =0
                else:
                    hasTown = False
                    self.sinceTown +=1 
                
                #Dungeon     
                if(random.randint(0,(4-self.sinceDun))) == 0:
                    hasDun = True 
                    self.sinceTown = 0 
                else:
                    hasDun = False 
                    self.sinceDun +=1
                
                
                if(hasTown and hasDun):
                    self.World.maps[self.World.currentMap] =self.World.genMap(self.Player.wX,self.Player.wY,True,True,town(self.itemManager),dungeon(self.Player,self.Player.wX,self.Player.wY,125,100,50,self.itemManager,self.CrManDun,self.calcDist()))
                elif(hasTown):
                    self.World.maps[self.World.currentMap] = self.World.genMap(self.Player.wX,self.Player.wY,True,False,Town=town(self.itemManager))
                elif(hasDun):
                    self.World.maps[self.World.currentMap] = self.World.genMap(self.Player.wX,self.Player.wY,False,True,Dungeon= self.makeDungeon())
                else:
                    self.World.maps[self.World.currentMap] = self.World.genMap(self.Player.wX,self.Player.wY,False,False)
                
            else:
                # What is the purpuse of this section of code?
                #Submit answers to willjames1109@outlook.com
                if len(self.World.maps[self.World.currentMap].shrubTimerDict) > 0:
                    
                    for key in self.World.maps[self.World.currentMap].shrubTimerDict.keys():
                        value = self.World.maps[self.World.currentMap].shrubTimerDict[key]
                        if (self.World.maps[self.World.currentMap].shrubTimerDict[key][0] != -1):
                            if(self.GClock.day - value[0] >= value[1]): 
                                value[0] = -1 
                                self.World.maps[self.World.currentMap].shrubTimerDict[key] = value 
                                self.World.maps[self.World.currentMap].tiles[(self.Player.x,self.Player.y)] = foodTree
            self.statWin.updateMap(self.World.currentMap)
            return(2)
    def makeDungeon(self)->dungeon:
        return(dungeon(self.Player,self.World.mapX,self.World.mapY,125,100,50,self.itemManager,self.CrManDun,self.calcDist()))
    def redrawAll(self):
        self.statWin.draw()
        self.intWin.draw()
        self.logWin.draw()
        
        self.statWin.update()
        self.logWin.update()
        self.intWin.update() 
        self.World.Window.draw()
        self.World.drawCurrentMap()        
    def levelMult(self)->float:
        current = self.World.currentMap 
        dist = abs(current[0]) + abs(current[1])  
        return(float(dist/100))    
# hobbit = book("hobbit",100,"Once was there and back again")
# reader = bookReader(hobbit)
#reader.main()        
testMain = WayHome(40,30)


     



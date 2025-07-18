from creature import creature 
from clear import clear
import time 
from window import Window
from item import *
from printAt import *
import sys 
from bookReader import bookReader
from selectMenu import *
class player(creature):
    def __init__(self,name:str):
        #Local 
        self.x = int()
        self.y = int()
        #World / current tile
        super().__init__(name,1,25)
        self.name = name
        self.wX = 0
        self.wY = 0
        #A campsite placed by player 
        self.respawnCamp = None
        self.gold = 10
        self.defense = 3
        self.attack = 5
        self.xp = 0
        self.xpToNextLevel = 50
        self.ap = 10
        self.prevLoc = (0,0)
        self.equiptItems = {"helmet":None , "armour":None,"weapon":None,"rod":None}
        self.items = list()
        self.lastRotTime = [0,0,0]
        self.creaturesKilled = dict()
        self.totalXp = 0
        self.swordFrags = 0
        self.madeSword = False
        self.numberRespawns = 0
    def addHp(self,amount:int):
        self.hp += amount 
        if(self.hp >self.maxHp):
            self.hp = self.maxHp
    def rot(self,time)->list[str]:
            outList = []
            difference = time[0] - self.lastRotTime[0]
            if difference > 0:
                for item in self.items:
                    if type(item) == fish:
                        item.dayTillRot -= difference 
                        if item.dayTillRot <=0:
                            self.items.append(item(("Rotten "+item.name),0,"This item is rotten. You should be careful not to let items spoile. Some items can be preserved.")) 
                            outList.append(item.name)
                            self.items.remove(item) 
            return(outList)
    def addXp(self,xp:int):
        running = True 
        self.totalXp += xp
        while running:
            
            if(xp + self.xp >= self.xpToNextLevel):
                self.xp -= self.xpToNextLevel
                self.xpToNextLevel = int(self.xpToNextLevel * 1.5)
                self.addHp(10)
                self.levelUp()
            else:
                self.xp += xp
                running = False
    def levelUp(self):
        clear()
        
        desDict = {"hp":("Player's health stat currently at "+str(self.maxHp)),"def":("Base defense stat which armour adds to. Currently "+str(self.defense)),"atk":("Attack ability. Weapons add to this stat. At "+str(self.attack))}
        print("Level up ")
        print("Select an attribute to increase")
        print("")
        print("(H)p:")
        print(("     Player's health stat,by 2, currently at "+str(self.maxHp)))
        print("")
        print("(D)efense:")
        print(("     Base defense stat which armour adds to. Currently "+str(self.defense)))
        print("")
        print("(A)ttack:")
        print(("     Attack ability. Weapons add to this stat. At "+str(self.attack))) 
        running = True 
        while running:
            selected = input(">").lower()
            match(selected):
                case "h":
                    self.hp+=2
                    print("Levelled up hp")
                    running = False
                case "d":
                    self.defense+=1
                    print("Levelled up defense") 
                    running = False
                case "a":
                    self.attack+=1
                    print("Levelled up attack")
                    running = False
        self.level +=1
        
                                                
    
    def showInventoryMenu(self):
        numberOfItems = len(self.items)
        itemDict = dict()
        counter = 0
        def printList(itemDict):
            for key in itemDict.keys():
                item = itemDict[key]
                if item in self.equiptItems.values() and item != None:
                    print(f"{key} : E {item.name}")
                else:
                    print(f"{key} :   {item.name}")
            print("--------")
            print("(B)ack")
        def genDict(itemDict,counter):
            counter = 0
            itemDict.clear()
            for item in self.items:
                itemDict[counter] = item
                counter +=1
        genDict(itemDict,counter)
        done = False
        while(not done ):
            if(numberOfItems != len(self.items)):
                numberOfItems = len(self.items)
                genDict(itemDict,counter)
            clear()
            print("Inventory")
            printList(itemDict=itemDict)
            choice = str(input(">")).lower()
            if(choice == "b"):
                done = True 
            else:
                try:
                    choice = int(choice)
                except:
                    choice = -1
                if(choice < 0 or choice > len(itemDict.keys())-1):
                    print("Invalid selection")
                    print("Number between 0 -",counter)
                    time.sleep(2) 
                else:
                    clear()
                    self.selectedItem(itemDict[choice])
                
    def selectedItem(self,Item:item):
        if(not Item in self.items):
                return
        done = False
        while(not done):
            
            clear()
            offset = 2
            statsWin = Window(0,0,30,20,"Stats")
            desWin = Window(statsWin.w+2,0,45,statsWin.h,"Description")
            statsWin.draw_text(0,0,"Name:   "+Item.name)
            if type(Item) == weapon:
                    statsWin.draw_text(0,offset,("Damage: "+str(Item.damage)))
                    offset +=2
            elif type(Item) == armour or type(Item) == helmet:
                    statsWin.draw_text(0,offset,("Protection: "+str(Item.protection)))
                    offset +=2
            elif type(Item) == fish or type(Item) == food:
                statsWin.draw_text(0,offset,("Hp: "+str(Item.hp)))
                offset +=2
            if type(Item) == weapon or type(Item) == fishingRod:
                statsWin.draw_text(0,offset,("Condition: "+str(Item.condition)+" / "+str(Item.maxCondition)))
                offset +=2
            statsWin.draw_text(0,offset,("Value:   £" +str(Item.value)))
            offset +=2 
            
            
            
            linesList = [Item.description[i : i + desWin.w] for i in range(0, len(Item.description), desWin.w)]
            counter = 0 
            for line in linesList:
                desWin.draw_text(0,counter,line)
                counter +=1
            
            # print("Selected:",Item.name)
            # print("=================")
            
                
                
            offset = statsWin.h+3
            printAt(0,offset,"What would you like to do?")
        

            offset+=1
            
            
            if (type(Item) in equipableItems and Item not in self.equiptItems.values()):
                printAt(0,offset,'(E)quip')
                
                offset+=1
            elif(type(Item) in equipableItems and Item  in self.equiptItems.values()):
                
                printAt(0,offset,"(U)nequip")
                offset+=1
            if(type(Item) == fish or type(Item) == food):
                
                printAt(0,offset,"(E)at")
                offset+=1
            
            if(type(Item) == book):
                
                printAt(0,offset,"(R)ead")
                offset+=1 
            
            printAt(0,offset,"(G)et rid of")
            offset+=1
            
            printAt(0,offset,"(B)ack \n")
            offset+=1
            
            choice = str(input(">")).lower()
            match(choice):
                case "e":
                    if(type(Item) in equipableItems and Item not in self.equiptItems.values()):
                        clear()
                        self.equipItem(Item)
                    elif(type(Item) == fish or type(Item) == food):
                        self.addHp(Item.hp)
                        self.items.remove(Item)
                        done = True
                    pass
                case "u":
                    if( Item  in self.equiptItems.values()):
                        clear()
                        self.unequipItem(Item)
                    
                case "g":
                    self.dropItem(Item)
                    pass
                case "b":
                    done = True
                case "r":
                    if(type(Item) == book):
                        Reader = bookReader(Item)
                        Reader.main()
    def dropItem(self,Item:item):
        done = False 
        while(not done):
            clear()
            print("Are you sure you want to drop ",Item.name,"?")
            print("It will be gone forever. (Y)es/(N)o")
            choice = str(input(">")).lower()
            itemType = str()
            if(itemType == weapon):
                itemType = "weapon" 
            elif (itemType == armour):
                itemType = "armour"
            else:
                itemType = "helmet"
            match(choice):
                case "y":
                    if(self.equiptItems[itemType] == Item):
                        self.dict[itemType] = None
                    elif Item in self.items:
                        self.items.remove(Item)
                    print("Got rid of ",Item.name)
                    time.sleep(1)
                    done = True
                        
                case "n":
                    return 
                case _:
                    print("Invalid selection")
                    print("Choose Y or N")
                    time.sleep(2)
    def equipItem(self,Item:item):
        itemType = type(Item)
        key = str()
        if(itemType == weapon):
            key = "weapon" 
        elif (itemType == armour):
            key = "armour"
        elif (itemType == fishingRod):
            key = "rod"
        else:
            key = "helmet"
            
        if(self.equiptItems[key] != None):
            print(self.equiptItems[key].name," already in ",key," slot")
            print("Swap ? (Y)es / (N)o")
            
            done = False 
            while(not done):
                choice = str(input(">")).lower()
                match(choice):
                    case "y":
                        self.equiptItems[key] = Item 
                        done = True
                    case "n":
                        return 
                    case _:
                        print("Invalid selection")
                        print("Choose Y or N")
                        time.sleep(2)
    
                    
        else:
            self.equiptItems[key] = Item 
        
        print("Equipped ", Item.name , "in " ,key," slot")
        time.sleep(1.5)
    def unequipItem(self,Item:item):
        if Item in self.equiptItems.values():
            if(type(Item)== weapon):
                self.equiptItems["weapon"] = None
            elif(type(Item)== helmet):
                    self.equiptItems["helmet"] = None
            elif(type(Item)== fishingRod):
                self.equiptItems["rod"] = None
            else:
                self.equiptItems["armour"] = None
                
                
    def showStatus(self):
        clear()
        print(self.name)
        statusMsg = str()
        print("---------------")
        if(self.hp > self.maxHp):
            statusMsg = "You should not have this amount of health, but you do and I can't do much about it"
        elif(self.hp == self.maxHp):
            statusMsg = "Hale as the Firstborn in Sring of Arda"
        elif(self.hp >= self.maxHp *0.85):
            statusMsg = "Stalwart and Unshaken"
        elif(self.hp >= self.maxHp *0.7):
            statusMsg = "Wounded, Yet Unbowed"
        elif(self.hp >= self.maxHp *0.50):
            statusMsg = "Bloodied and Battleworn"
        elif(self.hp >= self.maxHp *0.30):
            statusMsg = "Wounds slow the pace, and strength ebbs like twilight"
        elif(self.hp >= self.maxHp *0.15):
            statusMsg = "The edge of death is near, but hope is not yet lost"
        elif(self.hp > 0):
            statusMsg = "Fading into Shadow"
        print(statusMsg)
        print("")
        print("Hp: ",self.hp," / ",self.maxHp)
        print("Xp: ",self.xp," / ",self.xpToNextLevel)
        print("Total xp earned: ",self.totalXp)
        print("Current Level: ",str(self.level))
        print("")
        print("Atk: ",self.attack)
        print("Def: ",self.defense)
        print("")
        print("Gold: ",self.gold)
        print("Press a enter to return")
        input("")
        return()
    def calcScore(self)->int:
        score = 0 
        score += self.totalXp + self.level 
        noCreatures = 0
        for key in self.creaturesKilled.keys():
            noCreatures += self.creaturesKilled[key]
        score += noCreatures *10 
        score += self.gold 
        for item in self.items:
            score+= item.value 
        
        score += self.swordFrags * 1000 
        if self.madeSword:
            score += 5000
        score -= self.numberRespawns *120
        return(score)
    def hasCampFire(self)->bool:
        returnVal = False 
        for item in self.items:
            if item.name == "Campfire":
                returnVal = True 
                break 
        
        return(returnVal)
    def showEquipItems(self):
            clear()
            print("===",self.name,"'s equip items===")
            try:
                print("Helmet:  ",self.equiptItems["helmet"].name)
            except:
                print("Helmet:  ",self.equiptItems["helmet"])
                
            try:
                print("Armour:  ",self.equiptItems["armour"].name)
            except:
                print("Armour:  ",self.equiptItems["armour"])
                
            try:
                print("Weapon:  ",self.equiptItems["weapon"].name)
            except:
                print("Weapon:  ",self.equiptItems["weapon"])
                
            try:
                print("Rod:  ",self.equiptItems["rod"].name)
            except:
                print("Rod:  ",self.equiptItems["rod"])
            
        
            input("Press enter to return")
            return()   
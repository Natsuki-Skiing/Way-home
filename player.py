from creature import creature 
from clear import clear
import time 
from window import Window
from item import *
import sys 
from bookReader import bookReader
from selectMenu import *
class player(creature):
    def __init__(self,name:str):
        #Local 
        self.x = int()
        self.y = int()
        #World / current tile
        super().__init__(name,1,50)
        self.name = name
        self.wX = 0
        self.wY = 0
        
        self.gold = 10
        self.defense = 3
        self.attack = 5
        self.xp = 0
        self.xpToNextLevel = 50
        self.ap = 10
        self.prevLoc = (0,0)
        self.equiptItems = {"helmet":None , "armour":None,"weapon":None}
        self.items = list()
        self.lastRotTime = [0,0,0]
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
        while running:
            
            if(xp + self.xp >= self.xpToNextLevel):
                self.xp -= self.xpToNextLevel
                self.xpToNextLevel = int(self.xpToNextLevel * 1.5)
                self.levelUp()
            else:
                self.xp += xp
                running = False
    def levelUp(self):
        clear()
        desDict = {"hp":("Player's health stat currently at "+str(self.maxHp)),"def":("Base defense stat which armour adds to. Currently "+str(self.defense)),"atk":("Attack ability. Weapons add to this stat. At "+str(self.attack))}
        print("Level up ")
        print("(H)p:")
        print(("     Player's health stat currently at "+str(self.maxHp)))
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
                    self.hp+=1
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
        
                                                
    
    def showInventoryMenu(self):
        numberOfItems = len(self.items)
        itemDict = dict()
        counter = 0
        def printList(itemDict):
            for key in itemDict.keys():
                item = itemDict[key]
                print(f"{key} : {item.name}")
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
        clear()
        offset = 2
        statsWin = Window(0,0,30,20,"Stats")
        desWin = Window(statsWin.w+2,0,45,statsWin.h,"Description")
        statsWin.draw_text(0,0,"Name:   "+Item.name)
        if type(Item) == weapon:
                statsWin.draw_text(0,offset,("Damage: "+str(Item.damage)))
                offset +=2
        elif type(Item) == armour:
                statsWin.draw_text(0,offset,("Protection: "+str(Item.protection)))
                offset +=2
        elif type(Item) == fish:
            statsWin.draw_text(0,offset,("Hp: "+str(Item.hp)))
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
        sys.stdout.write(f"\033[{offset};{0}H{"What would you like to do?"}")

        offset+=1
        
        
        if (type(Item) in equipableItems):
            sys.stdout.write(f"\033[{offset};{0}H{"(E)quip"}")
            offset+=1
        if(type(Item) == fish):
            sys.stdout.write(f"\033[{offset};{0}H{"(E)at"}")
            offset+=1
           
        if(type(Item) == book):
            sys.stdout.write(f"\033[{offset};{0}H{"(R)ead"}")
            offset+=1 
        sys.stdout.write(f"\033[{offset};{0}H{"(G)et rid of"}")
        offset+=1
        sys.stdout.write(f"\033[{offset};{0}H{"(B)ack \n"}")
        offset+=1
        while(not done):
            choice = str(input(">")).lower()
            match(choice):
                case "e":
                    if(type(Item) in equipableItems):
                        clear()
                        self.equipItem(Item)
                    elif(type(Item) == fish):
                        self.addHp(Item.hp)
                        self.items.remove(Item)
                        done = True
                    pass
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
                        self.dict[type(Item)] = None
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
        print("")
        print("Atk: ",self.attack)
        print("Def: ",self.defense)
        print("Press a enter to return")
        input("")
        return()
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
            
        
            input("Press space to return")
            return()   
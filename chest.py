from itemManager import * 
from items import *
from window import * 
import random
from printAt import printAt

from clear import clear
class chest:
    def __init__(self,playerLevel:int,ItemManager:itemManager):
        
        self.playerLevel = playerLevel
        self.items = self.generateItems(ItemManager) 
        clear()
        self.itemsWin = Window(0,0,66,10,"Chest")
       
        self.mainLoop()

    def mainLoop(self):
        self.takenItems = []
        running = True 
        while running:
            clear()  # Clear the entire screen at the start of each loop
            
            # Redraw the window
            self.itemsWin.draw()
            
            self.itemsWin.draw_text(0,0," # | Name                       | Val | Def | Dam | Cnd | Hp | Rot")
            self.itemsWin.draw_text(0,1,"==================================================================")
            counter = 0 
            stringList = []
            for item in self.items:
                stringList.append(self.genItemString(item,counter))
                counter +=1 
            self.itemsWin.row_draw(stringList,2)
            
            # Print instructions below the window
            printAt(self.itemsWin.h+3,0,"Number to take item. A for all. E for exit")
            choice = input(">").lower()
            
            match(choice):
                case "e":
                    running = False 
                case "a":
                    # Take all items
                    self.takenItems.extend(self.items)
                    self.items.clear()
                    running =False
                case _:
                    try:
                        choice = int(choice)
                        if(choice >=0 and choice <= len(self.items)-1):
                            self.takenItems.append(self.items[choice])
                            del self.items[choice] 
                            
                    except:
                        pass
            
        
        
    def generateItems(self,ItemMan:itemManager) -> list:
        outList = []
        totalNoItems = random.randint(1,6) 
        typeDict = self.segNumber(totalNoItems,list(ItemMan.AllItems.keys()))
        for key in typeDict.keys():
            for _ in range(typeDict[key]):
                outList.append(ItemMan.getItem(key,self.classFromLevel(self.playerLevel+1),random.randint(max(self.playerLevel-2,1),self.playerLevel+3)))
        return(outList)
        
    def genItemString(self, item, number: int) -> str:
        outComps = [str(number), item.name, "", "", "", "", "", ""]
        iType = type(item)
        if iType == helmet or iType == armour:
            outComps[3] = str(item.protection)
        if iType == weapon:
            outComps[4] = str(item.damage)
        if iType == fish:
            outComps[5] = str(item.hp)
            outComps[6] = str(item.dayTillRot)
        outComps[2] = str(item.value)

        return " {:>1} | {:<25}  | {:>3} | {:>3} | {:>3} | {:>3} | {:>2} | {:>3}".format(*outComps)

        
    def classFromLevel(self, playerLevel: int) -> int:
        if playerLevel < 5:
            return random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        elif playerLevel < 15:
            return random.choices([2, 3, 4, 5], weights=[40, 30, 20, 10])[0]
        elif playerLevel < 30:
            return random.choices([3, 4, 5, 6, 7], weights=[25, 25, 20, 15, 15])[0]
        elif playerLevel < 50:
            return random.choices([5, 6, 7, 8], weights=[20, 30, 30, 20])[0]
        else:
            return random.choices([7, 8, 9, 10], weights=[10, 30, 30, 30])[0]
            
    def segNumber(self,total:int,typeList:list):
        noSeg = len(typeList)
        cuts = sorted([random.randint(1, max(total - 1,1)) for _ in range(noSeg - 1)])
    
        outDict = dict()
        divisions = []
        prevCut = 0
        for cut in cuts:
            divisions.append(cut - prevCut)
            prevCut = cut
        divisions.append(total - prevCut) 
        
        
        for index in range(noSeg):
            outDict[typeList[index]] = divisions[index]
        return(outDict)



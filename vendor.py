from window import Window 
from item import * 
from names import names
import random
from itemManager import *
from names import *
class vendor:
    def __init__(self,level:int,itemManager:itemManager):
        self.name = random.choice(names) 
       
        self.itemManager = itemManager
        self.items = list()
        self.name = random.choice(names)
    def segNumber(self,total:int,typeList:list):
        noSeg = len(typeList)
        cuts = sorted([random.randint(1, total - 1) for _ in range(noSeg - 1)])
    
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
    
    def generateInventory(self,numberOfItems:int,types:list,playerLevel:int):
        self.items = []
        itemLevelRange = (playerLevel-5,playerLevel+5)
        splitDict = dict()
        if len(types) > 1:
            splitDict = self.segNumber(numberOfItems,types)
        else:
            splitDict[types[0]] = numberOfItems 
        
        # Actually getting the items now 
        for key, value in splitDict.items():
            
           
            i = 0
            sinceLastItem = 0
            while i < value:
                # Don't want the shop keepers to have items worth nothing 
                try:
                    #DEBUG
                    #Trying just random from all item classes 
                    #tempItem = self.itemManager.getItem(key,self.classFromLevel(playerLevel),random.randint(itemLevelRange[0],itemLevelRange[1]))
                    
                    tempItem = self.itemManager.getItem(key,random.randint(1,10),random.randint(itemLevelRange[0],itemLevelRange[1]))
                    if(tempItem.value >0):
                        self.items.append(tempItem)
                        i +=1
                    else:
                        sinceLastItem +=1
                except RuntimeError as e :
                    print(e)
                    sinceLastItem +=1
                    pass
                
                if(sinceLastItem ==10):
                    i +=1 
                    sinceLastItem = 0
                
        
class blackSmith(vendor):
    def __init__(self, level:int,itemManager:itemManager):
        super().__init__(level,itemManager)
        self.items = self.generateInventory(level)
    def generateInventory(self,playerLevel:int):#DEBUG ["weapon","helmet","armour"]
        super().generateInventory(random.randint(12,20),["weapon","helmet","armour"],playerLevel) 
class grocer(vendor):
    def __init__(self, level:int,itemManager:itemManager):
        super().__init__(level,itemManager)
        self.items = self.generateInventory(level)
    def generateInventory(self,playerLevel:int):
        super().generateInventory(random.randint(15,25),["food","fish"],playerLevel)
        
class hunts(vendor):
    def __init__(self, level, itemManager):
        super().__init__(level, itemManager)
    def generateInventory(self,  playerLevel):
        super().generateInventory(random.randint(12,25),["fishingRod","campfire","wood"],playerLevel)
from item import * 
from selectMenu import arrowMenu 
from window import Window 
from vendor import vendor 
from clear import clear
from player import player
import sys

class tradingWindow(Window):
    def __init__(self, x, y, w, h, name,itemsList:list[item]):
        super().__init__(x, y, w, h, "All")
        
        self.books = list()
        self.weapons = list() 
        self.food = list()
        self.helmets = list() 
        self.rods = list()
        self.armour = list() 
        self.misc = list()
        self.allItems = itemsList
        self.currentList = self.allItems
        self.sortIntoCat() 
        self.catsList = [self.allItems,self.weapons,self.armour,self.helmets,self.food,self.rods,self.books,self.misc]
        self.namesDict = {0:"All Items",1:"Weapons",2:"Armour",3:"Helments",4:"Food",5:"Fishing Rods",6:"Books",7:"Misc"} 
        self.index = 0
        self.menu = arrowMenu(self.renderCurrentList(),self.h-1)
    def catChange(self,change:int):
           running = True 
           tempIndex = self.index
           while running:
                if self.index + change > 7:
                    self.index = -1 
                elif self.index + change <0:
                    self.index = 6 
                
                # Check to see if there are items in the cat 
                self.index += change 
                if(len(self.catsList[self.index])> 0):
                    running = False 
                    self.currentList = self.catsList[self.index]
                    self.menu.list = self.renderCurrentList()
                    
                    self.updateName(self.namesDict[self.index])
                    self.menu.position = 0
                    self.menu.index =0
                    self.menu.selected = 0
                else:
                    running = False
                    
                # Not sure if this works
    def addItem(self,item:item):
        self.allItems.append(item)
        self.sortIntoCat()
        self.clear()
        self.menu.list = self.renderCurrentList()
        self.menu.renderList()           
    def removeItem(self,selected:int):
        if self.currentList != self.allItems:
            self.allItems.remove(self.currentList.pop(selected))
        else:
            self.currentList.pop(selected)
        self.sortIntoCat()
        self.clear()
        self.menu.list = self.renderCurrentList()
        self.menu.renderList()
        #self.row_draw(self.renderCurrentList())         
    def mainLoop(self):
        running = True
        
        while running:
            rawList = self.menu.renderList()
            self.row_draw(rawList)
            selected = self.menu.mainLoop()
            if type(selected) == list:
                rawList = selected 
            elif selected == -1:
                self.catChange(1)
                 
                pass
            elif selected == -2:
                self.catChange(-1)
            elif selected == -3:
                self.row_draw(rawList)
                return(-1)
                #nextWindow 
                pass 
            elif selected == -4:
                self.row_draw(rawList)
                #prevWindow
                return(-2)
            elif selected >= 0:
                return(selected)
                pass
            else:
                return(selected)
    def sortIntoCat(self):
        self.books = []
        self.weapons = []
        self.food = []
        self.helmets = [] 
        self.rods = []
        self.armour = [] 
        self.misc = []

        for item in self.allItems:
            t = type(item)
            if t is weapon:
                self.weapons.append(item)
            elif t is armour:
                self.armour.append(item)
            elif t is book:
                self.books.append(item)
            elif t is fish or food:
                self.food.append(item)
            elif t is helmet:
                self.helmets.append(item)
            elif t is fishingRod:
                self.rods.append(item)
            else:
                self.misc.append(item)
        self.catsList = [self.allItems,self.weapons,self.armour,self.helmets,self.food,self.rods,self.books,self.misc]
    def renderCurrentList(self)->list[str]:
        outList = []
        for item in self.currentList:
            #TODO 
            #When selling worth less when buying they sell for more
            priceStr = str(item.value)
            nameW = self.w - len(priceStr)
            outList.append(str(item.name[:nameW].ljust(nameW) + priceStr))
        return outList
    def lstNoSelect(self):
        self.clear()
        self.row_draw(self.renderCurrentList())

class transWindow(tradingWindow):
    # This probbaly breaks a couple solid principles , sorry Tracy
    def __init__(self, x, y, w, h, playerInv,vendorInv):
        super().__init__(x, y, w, h, "Current Transaction ",[]) 
        self.sum = 0
        #
        #self.menu = arrowMenu(self.allItems,self.h)
        self.playerValue = 0
        self.vendorValue = 0
        self.checkList = list()#To make it work better with inherted instructions have same index for owner value instead of tuple
        self.playerItems = playerInv 
        self.vendorItems = vendorInv
    def removeItem(self,index:int):
        item = self.allItems[index]
        if(self.checkList[index]):
            self.playerValue -= item.value
            reTup = (True,item)
        else:
            self.vendorValue -= item.value
            reTup = (False,item)
        del self.allItems[index]
        del self.checkList[index]
        # Select item above removed item 
        if index >0:
            self.menu.selected = index -1
        self.menu.list = self.renderCurrentList()
        self.clear()
        self.row_draw(self.menu.renderList())
        

        return(reTup)
    def addItem(self,itemTuple):
        # True means it's from the player 
        self.allItems.append(itemTuple[1])
        self.checkList.append(itemTuple[0])
        if itemTuple[0]:
            self.playerValue += itemTuple[1].value
        else:
            self.vendorValue += itemTuple[1].value 
        #self.currentList = self.allItems
        self.menu.list = self.renderCurrentList()
        self.row_draw(self.renderCurrentList())    
    def mainLoop(self):
        running = True
        while running:
            rawList = self.menu.renderList()
            self.row_draw(rawList)
            selected = self.menu.mainLoop()
            if type(selected) == list:
                rawList = selected 
            # I don't think i want cat changes for this 
            # elif selected == -1:
            #     self.catChange(1)
                 
            #     pass
            # elif selected == -2:
            #     self.catChange(-1)
            elif selected == -3:
                self.row_draw(rawList)
                return(-1)
                #nextWindow 
                pass 
            elif selected == -4:
                self.row_draw(rawList)
                #prevWindow
                return(-2)
                pass
            elif selected >= 0:
                self.selected = selected
                return(self.removeItem(selected))
                pass
            else:
                return(selected)
class valueWin(Window):
    #TODO Make it have no border 
    def __init__(self, x, y, w, h, playerValue,vendorValue,playerMoney):
        super().__init__(x, y, w, h, "Transaction Value")
        self.player = playerValue 
        self.vendor = vendorValue 
        self.playerMon = str(playerMoney)
        self.sum = playerValue - vendorValue 
        self.update(self.player,self.vendor)
    def update(self,playerValue,vendorValue):
        self.player = playerValue
        self.vendor = vendorValue 
        self.sum = playerValue - vendorValue
        sum = str() 
        if self.sum >0:
            #Green
            colour = "\033[32m"
            pass 
        elif self.sum < 0:
            #red
            colour = "\033[31m"
            pass 
        else:
            #orange/Yellow 
            colour = "\033[33m"
            pass 
    
        sum = colour + str(self.sum) + "\033[0m"
        rows = ["","Player Item Value: "+str(self.player),"","Vendor Item Value: "+str(self.vendor),"","Player Funds:      "+self.playerMon,"","Transaction Sum:   "+sum]
        self.clear() 
        self.row_draw(rows)
class tradingMenu:
    def __init__(self,Player,Vendor):
        clear()
        self.activeWin = 0
        
        sys.stdout.write(f"\033[{0};{0}H{Player.name}")
        
        playerItems = [] 
        for item in Player.items:
            if item not in Player.equiptItems.values():
                playerItems.append(item)
        self.playerWindow = tradingWindow(0,2,35,30,"Player",playerItems) 
        self.transWindow = transWindow(self.playerWindow.w+10,3,25,15,Player.items,Vendor.items)
        self.transInfoWindow = valueWin(self.transWindow.x,self.transWindow.h+self.transWindow.y + 3,self.transWindow.w,9,0,0,Player.gold)
        self.traderWindow = tradingWindow(self.transWindow.x+self.transWindow.w+10,self.playerWindow.y,self.playerWindow.w,30,"Vendor",Vendor.items)
        sys.stdout.write(f"\033[{0};{self.traderWindow.x+1}H{Vendor.name}")
        sys.stdout.write(f"\033[{self.playerWindow.h + self.playerWindow.y+4};{0}H{'Change Category: <- -> ,Change Window: z x, Confirm Transaction: c , Exit b'}")
        self.winDict = {0:self.playerWindow,1:self.transWindow,2:self.traderWindow}
        self.traderWindow.lstNoSelect()
        self.selected = None
        running = True
        while running:
            self.selected = self.winDict[self.activeWin].mainLoop()
            #Removing an item from the current transaction back to-
            #correct inventory
            if(type(self.selected) == tuple):
                #Back to the player
                if(self.selected[0]):
                    self.playerWindow.addItem(self.selected[1])
                    self.playerWindow.lstNoSelect()
                    pass
                else:
                    #back to vendor
                    self.traderWindow.addItem(self.selected[1])
                    self.traderWindow.lstNoSelect() 
                self.transInfoWindow.update(self.transWindow.playerValue,self.transWindow.vendorValue)
            #End transaction 
            elif self.selected == -5:
                buy = False
                sum = self.transWindow.playerValue - self.transWindow.vendorValue
                #Check can afford 
                if sum > 0:
                    Player.gold+= sum 
                    running = False
                    
                    buy = True
                else:
                    
                    if Player.gold >= abs(sum):
                        Player.gold += sum 
                        buy = True
                        running =  False 
                if buy :
                    equiptItems = []
                    for item in list(Player.equiptItems.values()):
                        if item != None:
                            equiptItems.append(item)
                    Player.items = self.playerWindow.allItems + equiptItems
                    Vendor.items = self.traderWindow.allItems
                    counter = 0
                    for item in self.transWindow.allItems:
                        if not self.transWindow.checkList[counter]:
                            Player.items.append(item)
                        else:
                            Vendor.items.append(item)
                        counter +=1
            elif self.selected == -6:
                counter =0
                for item in self.transWindow.allItems:
                    
                        if self.transWindow.checkList[counter]:
                            Player.items.append(item)
                        else:
                            Vendor.items.append(item)
                        counter +=1
                running = False
            #change window
            elif self.selected < 0:
                self.winDict[self.activeWin].lstNoSelect()
                if self.selected == -1:
                    if self.activeWin == 2 :
                        self.activeWin = 0 
                    else:
                        self.activeWin +=1
                elif self.selected == -2:
                    if self.activeWin == 0 :
                        self.activeWin = 2 
                    else:
                        self.activeWin -=1
            
                
                pass
            
            else :
                #add to the transaction 
                if(self.activeWin == 0):
                    self.transWindow.addItem((True,playerItems[self.selected]))
                    self.playerWindow.removeItem(self.selected)
                    self.transInfoWindow.update(self.transWindow.playerValue,self.transWindow.vendorValue)
                    
                    pass 
                elif(self.activeWin == 2):
                    self.transWindow.addItem((False,self.traderWindow.currentList[self.selected]))
                    self.traderWindow.removeItem(self.selected)
                    self.transInfoWindow.update(self.transWindow.playerValue,self.transWindow.vendorValue)
# clear()             
# Player = player("Player")
# Player.items.append(weapon("Kitchen Fork",10,1,1,"A kitchen fork, not a fancy one. Is made from steel. Handle has some rust on it, probbaly reduces the value"))
# Player.items.append(armour("Raggy top",1,3,"A raggy smelly top. Has more holes than not."))
# Player.items.append(book("hobbit",100,"Once was there and back again"))

# Vendor = player("Vendor")
# Vendor.items.append(weapon("Kitchen Fork",10,1,1,"A kitchen fork, not a fancy one. Is made from steel. Handle has some rust on it, probbaly reduces the value"))
# Vendor.items.append(armour("Raggy top",1,3,"A raggy smelly top. Has more holes than not."))
# Vendor.items.append(book("hobbit",100,"Once was there and back again"))

# testMenu = tradingMenu(Player,Vendor)
from clock import *
import random
from vendor import * 
from item import * 
from player import *
from window import *
from selectMenu import *
from ascii import *
from clear import *
from tradingMenu import *
from repairMenu import *
townNames = [
    # -ton / -ham
    "Wyrmton", "Aelricton", "Dunham", "Eastmereton", "Brambleton",
    "Eldham", "Thorneton", "Crowtham", "Fenrithton", "Caerham",

    # -ford
    "Ashford", "Blackford", "Elmsford", "Redglenford", "Grimford",
    "Oakensford", "Mireford", "Dunford Hollow", "Silverford", "Ravenford",

    # -wich / -wick
    "Wyrwich", "Aldwick", "Greywich", "Thornwick", "Dunwich",
    "Hollowwick", "Fenwicke", "Norwick", "Braywick", "Mistwick",

    # -stead / -stow
    "Hearthstead", "Wattlestead", "Broadstow", "Fairstead", "Coldstow",
    "Greenstead", "Crowstead", "Wraithstow", "Stonehirstead", "Fogstow",

    # -leigh / -ley
    "Fernleigh", "Harthley", "Emberley", "Oakley Cross", "Windleigh",
    "Hollowley", "Barrowleigh", "Thistley", "Grimley Hill", "Wyrley Moor",

    # -bridge / -bury / -holt
    "Alderbridge", "Thornbury", "Elmbury", "Redbridge", "Hawkbridge",
    "Dunholt", "Brambleholt", "Ashbury", "Lowbridge", "Goldbury"
]
class town:
    def __init__(self,ItemManager:itemManager):
        self.lastUpdate = 0
        # TODO maybe make different town culture depending on the position
        self.ItemManger = ItemManager 
        self.name = random.choice(townNames) 
        self.Smithy = blackSmith(0,self.ItemManger)
        self.Hunts = hunts(0,self.ItemManger)
        self.Grocer = grocer(0,self.ItemManger)
        self.ascii = ascii()
        self.Player = None
        self.menu =  arrowMenu(["Black Smith","Grocer","Woodsman","Leave Town"],6)
        self.Smithy.generateInventory(1)
        self.Grocer.generateInventory(1)
        self.Hunts.generateInventory(1)
    def townMainLoop(self,currentTime:list[int],Player:player):
        self.townWin = Window(0,8,20,5,"Town Services")
        self.Player = Player
        if (currentTime[0]-self.lastUpdate >=1 ):
            # Updating the vendors item lists 
            self.Smithy.generateInventory(Player.level)
            self.Grocer.generateInventory(Player.level)
            self.Hunts.generateInventory(Player.level)
            self.lastUpdate = currentTime[0]
            
            
        running = True 
        self.mainMenu()
        return()
    
    def mainMenu(self):
        
        running = True 
        
        
        
        
        self.drawMenu()
        while running:
            self.townWin.row_draw(self.menu.renderList())
            selected = self.menu.mainLoop()
            match(selected):
                case 0:
                    #blackSmith
                    
                    while True:
                        clear()
                        print("What service would you like?")
                        print("0: Trade")
                        print("1: Repair Equiptment")
                        print("2: Enhance Equiptment")
                        print("3: Exit")
                        try:
                            choice = int(input(">"))
                        except:
                            if(choice.lower() == "b"):
                                break
                            else:
                                continue
                        
                        if choice == 0 :
                            TradMen = tradingMenu(self.Player,self.Smithy)
                            break 
                        elif choice ==1 :
                            repWin = repairWindow(self.Player)
                            break
                        elif choice == 3:
                            running = False
                    self.drawMenu()
                    
                case 1: 
                    #grocer 
                    # Copy the grocer's menu here 
                    TradMen = tradingMenu(self.Player,self.Grocer)
                    self.drawMenu()
                    pass
                case 2:
                    TradMen = tradingMenu(self.Player,self.Hunts)
                    self.drawMenu()
                case 3:
                    running = False
         
    def drawMenu(self):
        clear()
        self.ascii.draw((0,0),self.name,"Green") 
        self.townWin.draw()

        
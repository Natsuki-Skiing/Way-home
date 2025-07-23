
from player import *
from ascii import *
from clear import *
from printAt import *
class campFire:
    def __init__(self,location,woodLevel = 10):
        self.woodLevel = woodLevel 
        self.respawnPoint = False
        self.location = location
        self.respawnCost = 5
        pass
    def drawMenu(self):
        title = ascii
        campColours = ["red","yellow"]
        
        
        clear()
        
        title.draw((0,0),"Campfire",random.choice(campColours))
        printAt(0,17,("Current wood level: "+str(self.woodLevel)))
        printAt(0,18,("Is current respawn point: "+str(self.respawnPoint)))
        printAt(0,20,("0 : Sleep (10 wood)"))
        printAt(0,21,("1 : Set as spawn"))
        printAt(0,22,("2 : Add wood to fire"))
        printAt(0,23,"3 : Back")
            
    def checkRespawn(self):
        returnValue = False 
        if(self.woodLevel >= self.respawnCost):
            returnValue = True 
            self.woodLevel -= self.respawnCost 
        
        return(returnValue)
        
        
        return(returnValue)   
    def mainLoop(self,Player:player):
        Player = Player
        running = True
        while running:
            self.drawMenu()
            try:
                    choice = int(input(">"))
                    if choice == 0 :
                        clear()
                        if self.woodLevel >= 10:
                            self.woodLevel -= 10
                            Player.hp = Player.maxHp
                            print("Health restored")
                            
                        else:
                            print("Not enough wood to heal")
                        input("Press enter to continue")
                    elif choice == 1:
                        self.setSpawn(Player) 
                    elif choice == 2:
                        self.addWood(Player)
            except:
                continue
    def addWood(self,Player:player):
        numberOfWood = 0
        for item in Player.items:
            if item.name == "wood":
                numberOfWood +=1 
        if numberOfWood == 0:
            print("You have no wood")
            print("Wood can be bought from vendors in towns")
            input("Press enter to continue")
        else:
            print("Amount of wood in inventory: ",numberOfWood)
            print("Enter amount needed , 0 to exit")
            
            running = True
            while running:
                try:
                    amount = int(input(">"))
                    if amount == 0:
                        running = False 
                    elif amount < 0 or amount > numberOfWood :
                        continue
                    else:
                        removed = 0
                        currentIndex = 0
                        length = len(Player.items)
                        while currentIndex < length and removed < amount:
                            if Player.items[currentIndex].name == "wood":
                                Player.items.pop(currentIndex)
                                removed += 1
                            else:
                                currentIndex += 1
                        running = False
                                        
                except:
                    continue 
            
            print("Added ",amount," of wood to fire")
            input("Press enter to return")
            
    def setSpawn(self,Player:player):
        playerOk = False
        clear()
        if Player.respawnCamp == None:
            playerOk = True
        else:
            campLoc = str(Player.respawnCamp.location)
            print("There is already a camp set as spawn point at ",campLoc)
            print("To set it back to the previous campfire would require travelling back to it")
            print("Do you still want to continue? (y/n)")
            running = True
            while(running):
                
                try:
                    choice = input(">").lower()
                    if choice == "y":
                        playerOk = True
                        clear()
                except:
                    continue
        
        if playerOk:
            self.respawnPoint = True
            Player.respawnCamp = self 
            print("Respawn set")
            print("To respawn the campfire needs to have at least ",self.respawnCost," wood")
            input("Press enter to continue") 
        
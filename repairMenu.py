from printAt import *
from item import * 
from player import * 
from window import *
from clear import *
import math
import time 

class repairWindow:
    def __init__(self, playerInstance):
        self.playerInstance = playerInstance 
        self.repairableItems = []
        self.numberOfItems = 0
        
        anvilArt = [
            " .-------..___",
            "  '-._     :_.-'",
            "   .- ) * ( --.",
            "  :  '-' '-'  ;.",
            " /'-..*____.-' |",
            " |   |     \\   |",
            " \\   |     /   \\",
            " |   \\     )_.-'",
            " '-._/__..-'",
            "",
            "Price:",
            "1 Gold for 2 condition points",
            "Still applies if only 1 needed"
        ]
        
        self.itemWindow = Window(0, 0, 40, 30, "Repairable Items")
        self.anvilWindow = Window(self.itemWindow.w + 2, 0, 35, 15)
        self.anvilWindow.row_draw(anvilArt) 
        
        self.helpWindow = Window(
            self.itemWindow.w + 2, 
            self.anvilWindow.h + 2, 
            self.anvilWindow.w, 
            (self.itemWindow.h - self.anvilWindow.h - 2), 
            "Controls"
        )
        controls = ["Back : B"]
        self.helpWindow.row_draw(controls)
        
        self.runRepairLoop()
        self.playerInstance.items.extend(self.repairableItems)
        
    def runRepairLoop(self):
        while True:
            self.refreshDisplay()
            cursorY = self.itemWindow.h + 4
            print(f"\033[{cursorY};0H", end="")
            
            userChoice = input(">").lower()
            if userChoice == "b":
                break
                
            if self.processItemSelection(userChoice):
                self.redrawWindows()
    
    def processItemSelection(self, userChoice):
        try:
            itemIndex = int(userChoice)
        except ValueError:
            return False
            
        if not (0 <= itemIndex < self.numberOfItems):
            return False
            
        selectedItem = self.repairableItems[itemIndex]
        return self.handleRepairProcess(selectedItem, itemIndex)
    
    def handleRepairProcess(self, selectedItem, itemIndex):
        print(f"How many points to repair {selectedItem.name}?")
        print(f"Max number: {selectedItem.maxCondition}")
        print(f"Current condition: {selectedItem.condition}")
        print("0 to go back")
        
        while True:
            try:
                repairPoints = int(input(">"))
                if repairPoints == 0:
                    return True
                    
                if repairPoints > selectedItem.maxCondition:
                    print("Cannot repair more than maximum condition")
                    continue
                    
                repairCost = math.ceil(repairPoints / 2)
                
                if repairCost > self.playerInstance.gold:
                    print("Cannot afford")
                    print(f"Costs {repairCost} gold, you only have {self.playerInstance.gold}")
                    print("Enter 0 to go back")
                    continue
                    
                if self.confirmRepair(repairCost):
                    selectedItem.condition += repairPoints
                    self.playerInstance.gold -= repairCost
                    return True
                else:
                    return True
                    
            except ValueError:
                print("Please enter a valid number")
                continue
    
    def confirmRepair(self, cost):
        print(f"This will cost {cost} gold. Continue? (Y)es /(N)o")
        while True:
            try:
                confirmation = input(">").lower()
                if confirmation == "n":
                    return False
                elif confirmation == "y":
                    return True
            except:
                continue
    
    def sortRepairableItems(self):
        itemList = []
        self.numberOfItems = 0
        
        for item in self.playerInstance.items[:]:
            if self.isRepairable(item):
                self.repairableItems.append(item)
                itemList.append(f"{self.numberOfItems}: {item.name}")
                self.numberOfItems += 1
                self.playerInstance.items.remove(item)
                
        return itemList
    
    def isRepairable(self, item):
        return (isinstance(item, (weapon, fishingRod)) and 
                item.condition != item.maxCondition)
    
    def refreshDisplay(self):
        self.itemWindow.clear()
        self.playerInstance.items.extend(self.repairableItems)
        self.repairableItems.clear()
        self.itemWindow.row_draw(self.sortRepairableItems())
    
    def redrawWindows(self):
        clear()
        self.helpWindow.draw()
        self.anvilWindow.draw()
        self.itemWindow.draw()
        
        anvilArt = [
            " .-------..___",
            "  '-._     :_.-'",
            "   .- ) * ( --.",
            "  :  '-' '-'  ;.",
            " /'-..*____.-' |",
            " |   |     \\   |",
            " \\   |     /   \\",
            " |   \\     )_.-'",
            " '-._/__..-'"
        ]
        
        self.anvilWindow.row_draw(anvilArt)
        controls = ["Back : B"]
        self.helpWindow.row_draw(controls)
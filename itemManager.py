from item import * 
import json 
import random
import copy
class itemManager:
    def __init__(self,folder:str):
        # Dict of the types 
        # Dist of each class within that dict 
        # Each level is a list of items
        # Classes are kinda link how rare the item is
        self.folder = folder +'/'
        self.AllItems = {"weapon":dict(),"armour":dict(),"fish":dict(),"helmet":dict(),"potion":dict(),"fishingRod":dict()}#"book":dict(),} #DEBUG
        for type in self.AllItems.keys():
            try:
                self.populateDict(type)
            except:
                pass
        pass
    def getItem(self,Type:str,itemClass:int,itemLevel:int):
        # if its a range it get a random item from that range
        #DEBUG remove try when made all items for the game
        
        item = copy.deepcopy(random.choice(self.AllItems[Type][itemClass]))
        
        if itemClass == "armour" or itemClass == "weapon":
            item.scaleStatsForLevel(itemLevel)
        
        return(item)
    def populateDict(self,type:str):
        with open((self.folder+type+".json")) as f:
            raw = json.load(f) 
        
        for entry in raw:
            match (entry["type"]):
                case "Weapon":      
                    newItem = weapon(entry["name"],  entry["damage"], entry["maxCondition"], entry["value"], entry["description"])
                case "Helmet":      
                    newItem = helmet(entry["name"],  entry["protection"], entry["value"], entry["description"])
                case "Armour":      
                    newItem = armour(entry["name"],  entry["protection"], entry["value"], entry["description"])
                case "Fish":        
                    newItem = fish(entry["name"],  entry["value"], entry["description"], entry["hp"], entry["dayTillRot"])
                case "Book":        
                    newItem = book(entry["name"],  entry["value"], entry["description"])
                case "FishingRod":  
                    newItem = fishingRod(entry["name"],  entry["value"], entry["description"])
                case "Potion":      
                    newItem = potion(entry["name"],  entry["value"], entry["description"])
                case _:             
                    raise ValueError(f"Unknown item type: {entry['type']}")

                
                
            if entry["class"] in self.AllItems[type].keys():
                self.AllItems[type][entry["class"]].append(newItem)
            else:
                self.AllItems[type][entry["class"]] = [newItem]
         

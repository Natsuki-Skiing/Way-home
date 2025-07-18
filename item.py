
import math
class item:
    def __init__(self,name:str,value:int,description:str):
        self.name = name
        self.value = value
        self.description = description
class armour(item):
    def __init__(self,name:str,protection:int,value:int,description:str):
        super().__init__(name,value,description)
        self.protection = protection
        self.level = 0
    def scaleStatsForLevel(self,level:int):
        growthRate = 0.5
        #Setting the states for the level  
        self.protection = int((self.protection*0.5) * (level * growthRate))
class fish(item):
    def __init__(self,name:str,value:int,description:str,hp:int,dayRot:int):
        super().__init__(name,value,description)
        self.hp = hp 
        self.dayTillRot = dayRot 
        
class food(fish):
    def __init__(self, name, value, description, hp, dayRot):
        super().__init__(name, value, description, hp, dayRot)
               
class helmet(armour):
    def __init__(self,name:str,protection:int,value:int,description:str):
        super().__init__(name,protection,value,description)
        
class weapon(item):
    def __init__(self,name:str,damage:int,maxCondition:int,value:int,description:str):
        super().__init__(name,value,description)
        self.damage = damage
        self.maxCondition = maxCondition
        self.condition = self.maxCondition
        self.level = 0
    def scaleStatsForLevel(self,level:int):
        growthRate = 0.5
        #Setting the states for the level  
        self.damage = int(self.damage * (level * growthRate))
        self.maxCondition = int(self.maxCondition * (level * growthRate))
        self.condition = self.maxCondition
    def reduceCondtion(self,value:int):
        self.condition -= value 
        if self.condition == 0:
            self.value = 0
        else:
            self.value = int(math.ceil(self.value *(self.condition/self.maxCondition)))

class book(item):
    def __init__(self,name:str,value:int, description:str):
        super().__init__(name,value,description)
        self.path = "books/"+name+".txt"
        self.page = 0
class fishingRod(item):
    def __init__(self,name:str,value:int,description:str,distMod:float,maxCondition:int):
        super().__init__(name,value,description)
        self.distMod = distMod
        self.maxCondition = maxCondition
        self.condition = self.maxCondition
    def reduceCondtion(self,value:int):
        self.condition -= value 
        if self.condition == 0:
            self.value = 0
        else:
            self.value = int(self.value *(self.condition/self.maxCondition))
    
class potion(item):
    def __init__(self, name, value, description):
        super().__init__(name, value, description)
    
class spellIngredient(item):
    def __init__(self, name, value, description):
        super().__init__(name, value, description)
equipableItems = [armour,weapon,helmet,fishingRod]
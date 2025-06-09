

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

class book(item):
    def __init__(self,name:str,value:int, description:str):
        super().__init__(name,value,description)
        self.path = "books/"+name+".txt"
        self.page = 0
class fishingRod(item):
    def __init__(self,name:str,value:int,description:str):
        super().__init__(name,value,description)
        
    
class potion(item):
    def __init__(self, name, value, description):
        super().__init__(name, value, description)
    
    
equipableItems = [armour,weapon,helmet]
from creature import creature

class opp(creature):
    def __init__(self,name:str,baseHp:int,baseDef:int,baseAttack:int,Class:int=0,level =None):
        #TODO
        #Want to make it more interesting like they can use spells and shit
        self.baseAttack = baseAttack
        self.baseDef = baseDef
        self.baseHp = baseHp
        self.Class = 0
        super().__init__(name,level,baseHp)
    def scaleStat(self,base, level, multiplier):
        return int(base * (level * multiplier))

    def scaleForLevel(self,level:int):
        self.level = level
        self.maxHp = self.scaleStat(self.baseHp, level, 0.5)
        self.hp = self.maxHp
        self.defense = self.scaleStat(self.baseDef, level, 0.4)
        self.attack = self.scaleStat(self.baseAttack, level, 0.3)
    
        
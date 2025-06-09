class creature:
    def __init__(self,name:str,level:int,hp:int):
        self.name = name
        
        self.hp = hp
        self.maxHp =hp
        self.level = level
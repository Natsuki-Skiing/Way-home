from creature import *
import os 
import sys


class healthBar:
    def __init__(self,target:creature,width:int = 10):
        self.colourTable = {
        "reset": "\033[0m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "red": "\033[31m", 
        } 
        self.Target = target 
        self.colour = "green"
        self.string = str()
        self.width = width
        self.update()
    def update(self):
        if self.Target.hp <= 0:
            self.colour = "red"
            noBars = 0
        else:
            ratio = self.Target.hp / self.Target.maxHp
            perHealth = round(ratio * 100, 2)
            
            if perHealth >=70:
                self.colour = "green"
            elif perHealth >= 40:
                self.colour = "yellow"
            else: 
                self.colour = "red"
            toBars = self.width - 2
            noBars = int(toBars * ratio)
            if noBars == 0 and perHealth >0:
                noBars = 1
        self.string = "["+"▮"*noBars+"▯"*(self.width-2-noBars) +" ]"
    def render(self)->str:
        return(f"{self.colourTable[self.colour]}{self.string}\033[0m")   

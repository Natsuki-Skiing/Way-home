import os
import sys 
import readchar
from clear import clear
class arrowMenu:
    def __init__(self,list:list[str],height:int= 20):
        self.list = list
        self.len  = len(list)-1
        self.height = height -1
        self.selected = 0 
        self.position = 0
        self.listShown = self.list[0:height]
    def renderList(self)->list[str]:
        window = self.list[self.position : self.position + self.height]
        outList = []
        for local_idx, item in enumerate(window):
            abs_idx = self.position + local_idx
            if abs_idx == self.selected:
                outList.append(f"\033[7m{item}\033[0m")
            else:
                outList.append(item)
        return outList
    
    def listScroll(self,change:int):
        self.selected += change
        self.selected = max(0, min(self.selected, len(self.list) - 1)) 
        
        if self.selected < self.position:
            self.position = self.selected
        elif self.selected >= self.position + self.height:
            self.position = self.selected - self.height + 1
    def mainLoop(self):
        running = True 
        #Might need a loop here eh i dunno 
        match(readchar.readkey()):
            case readchar.key.UP:
                if self.selected >0:
                    self.listScroll(-1)
            case readchar.key.DOWN:
                if self.selected < len(self.list):
                    self.listScroll(1) 
            case readchar.key.ENTER:
                return(self.selected)
            case readchar.key.LEFT:
                return(-2)
            case readchar.key.RIGHT :
                return(-1)
            case "x":
                return(-3)
            case "z":
                return(-4)
            case "c":
                #confirm trade it's over
                return(-5)
            case "b":
                #Exiting from the menu without the confirming the menu
                return(-6)
                
        return self.renderList()
                        
                        


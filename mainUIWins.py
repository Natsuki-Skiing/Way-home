from window import * 
from player import * 
from healthBar import *
class statWin(Window):
    def __init__(self, x, y, w, h, name,currentMap,Player:player,time:tuple[int,int,int]):
        super().__init__(x, y, w, h, name)
        self.bar = healthBar(Player,w-1)
        self.currentMap = currentMap
        self.time = time
        self.update()
    def updateMap(self,currentMap):
        self.currentMap = currentMap
        self.update()
    def update(self):
        self.bar.update()
        rows = ["Health",self.bar.render(),"","Map",(" "+str(self.currentMap[0])+" , "+str(self.currentMap[1])),"","Time: "+str(self.time[1])+" : "+str(self.time[2]),"", "Day : "+str(self.time[0])]
        
        self.clear()
        self.row_draw(rows) 
    def updateSetTime(self,time:tuple[int,int,int]):
        self.time = time
        self.update()
        
class logWin(Window):
    def __init__(self, x, y, w, h, name=None):
        super().__init__(x, y, w, h, name)
        self.lines = list()
    def addMsg(self,msg:str):
        newList = list()
        if (len(msg) > self.w):
            # Wanna have this for multi line statments
            pass
        else:
            newList.append(msg) 
        
        self.lines = newList + self.lines
        
        if len(self.lines) > self.h:
            del self.lines[-(len(self.lines) -self.h)]
        self.update()
            
    def update(self):
        self.clear()
        counter = 0
        for line in self.lines:
            self.draw_text(0,counter,(line))
            counter +=1

class interWin(Window):
    def __init__(self, x, y, w, h, name=None):
        super().__init__(x, y, w, h, "Actions")
        self.stack = list()
    def addAction(self,action:str):
        if action not in self.stack:
            self.stack.append(action)
            self.update()
    def removeAction(self, action: str):
        itemsToRemove = [item for item in self.stack if action in item]
        if itemsToRemove:
            self.stack.remove(itemsToRemove[0])
            return True
        else:
            return False 
    def update(self):
        self.clear()
        counter =0
        for action in self.stack:
            self.draw_text(0,counter,action)
            counter +=1
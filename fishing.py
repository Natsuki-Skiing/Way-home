import random 
import time
import platform
import sys 
import math
from clear import *
import threading
from tile import * 
from printAt import *
from window import * 
from player import *
from items import *
from itemManager import *
water = tile("≈",False,"blue")
fishTile = tile("F",False,"yellow")
selectedWater = tile("≈",False,"red")
selectedFish = tile("F",False,"pink")

class fishingGame:
    def showFish(self):
        
            
            
        self.fishX = random.randint(0,self.pondX)
        self.fishY = random.randint(0,self.pondY)
        
        self.imgBuff[self.fishX][self.fishY] = fishTile
        self.drawBuffer()
        
    def startState(self):
        #Fish appear in random location 
        running = True 
        while running:
            #wait rand time for a fish to appear
            time.sleep(random.uniform(2.0,7.0))
            
            self.showFish()
            
            if(self.Input()):
                #DEBUG
                running = False
                self.selectedBuffer[self.fishX][self.fishY] = selectedFish
            else:
                self.imgBuff[self.fishX][self.fishY] = water
                self.drawBuffer()
            
        pass
    def __init__(self,Player:player,itemMan:itemManager):
        self.player = Player
        self.itemMan = itemMan
        self.windows = platform.system() == "Windows"
        self.timeout = 0.35
        self.fishX = -1 
        self.fishY = -1
        self.pondX = 29 
        self.pondY = 29
        
        # Trying somthing new here 
        # Dunno if it's good or not 
        if self.windows:
            import msvcrt
            self.msvcrt = msvcrt 
               
        else:
            import select
            import termios
            import tty
            self.select = select
            self.termios = termios 
            self.tty = tty
        clear()
        self.window = Window(0,0,30,30,"Fishing")
        self.imgBuff = [[water for _ in range(self.pondX)] for _ in range(self.pondY)]
        self.selectedBuffer = [[selectedWater for _ in range(self.pondX)] for _ in range(self.pondY)]
        self.pondX -=1 
        self.pondY -=1 
    def renderLine(self,linePos:int,vertical:bool):
        if vertical:
           
            col = [row[linePos] for row in self.selectedBuffer]
            image = [
                row[:linePos] + [col[i]] + row[linePos+1:]
                for i, row in enumerate(self.imgBuff)
            ]
        else:
            
            line = self.selectedBuffer[linePos].copy()
            image = self.imgBuff.copy()
            image[linePos] = line
    
        
        self.drawBuffer(buffer = image)
        return(image)
            
        
            
        
    def line(self,vertical:bool):
        
        if(bool(random.randint(0,1))):
            linePos = 0
            direction = True 
        else:
            linePos = self.pondX 
            direction = False
        
        running = True
        
        # Need to change the timeout time, maybe half ?
        if vertical:
            self.timeout = 0.003
        else:
            self.timeout = 0.0035
        while running:
            # Changes direction if at edges
            image = self.renderLine(linePos,vertical)
            if direction:
                if linePos == self.pondX:
                    direction = False 
            else:
                if linePos == 0:
                    direction = True 
            
            if(self.Input()):
                self.imgBuff = image.copy()
                break 
            else:
                if(direction):
                    linePos +=1 
                else:
                    linePos -=1
        
        return(linePos)
            
                    
    def castingState(self)->tuple:
        #X or y first 
        vertical = bool(random.randint(0,1))
        
        fv = self.line(vertical)
        #Go other way
        vertical = not vertical
        sv = self.line(vertical)
        
        if(vertical):
            return((fv,sv))
        else:
            return(sv,fv)
        
    def drawBuffer(self,buffer= None):
        if buffer:
            imgBuff = buffer
        else:
            imgBuff = self.imgBuff
        renderList = []
        for row in imgBuff:
            rowStr = str()
            for tile in row:
                rowStr += tile.render()
            renderList.append(rowStr)
        self.window.row_draw(renderList)
    def getFish(self,dist:float):
        gotFish = False 
        dist = int(dist)
        if(dist == 0):
            gotFish = True
        elif(0 == random.randint(0,int(dist))):
            gotFish = True 
        if gotFish:
            classWeight = [6,5,5,4,4,4,4,3,2,1]
            while True:
                try:
                    fClass = random.choices([1,2,3,4,5,6,7,8,9,10],weights=classWeight,k=1)[0]
                    fish = self.itemMan.getItem("fish",fClass,0)
                    break
                except:
                    continue
            return(fish)
        else:
            return(None)
    def mainLoop(self):
        
        running = True
        self.drawBuffer()
        self.startState()
        self.player.equiptItems["rod"].reduceCondtion(1)
        castTup = self.castingState()
        #Calc dist from cast and fish 
        dist = math.dist(castTup,(self.fishX,self.fishY))
        dist = max(dist - self.player.equiptItems["rod"].distMod,0)
        
        return(self.getFish(dist))
        
        pass
    def Input(self)->bool:
        win = False
        if self.windows:
            timeout = self.timeout *10
            startTime = time.time()
            while time.time()- startTime < timeout:
                if self.msvcrt.kbhit():
                    if self.msvcrt.getwch() == ' ':
                        win = True
                        break 
        else:
            fd = sys.stdin.fileno()
            oldSettings = self.termios.tcgetattr(fd)
            self.tty.setraw(sys.stdin.fileno())
            timeout = self.timeout * 10  # Add timeout value

            try:
                startTime = time.time()
                
                win = False
                
                while time.time() - startTime < timeout:
                    if self.select.select([sys.stdin], [], [], 0)[0]:
                        if sys.stdin.read(1) == ' ':
                            win = True
                            break
                      # Prevent excessive CPU usage
                    
            finally:
                self.termios.tcsetattr(fd, self.termios.TCSADRAIN, oldSettings)
        return(win)


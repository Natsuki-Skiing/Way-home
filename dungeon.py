from tile import *
from player import * 
from battleSystem import * 
from window import * 
from mainUIWins import *
import readchar 
from clear import *
import random
from clock import *
from chest import *
wallVert = tile("│",False,"blue")
leftTop = tile("┌",False,"blue")
leftBottom = tile("└",False,"blue")
rightTop = tile("┐",False,"blue")
rightBottom = tile("┘",False,"blue")
wallHoz = tile("-",False,"blue")
floor = tile(".",True,"gray")
chestTile = tile("C",True,"green")
stairsUp = tile("U",True,"green")
stairsDown = tile("D",True,"red")
corridor = tile("#",True,"gray")
blank = tile(" ",False,"green")
playerTile = tile('P',False,"red")
gold = tile('G',True,"yellow")

class room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = (x + w // 2, y + h // 2)
        self.room_type = self.determineRoomType()
        
    def determineRoomType(self):
        area = self.w * self.h
        if area <= 35:
            return "small"
        elif area <= 70:
            return "medium" 
        else:
            return "large"

class level:
    def __init__(self,w:int,h:int,noRooms:int,):
        self.width = w 
        self.height = h 
        # Removed grid-specific self.cols and self.rows initialization
        self.noRooms = noRooms 
        self.roomMax = 25
        self.roomMin = 5
        self.map = []
        self.knownTiles = []
        self.levelFrames = {}
        self.rooms = []
        self.map = [[None for _ in range(w)] for _ in range(h)]
        self.genRooms()
        self.drawRooms()
        self.connectRooms()
        
    def drawRooms(self):
        for room in self.rooms:
            for y in range(room.y, room.y + room.h):
                for x in range(room.x, room.x + room.w):
                    if y == room.y:
                        if x == room.x:
                            self.map[y][x] = leftTop
                        elif x == room.x + room.w - 1:
                            self.map[y][x] = rightTop
                        else:
                            self.map[y][x] = wallHoz

                    elif y == room.y + room.h - 1:
                        if x == room.x:
                            self.map[y][x] = leftBottom
                        elif x == room.x + room.w - 1:
                            self.map[y][x] = rightBottom
                        else:
                            self.map[y][x] = wallHoz

                    elif x == room.x or x == room.x + room.w - 1:
                        self.map[y][x] = wallVert

                    else:
                        self.map[y][x] = floor
                        
        self.addRoomFeatures()
        
    def addRoomFeatures(self):
        if len(self.rooms) >= 2:
            stairUpRoom = random.choice(self.rooms[1:])
            stairX = random.randint(stairUpRoom.x + 1, stairUpRoom.x + stairUpRoom.w - 2)
            stairY = random.randint(stairUpRoom.y + 1, stairUpRoom.y + stairUpRoom.h - 2)
            self.map[stairY][stairX] = stairsUp
            
        if len(self.rooms) >= 3:
            remainingRooms = [r for r in self.rooms[1:] if r != stairUpRoom] if len(self.rooms) >= 3 else []
            if remainingRooms:
                stairDownRoom = random.choice(remainingRooms)
                stairX = random.randint(stairDownRoom.x + 1, stairDownRoom.x + stairDownRoom.w - 2)
                stairY = random.randint(stairDownRoom.y + 1, stairDownRoom.y + stairDownRoom.h - 2)
                self.map[stairY][stairX] = stairsDown
        
        for room in self.rooms:
            if  random.randint(1, 100) <= 50:
                chestX = random.randint(room.x + 1, room.x + room.w - 2)
                chestY = random.randint(room.y + 1, room.y + room.h - 2)
                self.map[chestY][chestX] = chestTile
                if random.randint(1,3) == 1:
                    chestX = random.randint(room.x + 1, room.x + room.w - 2)
                    chestY = random.randint(room.y + 1, room.y + room.h - 2)
                    self.map[chestY][chestX] = chestTile
            # Removed the incomplete line from the original file
            # self.map[random.randint(room.x + 1, room.x + room.w - 2)][random.randint(room.y + 1, room.y + room.h - 2)]
                        
    def genRooms(self):
        
        numRoomsToGenerate = self.noRooms
        maxAttempts = numRoomsToGenerate * 50

        attempts = 0
        while len(self.rooms) < numRoomsToGenerate and attempts < maxAttempts:
            attempts += 1
            
            w = random.randint(self.roomMin, self.roomMax)
            h = random.randint(self.roomMin, self.roomMax)
            
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)

            newRoom = room(x, y, w, h)
            
            overlap = False
            for existingRoom in self.rooms:
                if (newRoom.x < existingRoom.x + existingRoom.w + 1 and
                    newRoom.x + newRoom.w + 1 > existingRoom.x and
                    newRoom.y < existingRoom.y + existingRoom.h + 1 and
                    newRoom.y + newRoom.h + 1 > existingRoom.y):
                    overlap = True
                    break
            
            if not overlap:
                self.rooms.append(newRoom)
    
    def drawCorridor(self, x1, y1, x2, y2):
        if random.randint(0, 1) == 0:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if self.map[y1][x] is None or self.map[y1][x] != floor:
                    self.map[y1][x] = corridor
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if self.map[y][x2] is None or self.map[y][x2] != floor:
                    self.map[y][x2] = corridor
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if self.map[y][x1] is None or self.map[y][x1] != floor:
                    self.map[y][x1] = corridor
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if self.map[y2][x] is None or self.map[y2][x] != floor:
                    self.map[y2][x] = corridor
                    
    def connectRooms(self):
        if len(self.rooms) <= 1:
            return
            
        connected = [self.rooms[0]]
        unconnected = self.rooms[1:]
        
        while unconnected:
            minDist = float('inf')
            closestPair = None
            
            for connectedRoom in connected:
                for unconnectedRoom in unconnected:
                    dx = connectedRoom.center[0] - unconnectedRoom.center[0]
                    dy = connectedRoom.center[1] - unconnectedRoom.center[1]
                    dist = dx * dx + dy * dy
                    
                    if dist < minDist:
                        minDist = dist
                        closestPair = (connectedRoom, unconnectedRoom)
            
            if closestPair:
                room1, room2 = closestPair
                x1, y1 = room1.center
                x2, y2 = room2.center
                self.drawCorridor(x1, y1, x2, y2)
                
                connected.append(room2)
                unconnected.remove(room2)
        
        numExtraConnections = min(3, len(self.rooms) // 4)
        for _ in range(numExtraConnections):
            room1 = random.choice(self.rooms)
            room2 = random.choice(self.rooms)
            if room1 != room2:
                x1, y1 = room1.center
                x2, y2 = room2.center
                dx, dy = abs(x1 - x2), abs(y1 - y2)
                if dx + dy < (self.width + self.height) // 4:
                    self.drawCorridor(x1, y1, x2, y2)

class dungeon:
    def __init__(self,Player,windowW:int,windowH:int,levX:int,levY:int,noRooms:int,ItMan:itemManager,OpMan:creatureManager,distanceFromStart:int,hasSword = False):
        self.currentLevel = 1
        self.ItMan = ItMan 
        self.OpMan = OpMan
        self.winW = windowW
        self.winH = windowH
        self.levX = levX
        self.levY = levY
        self.noRooms = noRooms
        self.Clock = None
        self.hasSword = hasSword
        self.distFromStrt = distanceFromStart
        self.levels = {}
        self.levels[1] = self.newLevel() 
        self.knownTilesPerLevel = {1:[]}
        self.running = True
        self.player = Player
        self.sightRange = 3
        self.strtRoom =  random.choice(self.levels[self.currentLevel].rooms)
        
        self.chestsDict = dict()
        
        self.foundSword = False
        self.tileSwap = None
        self.playerStrtLoc()
    def newLevel(self)->level:
        return(level(self.levX,self.levY,self.noRooms))
    
    def playerStrtLoc(self):
        
        
        stairX = self.strtRoom.center[0]
        stairY = self.strtRoom.center[1] - 1
        
        if stairY >= self.strtRoom.y + 1:
            self.levels[self.currentLevel].map[stairY][stairX] = stairsUp
        else:
            stairX = self.strtRoom.center[0] + 1
            stairY = self.strtRoom.center[1]
            if stairX <= self.strtRoom.x + self.strtRoom.w - 2:
                self.levels[self.currentLevel].map[stairY][stairX] = stairsUp
        
        
    def renderMap(self):
        halfW, halfH = self.winW // 2, self.winH // 2
        originX = self.player.x - halfW
        originY = self.player.y - halfH
        originX = max(0, min(originX, self.levX - self.winW))
        originY = max(0, min(originY, self.levY - self.winH))

        level = self.levels[self.currentLevel]
        
        self.mainWindow.clear()
        
        for wx, wy in self.knownTilesPerLevel[self.currentLevel]:
            sx, sy = wx - originX, wy - originY
            if 0 <= sx < self.winW and 0 <= sy < self.winH:
                tile = level.map[wy][wx]
                if tile is not None:
                    glyph = tile.render()
                    self.mainWindow.draw_text(sx, sy, glyph)
        
        playerScreenX = self.player.x - originX
        playerScreenY = self.player.y - originY
        self.mainWindow.draw_text(playerScreenX, playerScreenY, playerTile.render())
        
        self.mainWindow.refresh()
        
    def updateKnownTiles(self):
        for x in range(self.player.x - self.sightRange, self.player.x + self.sightRange + 1):
            for y in range(self.player.y - self.sightRange, self.player.y + self.sightRange + 1):
                if (x - self.player.x) ** 2 + (y - self.player.y) ** 2 <= self.sightRange ** 2:
                    if((x,y) not in self.knownTilesPerLevel[self.currentLevel] and 
                       (x < self.levX and x >= 0) and (y < self.levY and y >= 0)):
                        self.knownTilesPerLevel[self.currentLevel].append((x, y))
    
    def battle(self)->bool:
        retValue = False 
        rand = random.randint(1,100)
        if self.tileSwap == corridor and rand < 15:
            battleSystem(self.player,self.OpMan,self.distFromStrt,False)
            retValue = True
            
        elif(rand <=35):
            battleSystem(self.player,self.OpMan,self.distFromStrt+(self.currentLevel),False)
            retValue = True
        return(retValue)    
    def mainLoop(self,Clock:clock):
        self.Clock = Clock
        self.player.x, self.player.y = self.strtRoom.center
        clear()
        self.mainWindow = Window(0,0,self.winW,self.winH,"Dungeon")
        self.statWin = dStatWin(self.mainWindow.w+2,0,30,self.winH-9,self.player.name,(0,0),self.player,self.Clock.GetFullTime(),self.currentLevel)
        self.intWin = interWin(self.winW+2,(self.statWin.h+2),self.statWin.w,(self.winH-self.statWin.h-2),"Actions")
        self.logWin = logWin(0,self.winH+2,self.winW+self.statWin.w+2,7,"Events Log")
        self.Clock = Clock
        self.updateKnownTiles()
        self.renderMap()
        clearInt = False 
        redrawAll = False
        while self.running:
            #Adding comands to the command win 
            
            if(clearInt):
                clearInt = False
                self.intWin.clear()
                self.intWin.stack = []
            match(readchar.readkey()):
                case readchar.key.LEFT:
                    self.movePlayer(9)
                    redrawAll = self.battle()
                case readchar.key.RIGHT:
                    self.movePlayer(3)
                    redrawAll = self.battle()
                case readchar.key.UP:
                    self.movePlayer(12)
                    redrawAll = self.battle()
                case readchar.key.DOWN:
                    self.movePlayer(6)
                    redrawAll = self.battle()
                case "c":
                    if(self.tileSwap == chestTile):
                        redrawAll = True 
                        chestKey = (self.currentLevel,self.player.x,self.player.y)
                        if chestKey in  self.chestsDict.keys():
                            Chest = self.chestsDict[chestKey]
                        else:
                            #Chest that has a sword piece
                            if self.hasSword and not self.foundSword and random.randint(0,3) ==0:
                                Chest = chest(self.player.level+int(self.currentLevel/2),self.ItMan,True)
                                
                            else:
                                
                                Chest = chest(self.player.level+int(self.currentLevel/2),self.ItMan)
                            self.chestsDict[chestKey] = Chest
                                
                                
                        Chest.mainLoop()
                case "u":
                    if(self.tileSwap == stairsUp ):
                        if self.currentLevel > 1 :
                            self.genLevel(False) 
                        else:
                            self.running = False
                            break
                case "d":
                    if(self.tileSwap == stairsDown ):
                        redrawAll = True
                         
                        self.genLevel(True)
            
            if(redrawAll):
                redrawAll = False 
                clear()
                self.logWin.draw()
                self.mainWindow.draw()
                self.intWin.draw()
                self.statWin.draw()
                self.renderMap()
                self.statWin.update()
            if(self.tileSwap == chestTile):
                self.intWin.addAction("(C)hest")
            elif("(C)hest" in self.intWin.stack):
                clearInt = True
            if(self.tileSwap == gold):
                self.intWin.addAction("(G)old")
            elif("(G)old" in self.intWin.stack):
                clearInt = True
            if(self.tileSwap == stairsUp):
                self.intWin.addAction("(U)p Stairs")
            elif("(U)p Stairs" in self.intWin.stack):
                clearInt = True
            if(self.tileSwap == stairsDown):
                self.intWin.addAction("(D)own Stairs")
            elif("(D)own Stairs" in self.intWin.stack):
                clearInt = True 
                
            self.Clock.update() 
            newTime = self.Clock.GetFullTime()
            self.statWin.updateSetTime(newTime) 
            difDay = self.Clock.lastRotday - newTime[0]
            if(difDay >0):
                rottenItems = self.Player.rot(newTime)
                if len(rottenItems) > 1:
                    for item in rottenItems:
                        self.logWin.addMsg((item+" has rotted")) 
                self.Clock.lastRotday = newTime[0]
                    
    def movePlayer(self,dir:int)->int:
        self.player.prevLoc = (self.player.x,self.player.y)
        newCood = [self.player.x,self.player.y]
        match(dir):
            case 12:
                newCood[1] -= 1
            case 3:
                newCood[0] += 1
            case 6:
                newCood[1] += 1
            case 9:
                newCood[0] -= 1
                
        if (0 <= newCood[0] < self.levX and 0 <= newCood[1] < self.levY):
            tile = self.levels[self.currentLevel].map[newCood[1]][newCood[0]]
            if tile is not None and tile.walkable:
                self.player.x = newCood[0]
                self.player.y = newCood[1]
                self.tileSwap = tile
                self.updateKnownTiles()
                self.renderMap()
            
    def genLevel(self,dir:bool):
        #True is going down 
        if(dir):
            self.currentLevel -= 1 
        else:
            self.currentLevel += 1
        
        if(self.currentLevel not in self.levels.keys()):
            self.levels[self.currentLevel] = self.newLevel()

class dStatWin(statWin):
    def __init__(self, x, y, w, h, name, currentMap, Player, time,level):
        self.level = level
        super().__init__(x, y, w, h, name, currentMap, Player, time)
        
    def update(self):
        super().update()
        self.draw_text(0,3,"Level")
        
        self.draw_text(0,4,str(self.level)+"      ")

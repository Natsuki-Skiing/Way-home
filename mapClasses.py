import random 
import math
import sys
from town import *
from dungeon import *
from window import *
from itemManager import *
from clock import *
colourTable = {
    "reset": "\033[0m",
    "green": "\033[32m",
    "gray": "\033[90m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "red": "\033[31m",
    "purple": "\033[95m",           # Bright magenta / purple
    "pink": "\033[38;5;213m",
    "orange": "\033[38;5;208m"
}


class tile:
    def __init__(self,tile:str,walkable:bool,colour:str):
        self.tile = tile 
        self.walkable = walkable 
        self.colour = colourTable[colour]
    def render(self):
        return f"{self.colour}{self.tile}\033[0m"

class door(tile):
    def __init__(open:bool):
        tile = str()
        if(open):
            tile = ";"
        else:
            tile = ":"
            
        super().__init__(tile,open)
        
shrub = tile("♣",True,"green")
moss = tile("░",True,"yellow")
water = tile("≈",False,"blue")
foodTree = tile("♣",True,"red")
flowerYellow = tile("ꕤ",True,"yellow")
flowerPurp = tile("ꕤ",True,"purple")
townTile = tile("T",True,"red")
groundTiles = [moss,shrub,flowerYellow,flowerPurp]
groundTilesWeight = [5,2,1,1]
wall = tile("#",False,"gray")
campsiteTile = tile("C",True,"orange")
playerTile = tile('P',False,"red")
dungeonTile = tile("D",True,"red")
floor = tile(".",True,"green")
class map :
    def __init__(self,x:int,y:int,hasTown:bool,hasDun:bool,town=None,Dungeon=None):
        self.hasWater = False
        self.tilesNextToWater = list()
        self.tiles = dict()
        self.hasTown = hasTown
        self.hasDungeon = hasDun
        hasShrub =False
        #So i can pick one to be a food tree if i wish
        shrubLoctions  = list()
        self.shrubTimerDict = dict()
        self.campFires = dict()
        for h in range(y):
            for w in range(x):
                #Had set to wall originally changed to floor to test movement 
                #I'm not sure of the orinial meaning behind setting them all to wall
                if(random.randint(0,8) == 0):
                    newTile =  random.choices(groundTiles,weights=groundTilesWeight,k=1)[0]
                    if(type(newTile) == type(shrub)):
                        shrubLoctions.append((w,h))
                        
                    self.tiles[(w,h)] = newTile
                else:
                    self.tiles[(w,h)] = floor 
                    
        #Water generation 
        
        if(random.randint(0,2) == 1):
            #Gunna do water 
            strtX = random.randint(0,x-1)
            strtY = random.randint(0,y-1)
            self.hasWater = True
            noWaterCells = random.randint(5,30)
            self.tiles[(strtX,strtY)] = water
            possibleCells = self.coordsInDistance(strtX,strtY,noWaterCells)
            while noWaterCells >0:
                potential = random.choice(possibleCells)
                if(potential[0]> 0 and potential[0]<x-1 and potential[1]> 0 and potential[1]<y-1):
                    offsets = [(-1,0),(1,0),(0,-1),(0,1)]
                    nextToWater = False
                    for offset in offsets:
                        key = ((potential[0] + offset[0]) , (potential[1] + offset[1]))
                        if(self.tiles[key]== water):
                            nextToWater = True 
                            break 
                    if(nextToWater):
                        self.tiles[(potential[0] ,potential[1])] = water 
                        possibleCells.remove(potential)
                        noWaterCells -=1
                        for offset in offsets:
                            pos = (potential[0]+ offset[0],potential[1]+offset[1])
                            if(pos[0]> 0 and pos[0]<x-1 and pos[1]> 0 and pos[1]<y-1):
                                
                                self.tilesNextToWater.append((pos[0],pos[1]))
                else:
                    possibleCells.remove(potential) 
        #Food tree placement
        if(random.randint(0,1)== 1 and len(shrubLoctions) > 0):
            loc = random.choice(shrubLoctions)
            #Tree can pick from
            self.tiles[loc] = foodTree
            self.shrubTimerDict[loc] = [-1,random.randint(1,5)]
            # A rare chance for there to be an extra food tree
            if(random.randint(0,3)==1):
                loc = random.choice(shrubLoctions)
                self.tiles[loc] = foodTree 
                self.shrubTimerDict[loc] = [-1,random.randint(1,5)]
        if(hasTown and town!= None):
            self.town = town
            #Placing the town tile
             
            self.tiles[(random.randint(1,w-1),random.randint(1,h-1))] = townTile 
        if(hasDun and Dungeon != None):
            self.Dungeon = Dungeon 
            self.tiles[(random.randint(1,w-1),random.randint(1,h-1))] = dungeonTile
                
    def nextToWater(self,x:int,y:int)->bool:
        if ((x,y) in self.tilesNextToWater):
            return(True)
        return(False)
    def coordsInDistance(self,x, y, max_d,radius=1):
        coords = []
        for dx in range(-max_d, max_d + 1):
            for dy in range(-max_d, max_d + 1):
                if abs(dx) + abs(dy) <= max_d:  # Use Euclidean here if needed
                    coords.append((x + dx, y + dy))
        return coords      
    def placeCampfire(self,x:int,y:int):
        
        self.tiles[(x,y)] = campsiteTile
            
        
        
            
                
                
                
                
            
            
    

class world:
    def __init__(self,mapX:int,mapY:int):
        self.mapX = mapX
        self.mapY = mapY
        self.rY = mapY -1 
        self.rX = mapX -1
        self.maps = dict()
        self.currentMap = (0,0)
        self.tileSwap = None
        self.lastTileX = 0
        self.lastTileY= 0
        self.GClock = clock(dayMinReal= 3)
        #used for town and dungeon chance generation
        self.sinceTown = 0
        self.sinceDun =0
        self.sideTiles = [wall,floor]
        self.frame = "x" + mapX*"=" +"x"
        self.Window = Window(0,0,mapX,mapY,"Way Home")
    def inBounds(self,x:int,y:int)->bool:
        #Check in bounds of map 
        if(x < 0 or y <0) or (x > self.mapX-1 or y>self.mapY-1):
            return False
        return True 
    def canWalk(self,x:int,y:int)->bool:
        key = (x,y)
        
        return(self.maps[self.currentMap].tiles[key].walkable)
    def worldKey(self,x:int ,y:int) ->tuple:
        return((x,y))
    def sideGen(self,size:int):
        side = list()
        for pos in range(size):
            side.append(random.choice(self.sideTiles))
        return side
    def genMap(self,x:int,y:int,hasTown:bool,hasDun:bool,Town = None,Dungeon = None):
        # This is really ugly might fix but i don't really care to 
        if(hasTown):
            outMap = map(self.mapX,self.mapY,True,False,town= Town)
        elif(hasTown and hasDun):
            outMap = map(self.mapX,self.mapY,True,True,Town,Dungeon)
        elif(hasDun):
            outMap = map(self.mapX,self.mapY,False,True,Dungeon = Dungeon)
        else:   
            outMap = map(self.mapX,self.mapY,False,False)
        mapsToCheck = list()
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in offsets:
            position = self.worldKey(x + dx, y + dy)
            if position in self.maps:
                mapsToCheck.append(position)
            
       
        
        right = False
        left = False 
        down = False
        up = False

        keys = self.maps.keys()
        offset = self.worldKey(x+1,y)
        if offset in keys:
            right = True
            for i in range(self.mapY):
                outMap.tiles[(self.rY ,i)] = self.maps[offset].tiles[(0,i)] 
                
        
        offset = self.worldKey(x-1,y)
        if offset in keys:
            left = True
            for i in range(self.mapY):
                outMap.tiles[(0,i)] = self.maps[offset].tiles[(self.rY,i)]
                
        offset = self.worldKey(x,y-1)
        if offset in keys:
            up = True
            for i in range(self.mapY):
                outMap.tiles[(i,0)] = self.maps[offset].tiles[(self.rX,i)]
                
        offset = self.worldKey(x,y+1)
        if offset in keys:
            down = True
            for i in range(self.mapY):
                outMap.tiles[(i,self.rX)] = self.maps[offset].tiles[(i,0)]
                

        
        
        
        if(not right):
            side = self.sideGen(self.mapY)
            for i in range(self.mapY):
                outMap.tiles[(self.rX,i)] = side[i]
                
        if(not left):
            side = self.sideGen(self.mapY)
            for i in range(self.mapY):
                outMap.tiles[(0,i)] = side[i]
                
        if(not down):
            side = self.sideGen(self.mapX)
            for i in range(self.mapX):
                outMap.tiles[(i,self.rX)] = side[i]
                
        if(not up):
            side = self.sideGen(self.mapX)
            for i in range(self.mapX):
                outMap.tiles[(i,0)] = side[i]

        return(outMap)
    def placePlayer(self,x:int,y:int):
        key = (x,y)
        if(self.tileSwap == None):
            self.tileSwap = self.maps[self.currentMap].tiles[key]
            self.maps[self.currentMap].tiles[key] = playerTile
            self.lastTileX = x
            self.lastTileY = y
        else:
            lastKey = (self.lastTileX ,self.lastTileY)
            self.maps[self.currentMap].tiles[lastKey] = self.tileSwap
            self.lastTileX = x
            self.lastTileY = y
            self.tileSwap = self.maps[self.currentMap].tiles[key] 
            self.maps[self.currentMap].tiles[key] = playerTile
    
    def printAt(self, coords, Tile):
        """
        Print a tile at specified grid‐coords inside the window.
        """
        x, y = coords
        # draw_text already does:  row = self.y+2+y,  col = self.x+2+x
        self.Window.draw_text(x, y, Tile.render())

    def drawOnlyPlayer(self, newLoc, prevLoc):
        # to reduce flickering from redrawing whole map on lower end machines
        sys.stdout.write("\033[s")      # save cursor
        
        tileUnder = self.maps[self.currentMap].tiles[prevLoc]
        self.printAt(prevLoc, tileUnder)

        
        self.printAt(newLoc, playerTile)

        sys.stdout.write("\033[u")      # restore cursor
        sys.stdout.flush()

    
    def drawCurrentMap(self):
        # First, clear the screen for a fresh draw
        #sys.stdout.write("\033[2J\033[H")
        self.Window.clear()
        # Draw the entire map
        
        tile_map = self.maps[self.currentMap].tiles
        
        for h in range(self.mapY):
            row = ["|"]
            for w in range(self.mapX):
                tile = tile_map.get((w, h))
                if tile:
                    row.append(tile.render())
                else:
                    row.append(" ") 
            row.append("|")
            self.Window.draw_text(-1,h,("".join(row)))
        
        # Ensure output is flushed to the terminal
       
        sys.stdout.flush()
    def placeCampfire(self,x:int,y:int)->bool:
        returnValue = False 
        forbiddenTiles = ["T","C","D","≈","♣"]
        if self.tileSwap.tile not in forbiddenTiles:
            self.tileSwap = campsiteTile 
            self.maps[self.currentMap].placeCampfire(x,y)
            returnValue = True
        return(returnValue)
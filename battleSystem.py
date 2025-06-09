from healthBar import healthBar 
from creature import creature
import time 
import readchar
import random
from window import Window
from player import player
from clear import clear
from opp import opp
from itemMaker import *
from creatureManager import *
from selectMenu import *
import math 
from items import *

class itemWindow(Window):
    def __init__(self, x, y, w, h,playerItems:list):
        super().__init__(x, y, w, h, "Consumables")
        self.items = []
        self.itemNames = []
        for item in playerItems:
            if(type(item) == fish or type(item) == potion ):
                self.items.append(item)
                self.itemNames.append(item.name)
        self.menu = arrowMenu(self.itemNames,h)
    def mainLoop(self)->item:
        running = True 
        while running:
            self.row_draw(self.menu.renderList())
            selected = self.menu.mainLoop()
            if type(selected) == int:
                if selected >= 0: 
                    #index = self.menu.selected
                    return(self.items[selected])
        
class logWin(Window):
    def __init__(self, x, y, w, h, name=None):
        super().__init__(x, y, w, h, name)
        self.lines = list()
    def addMsg(self,msg:str):
        newList = list()
        if (len(msg) > self.w):
            #TODO
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
        counter = self.h-1
        for line in self.lines:
            self.draw_text(0,counter,(">"+line))
            counter -=1
class battleWindow(Window):
    def __init__(self, x, y, w, h,target:creature):
        self.target = target
        super().__init__(x, y, w, h, self.target.name)
        self.bar = healthBar(self.target,45)
        self.update()
    def update(self):
        self.bar.update()
        self.clear()
        rows = ["",self.bar.render(),"Hp: "+str(self.target.hp)+" / "+str(self.target.maxHp),"","Level: "+str(self.target.level)]
        self.row_draw(rows)
        pass
class battleSystem:
    def __init__(self,Player:player,creatureMan:creatureManager,distanceFromStart:int,run:bool = True):
        clear()
        self.run = run
        # This also indicates if in a dungeon as in a dungeon you cannot run
        self.player = Player
        self.oppClass = 1
        self.opp = self.getCreature(creatureMan,distanceFromStart)
        self.playerBar = healthBar(Player,20)
        
        self.titleWin = Window(0,0,50,1)
        self.oppWin = battleWindow(0,self.titleWin.h+2,self.titleWin.w,5,self.opp)
        self.playerWin = battleWindow(0,self.oppWin.h+self.titleWin.h+4,self.titleWin.w,5,Player)
        self.titleWin.draw_text(17,0,"ENEMY ENCOUNTER")
        self.oppBar = healthBar(self.opp,20)
        self.oppMissMsg = ["Thanks the gods!","You were too swift","Close Shave!","The strike finds nothing but air","Their effort ends in vain","Nice one"]
        self.attackMsg =["That must hurt!","It'll leave as scar","Ouch!","Good show!","It screams in pain","It would take a lot of potions to heal that","That was a perfect strike"]
        self.actionWin = Window(0,
                                self.titleWin.h+self.oppWin.h+self.playerWin.h+6,
                                self.titleWin.w,
                                6,
                                "Actions")
        self.battleLog = logWin(self.titleWin.w+2,0,40,self.titleWin.h+self.oppWin.h+self.playerWin.h+self.actionWin.h+6,"Combat Log")
        
        self.mainActions = ["(A)ttack","(I)tems"]
        self.attackActions = ["(H)ead ~50%","(B)ody ~75%"]
        self.mainAcRun =  ["(A)ttack","(I)tems","(R)un"]
        self.state = "main"
        
        #Creature with higher level goes first 
        if (Player.level == self.opp.level):
            playerFirst = bool(random.getrandbits(1))
        else:
            playerFirst = (Player.level > self.opp.level)
        
        self.mainLoop(playerFirst)
    def getCreature(self,creatureMan:creatureManager,distanceFromStart:int)->opp:
        if self.player.level < 5:
            self.oppClass = random.randint(1,2)
        elif self.player.level < 10:
            self.oppClass = random.randint(1,3)
        elif self.player.level <20:
            self.oppClass = random.randint(1,7)
        else :
            self.oppClass = random.randint(1,10)
        if self.run:
            level = int(self.calcCreatureLevel(distanceFromStart))
        else:
            level = int(self.calcCreatureLevel(distanceFromStart)*1.65)
            
        Creature = creatureMan.getOpp(self.oppClass,level)
        return(Creature)
    def calcCreatureLevel(self,distance:int)->float:
        DWeight = 0.80
        PLWeight = 0.75 
        
        return(max((DWeight*distance)+(self.player.level*PLWeight),1)+random.randint(0,1))
    def mainState(self):
        self.actionWin.clear() 
        if self.run :
            self.actionWin.row_draw(self.mainAcRun)
        else:
            
            self.actionWin.row_draw(self.mainActions)
        running = True 
        while running:
            
            match(readchar.readkey()):
                case 'a':
                    self.state = "attack"
                    running = False
                    pass 
                case 'i':
                    # Menu for consumables 
                    if(any(isinstance(item, (fish,potion)) for item in self.player.items)):
                        running = False
                        itemWin = itemWindow(self.battleLog.x+self.battleLog.w+2,0,20,self.battleLog.h,self.player.items)
                        Item = itemWin.mainLoop()
                        self.battleLog.addMsg(self.player.name+" uses "+Item.name )
                        if type(Item) == fish:
                            self.battleLog.addMsg(self.player.name+" gains "+str(Item.hp)+" hp")
                            self.player.addHp(Item.hp)
                        self.player.items.remove(Item)
                        itemWin.remove()
                    else:
                        self.battleLog.addMsg("No consumables in inv")
                    #self.state ="main"
                    
                case 'r':
                    if(self.run):
                        #TODO
                        #Might add chance to run but for now just allow 
                        self.state = "run"
                        running = False
    def attackState(self):
        self.actionWin.clear()
        self.actionWin.row_draw(self.attackActions)
        running = True 
        while running:
            
            match(readchar.readkey()):
                case "h":
                    self.attackHead()
                    running = False
                case "b":
                    self.attackBody()
                    running = False 
            self.state = "main"
    def oppAttack(self):
        #TODO
        #Just a simple chance could change
        if(random.randint(1,10)>=5):
            playerDef = self.player.defense
            if(self.player.equiptItems["armour"] != None):
                playerDef += self.player.equiptItems["armour"].protection 
            if(self.player.equiptItems["helmet"] != None):
                playerDef += self.player.equiptItems["helmet"].protection 
            pass
            #Experimental extra dam,critial hit 
            extraDam = 0
            if(random.randint(0,4)==1):
                extraDam = random.randint(1,self.oppClass)
                self.battleLog.addMsg(self.opp.name+" makes a critial attack")
            realDam = (self.opp.attack+extraDam) -playerDef 
            if realDam <= 0:
                self.battleLog.addMsg("It does no damage") 
            else:
                   
                self.player.hp -= realDam 
                self.battleLog.addMsg(self.opp.name+" does "+str(realDam)+" damage")
            
        else:
            self.battleLog.addMsg("It missed!")
            self.battleLog.addMsg(random.choice(self.oppMissMsg))
    def mainLoop(self,playersTurn):
        running = True
        while running:
            if playersTurn:
                self.battleLog.addMsg(">"+self.player.name+"'s turn")
                
                if self.state == "main":
                    self.mainState()
                if self.state == "attack":
                    self.attackState()
                if self.state == "run":
                    #TODO 
                    #This is gross need to fix or not idc this isn't graded work
                    running = False
                    return()
                pass
            else:
                pass
                self.battleLog.addMsg(">"+self.opp.name+"'s turn")
                
                #TODO 
                # Opp attack fo now will do simple want to add other actions
                self.battleLog.addMsg(self.opp.name+" Attacks!")
                self.oppAttack()
            #Changing turns
            playersTurn = not playersTurn
            self.playerWin.update()
            self.oppWin.update()
            self.playerWin.update()
            if(self.player.hp<=0):
                #TODO 
                #Player is dead not sure what to do rn
                pass
            elif(self.opp.hp <=0):
                #opp is dead 
                # calculate the xp for the player 
                xp = self.genXp()
                self.battleLog.addMsg("You killed the "+self.opp.name)
                if(random.randint(0,2)==0):
                    gold = random.randint(1,5)
                    self.battleLog.addMsg("Picked up "+str(gold)+" gold")
                    self.player.gold += gold
                self.battleLog.addMsg("Gained "+str(xp)+" Xp")
                
                self.player.addXp(xp)
                running = False 
        if(self.state == "run"):
            return()
        time.sleep(4)
    def genXp(self) -> int:
        
        lvl_p = self.player.level
        lvl_e = self.opp.level

        # Base XP is proportional to the enemy's level
        base_xp = (lvl_e * 10)

        # Positive diff = harder fight -> bonus XP; negative = easier -> reduced XP
        diff = lvl_e - lvl_p

        # Exponential scaling: 1.1**diff
        if(self.oppClass <=3):
            scale = 1.1
        elif(self.oppClass <=6):
            scale = 1.3
        elif(self.oppClass <=8):
            scale = 1.5
        else: 
            scale = 2
        xp_gain = int(base_xp * (scale ** diff))

        # Guarantee at least 1 XP
        xp_gain = max(1, xp_gain) 
        if not self.run:
            xp_gain = math.ceil(xp_gain*1.5)

        # Award it
        

        return xp_gain
    def attackMenu(self):
        if self.equiptItems["weapon"] != None:
            done = False
            while(not done):
                choice = str(input(">")).lower()
                match(choice):
                    
                    case _:
                        print("Invalid selection!")
                        time.sleep(1)
        else:
            clear()
            print("No weapon equipt !") 
            
    def getAttackMsg(self)->str:
        return(random.choice(self.attackMsg))
        pass 
    
    def attackHead(self):
        
        if(random.randint(0,1)== 1):
            self.attack(True)
        else:
            self.battleLog.addMsg(("You miss the "+self.opp.name))
        pass
    def attackBody(self):
        
        if(random.randint(1,75)<= 75):
            self.attack()
        else:
            
            self.battleLog.addMsg("You Missed the " + self.opp.name)
        pass
    def attack(self,head = False):
        Weapon = self.player.equiptItems["weapon"]
        
        if(head):
            damage = (int(Weapon.damage*2)+self.player.attack) - self.opp.defense
            
        else:
            damage = (Weapon.damage+self.player.attack) - self.opp.defense
        
        if(damage >= 0):
            self.opp.hp -= damage
            self.battleLog.addMsg("Hit "+self.opp.name+" for "+str(damage)+" hp")
            self.battleLog.addMsg(self.getAttackMsg())
        else:
            self.battleLog.addMsg("You failed to hurt the "+self.opp.name) 
            
#DEBUG          
# testOpp = opp("Ill Rat",5,10,5,2)
# testPlayer = player("Joe Biden")
# testBattle = battleSystem(testPlayer,testOpp)
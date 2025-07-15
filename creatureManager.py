from itemManager import * 
from opp import * 
import random ,copy
class creatureManager():
    def __init__(self, folder,fileName:str):
        self.folder = folder +'/'
        self.file = fileName
        self.AllOpps = {1:list(),2:list(),3:list(),4:list(),5:list(),6:list(),7:list(),8:list(),9:list(),10:list()}
        self.populateDict()
    def populateDict(self):
        with open(self.folder+self.file+".json") as f:
            raw = json.load(f)  
            
        for entry in raw:
            
            self.AllOpps[entry["class"]].append(opp(entry["name"],entry["baseHp"],entry["baseDef"],entry["baseAttack"],entry["class"])) 
    def getOpp(self,Oppclass:int,OppLevel:int)->opp:
        baseOpp =  copy.deepcopy(random.choice(self.AllOpps[Oppclass]))
        baseOpp.scaleForLevel(OppLevel)
        return(baseOpp)
            
import time

class clock:
    def __init__(self,dayMinReal:int = 30,strtDay:int= 0):
        self.day = strtDay 
        self.lastStamp = time.time()
        self.time = [9,0]
        self.convert = dayMinReal 
        self.secPerMin= (dayMinReal * 60) / (24 * 60)
        self.lastRotday = 0
    def update(self)->int:
        newStamp = time.time()
        diff = newStamp - self.lastStamp 
        self.lastStamp = newStamp 
        
        noMin = self.secPerMin * diff 
        totMin = int(noMin+ self.time[1]) 
        
        newHours , self.time[1] = divmod(totMin,60)
        self.time[0] += newHours 
        
        dayInc ,self.time[0] = divmod(self.time[0],24) 
        self.day += dayInc 
    def GetFullTime(self) ->list[int]:
        return [self.day , self.time[0],self.time[1]]
    
        
        
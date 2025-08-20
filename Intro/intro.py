from clear import * 
from window import *
import time
class introSeq():
    def __init__(self,textLocation = "Intro/introText.txt"):
        self.fileLoc = textLocation
        self.h = 30
        self.introWindow = Window(0,0,50,self.h,"Introduction")
        self.linesPrinted = []
        with open(self.fileLoc, "r") as f:
            self.lines = f.readlines()
    def start(self):
        
        index = 1 
        noLines = len(self.lines)
        while index < noLines:
            self.addLine(self.lines[index])
            index+=1
            time.sleep(2)
        time.sleep(1)
        #self.h =0
        self.addLine("Press enter to continue")
        input("")
    def addLine(self,line:str):
        if len(self.linesPrinted) >= self.h:
            self.linesPrinted = []
        self.linesPrinted.append(line)
        self.introWindow.clear()
        self.introWindow.row_draw(self.linesPrinted)
        
        pass
    

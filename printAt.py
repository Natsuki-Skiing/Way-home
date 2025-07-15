import sys 

def printAt(x:int,y:int,text:str):
    sys.stdout.write(f"\033[{y};{x}H{text}")
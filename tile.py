import os
import sys
colourTable = {
    "reset": "\033[0m",
    "green": "\033[32m",
    "gray": "\033[90m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "red": "\033[31m",
    "purple": "\033[95m",           # Bright magenta / purple
    "pink": "\033[38;5;213m" 
}
class tile:
    def __init__(self,tile:str,walkable:bool,colour:str):
        self.tile = tile 
        self.walkable = walkable 
        self.colour = colourTable[colour]
    def render(self):
        return f"{self.colour}{self.tile}\033[0m"
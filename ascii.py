import random
import sys
from clear import *
class ascii:
    def __init__(self):
        self.font = {
            'a': [
                " ██████    ",
                " ██    ██   ",
                "██      ██  ",
                "██████████  ",
                "██      ██  ",
                "██      ██  "
            ],
            'b': [
                "██████████  ",
                "██      ██  ",
                "██████████  ",
                "██████████  ",
                "██      ██  ",
                "██████████  "
            ],
            'c': [
                " ██████████  ",
                "██        █  ",
                "██           ",
                "██           ",
                "██        █  ",
                " ██████████  "
            ],
            'd': [
                "████████    ",
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                "████████    "
            ],
            'e': [
                "██████████  ",
                "██          ",
                "██████████  ",
                "██████████  ",
                "██          ",
                "██████████  "
            ],
            'f': [
                "██████████  ",
                "██          ",
                "██████████  ",
                "██████████  ",
                "██          ",
                "██          "
            ],
            'g': [
                " ██████████  ",
                "██        █  ",
                "██           ",
                "██ ██████    ",
                "██      ██   ",
                " ██████████  "
            ],
            'h': [
                "██      ██  ",
                "██      ██  ",
                "██████████  ",
                "██████████  ",
                "██      ██  ",
                "██      ██  "
            ],
            'i': [
                "██████████  ",
                "    ██      ",
                "    ██      ",
                "    ██      ",
                "    ██      ",
                "██████████  "
            ],
            'j': [
                "██████████  ",
                "      ██    ",
                "      ██    ",
                "      ██    ",
                "██    ██    ",
                "██████████  "
            ],
            'k': [
                "██    ██    ",
                "██  ██      ",
                "████        ",
                "████        ",
                "██  ██      ",
                "██    ██    "
            ],
            'l': [
                "██          ",
                "██          ",
                "██          ",
                "██          ",
                "██          ",
                "██████████  "
            ],
            'm': [
                "██      ██  ",
                "████  ████  ",
                "██  ██  ██  ",
                "██  ██  ██  ",
                "██      ██  ",
                "██      ██  "
            ],
            'n': [
                "██      ██  ",
                "███    ██  ",
                "██ ██  ██  ",
                "██  ██ ██  ",
                "██    ███  ",
                "██      ██  "
            ],
            'o': [
                " ████████   ",
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                " ████████   "
            ],
            'p': [
                "██████████  ",
                "██      ██  ",
                "██████████  ",
                "██          ",
                "██          ",
                "██          "
            ],
            'q': [
                " ████████   ",
                "██      ██  ",
                "██      ██  ",
                "██  ██ ██  ",
                "██    ███  ",
                " ████████  "
            ],
            'r': [
                "██████████  ",
                "██      ██  ",
                "██████████  ",
                "██  ██      ",
                "██    ██    ",
                "██      ██  "
            ],
            's': [
                " ██████████  ",
                "██           ",
                " ████████    ",
                "        ███  ",
                "         ██  ",
                "██████████   "
            ],
            't': [
                "██████████  ",
                "    ██      ",
                "    ██      ",
                "    ██      ",
                "    ██      ",
                "    ██      "
            ],
            'u': [
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                " ████████   "
            ],
            'v': [
                "██      ██  ",
                "██      ██  ",
                "██      ██  ",
                " ██    ██   ",
                "  ██  ██    ",
                "   ████     "
            ],
            'w': [
                "██      ██  ",
                "██      ██  ",
                "██  ██  ██  ",
                "██  ██  ██  ",
                "████  ████  ",
                "██      ██  "
            ],
            'x': [
                "██      ██  ",
                " ██    ██   ",
                "  ██  ██    ",
                "  ██  ██    ",
                " ██    ██   ",
                "██      ██  "
            ],
            'y': [
                "██      ██  ",
                " ██    ██   ",
                "  ██  ██    ",
                "   ████     ",
                "    ██      ",
                "    ██      "
            ],
            'z': [
                "██████████  ",
                "      ██    ",
                "    ██      ",
                "  ██        ",
                "██          ",
                "██████████  "
            ],
            ' ': [
                "            ",
                "            ",
                "            ",
                "            ",
                "            ",
                "            "
            ]
        }
        self.colors = { 
            "red": "\033[91m",
            "green": "\033[92m",
            "blue": "\033[94m",
            "yellow": "\033[93m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "grey": "\033[90m",
            "reset": "\033[0m"
        }

    def convertToAscii(self, textInput: str, textColor: str) -> list[str]: 
        # Choose color
        if textColor.lower() in self.colors.keys(): 
            chosenColor = self.colors[textColor.lower()]
        elif textColor.lower() in ["rand", "random", "r"]:
            chosenColor = self.colors[random.choice(list(self.colors.keys()))]
        else:
            chosenColor = self.colors["grey"]

        # Get the ASCII art for each character
        charArt = [] 
        for char in textInput.lower(): 
            if char in self.font:
                charArt.append(self.font[char])
            else:
                
                charArt.append(self.font[' '])

        #
        combinedTextRows = [] 
        for zippedRows in zip(*charArt): 
            # Join the individual character rows to form a full line of text
            fullLineText = "".join(zippedRows) 
            combinedTextRows.append(chosenColor + fullLineText + self.colors["reset"]) #

        return combinedTextRows

    def draw(self,coord:tuple, text:str,colour:str): # Re-added the draw function
        asciiText = self.convertToAscii(text,colour)
        counter = coord[1]
        for line in asciiText:
            counter +=1
            sys.stdout.write(f"\033[{counter};{coord[0]}H{line}")
            
            





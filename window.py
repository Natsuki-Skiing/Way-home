import os
import sys
import time

class Window:
    def __init__(self, x: int, y: int, w: int, h: int, name=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name

        
        self._compute_borders()
        
        # Draw the window without clearing entire screen
        self.draw()
        self.buffer = [[" " for _ in range(w)] for _ in range(h)]
    def _compute_borders(self):
        # Base border
        border = 'x' + '=' * self.w + 'x'
        # Create top border with optional title
        if self.name:
            title = f' {self.name} '
            if len(title) > self.w:
                raise ValueError("Name too long for window width")
            padding = self.w - len(title)
            left = padding // 2
            right = padding - left
            self.top_border = 'x' + '=' * left + title + '=' * right + 'x'
        else:
            self.top_border = border
       
        self.side_border = '|' + ' ' * self.w + '|'
        self.bottom_border = border

    def draw(self):
       
        top_row = self.y + 1
        left_col = self.x + 1
        # Draw top border
        sys.stdout.write(f"\033[{top_row};{left_col}H{self.top_border}")
        # Draw body
        for i in range(self.h):
            sys.stdout.write(f"\033[{top_row + 1 + i};{left_col}H{self.side_border}")
        # Draw bottom border
        sys.stdout.write(f"\033[{top_row + self.h + 1};{left_col}H{self.bottom_border}")
        sys.stdout.flush()
    def remove(self):
        totalHeight = self.h + 2
        totalWidth = self.w + 2
        
        for i in range(totalHeight):
            row = self.y + 1 + i
            col = self.x + 1
            sys.stdout.write(f"\033[{row};{col}H{' ' * totalWidth}")
        
        sys.stdout.flush()
        
    def clear(self):
    
        for i in range(self.h):
            row = self.y + 2 + i  
            col = self.x + 2      
            sys.stdout.write(f"\033[{row};{col}H{' ' * self.w}")
        sys.stdout.flush()

    def draw_text(self, x: int, y: int, text: str):
        # Validate coordinates and text length
        
        
        # Calculate position inside window (accounting for borders)
        row = self.y + 2 + y
        col = self.x + 2 + x
        sys.stdout.write("\033[s")  # save cursor
        sys.stdout.write(f"\033[{row};{col}H{text}")
        sys.stdout.write("\033[u")  # restore cursor
        sys.stdout.flush()
    # Pass a list of strings , one for each row    
    def row_draw(self,rowList,startY:int = 0):
        pos = startY 
        for row in rowList:
            self.draw_text(0,pos,row)
            pos +=1
    def refresh(self):
        
        sys.stdout.flush() 
    def updateName(self,name:str):
        self.name = name
        self._compute_borders()
        self.draw()
# Utility to clear full screen at start (cross-platform)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')



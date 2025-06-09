from item import book
import readchar
import os
class bookReader:
    def __init__(self,Book:book):
        self.Book = book 
        self.pages = dict() 
        size = os.get_terminal_size()
        self.width = size.columns -10
        self.height = size.lines - 10 
        
        self.pageSize = self.height * self.width
        
    def loadPage(self,pageNumber:int):
        if pageNumber in self.pages.keys():
            return(self.pages[pageNumber])
        else:
            try:
                file = open(self.Book.path,'r')
                file.seek(pageNumber * self.pageSize)
                
            except:
                pass
            
    def main(self):
        
        pass 
    

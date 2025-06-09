import threading
import playsound3
from playsound3 import playsound
import os
import random
class musicPlayer:
    def __init__(self,folder:str):
        self.dir = folder 
        self.songs = os.listdir(self.dir)
        self.soundQueue = self.songs 
        if '.DS_Store' in self.songs:
            self.songs.remove('.DS_Store')
        self.thread = threading.Thread(target =self.main)
        self.playingSong = random.choice(self.songs)
        
    def main(self):
        temp = self.playingSong
        self.playingSong = random.choice(self.soundQueue)
        self.soundQueue.append(temp)
        self.soundQueue.remove(self.playingSong)
        playsound(self.dir +self.playingSong) 
    def start(self):
        self.thread.start()

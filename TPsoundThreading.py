import threading
import time

import pyaudio  
import wave  
#Reference: https://people.csail.mit.edu/hubert/pyaudio/docs/
class soundThread(threading.Thread):

    def __init__(self, songName):
        threading.Thread.__init__(self) #thread class is the super class
        self.finished = False
        self.chunk = 128 
        self.nature = r"/Users/prachimahableshwarkar/Desktop/TP Sounds/nature.wav"
        self.classical = r"/Users/prachimahableshwarkar/Desktop/TP Sounds/classical.wav"
        self.crowd = r"/Users/prachimahableshwarkar/Desktop/TP Sounds/crowd.wav"
        self.songName = songName

    def run(self):
        slept = 10
        while(True):
            if self.finished == True:
                #print('need to skip')
                break
            #print('sleeping...', slept)
            if self.songName == "classical":
                f = wave.open(self.classical, "rb")
            elif self.songName == "nature":
                f = wave.open(self.nature, "rb")
            elif self.songName == "crowd":
                f = wave.open(self.crowd, "rb")
            p = pyaudio.PyAudio()
            stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                            channels = f.getnchannels(),  
                            rate = f.getframerate(),  
                            output = True)  
            data = f.readframes(self.chunk)  
            while data:
                if self.finished == True:
                    stream.stop_stream()  
                    stream.close()  
                    p.terminate() 
                    break
                stream.write(data)
                data = f.readframes(self.chunk)

    def setSongName():
        pass

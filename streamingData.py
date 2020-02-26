
from tkinter import *
import pyaudio  
import wave 

import gameTPTEST

from TGC import TGC #TGC is the classs and tgc is the file

import threading

# https://pymotw.com/3/threading/
# python - Running a Tkinter form in a separate thread - Stack Overflow
# http://stackoverflow.com/questions/10556479/running-a-tkinter-form-in-a-separate-thread

def callTGC():
	myTGC = TGC()
	myTGC.connect()
	myTGC.readData()

def callGame():
	gameTPTEST.main()

task1 = threading.Thread(target = callTGC)
task1.start()

callGame()

task1.join()




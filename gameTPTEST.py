
from tkinter import *
import pyaudio  
import wave 


#from TGC import TGC
from TPsoundThreading import soundThread

import urllib.request
import base64
#Reference: http://www.cs.cmu.edu/~112/notes/imagesDemo2.py

from timeit import default_timer as timer
#Reference: https://docs.python.org/2/library/time.html

####################################
# init
####################################

def init(data):
    # There is only one init, not one-per-mode
    data.mode = "splashScreen"
    data.time = 50
    data.count1 = 0
    data.count2 = 0
    b1 = Button(data.root, text="Play", command=lambda:onButton(data,1))
    b1.pack()

    data.stage = 0

    data.sound1_stage1_score = 0
    data.sound1_stage2_score = 0
    data.sound1_stage3_score = 0
    data.sound1_meanScore = 0

    data.sound2_stage1_score = 0
    data.sound2_stage2_score = 0
    data.sound2_stage3_score = 0
    data.sound2_meanScore = 0

    data.sound3_stage1_score = 0
    data.sound3_stage2_score = 0
    data.sound3_stage3_score = 0
    data.sound3_meanScore = 0

    data.splashscreen_url = "http://www.revradiotowerofsong.org/images/400_music_on_the_brain.gif"
    data.splashscreen_image = loadImageFromWeb(data.splashscreen_url)
    
    data.classical_url = "http://images.clipartpanda.com/musical-notes-gif-3d-music-notes.gif"
    data.classical_image = loadImageFromWeb(data.classical_url)

    #data.nature_url = "http://www.capetribfarmstay.com/images/rainforest.gif"
    data.nature_url = "http://www.lovethisgif.com/uploaded_images/56449-Paisajes-Animados-Gifs-Instantes.gif"
    data.nature_image = loadImageFromWeb(data.nature_url)

    data.crowd_url = "http://zippy.gfycat.com/MatureLegitimateBluebottle.gif"
    data.crowd_image = loadImageFromWeb(data.crowd_url)

    data.reveal_url = "https://s-media-cache-ak0.pinimg.com/originals/2f/75/ca/2f75ca4aef31dc772d50447c75ff91cb.gif"
    data.reveal_image = loadImageFromWeb(data.reveal_url)

    data.songName = None
    data.song1 = None
    data.song2 = None
    data.song3 = None


####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   playGameMousePressed(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)

####################################
# splashScreen mode
####################################

def button1Pressed(data):
    data.mode = "playGame"

def button2Pressed(data):
    data.mode = "help"



def onButton(data, buttonId):
    if (buttonId == 1): button1Pressed(data)
    elif (buttonId == 2): button2Pressed(data)


def splashScreenMousePressed(event, data):
    pass

def splashScreenKeyPressed(event, data):
    if data.mode == "splashScreen":
        data.mode = "Stroop Test"
    if data.mode == "Stroop Test":
        data.mode = "playGame"
        data.stage = 0

def splashScreenTimerFired(data):
    pass

def readUrl(splashscreen_url):
    with urllib.request.urlopen(splashscreen_url) as response:
       return response.read()

def loadImageFromWeb(splashscreen_url):
    assert(splashscreen_url.endswith(".gif")) # only works for gif's!
    return PhotoImage(data=base64.encodebytes(readUrl(splashscreen_url)))

def productivePitches(canvas, data):
    # Draw a background rectangle to highlight the transparency
    # of the images
    canvas.create_rectangle(0, 10, data.width, 190, fill="cyan")
    # Draw the demo info
    font = ("Arial", 16, "bold")

    # Draw the original size image on the left
    imageSize = ( (data.splashscreen_image.width(), data.splashscreen_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.splashscreen_image)
    canvas.create_text(data.width//2, data.height//2, text = "Productive Pitches", 
                       font = "Times 37 bold")
    canvas.create_text(data.width//2, data.height//2 + 100, text = "Press play to find out at what background",
                       font = "Helvetica 15 italic bold", fill = "white")
    canvas.create_text(data.width//2, data.height//2 + 120, text = " noise you are most productive!",
                       font = "Helvetica 15 italic bold", fill = "white")

# def stroopTest(canvas, data):
#   canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
#   canvas.create_text(data.width/2, data.height/2-20,
#                      text="Stroop Test", font="Arial 26 bold")
#   canvas.create_text(data.width/2, data.height/2+20,
#                      text="Press any key to play!", font="Arial 20")

def splashScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,300,300,fill="cyan")
    # print counts
    msg = "Play: " + str(data.count1)
    canvas.create_text(150,130,text=msg)
    msg = "Help: " + str(data.count2)
    canvas.create_text(150,170,text=msg)
    if data.mode == "splashScreen":
        productivePitches(canvas, data)
    if data.mode == "Stroop Test":
        stroopTest(canvas, data)

    

####################################
# help mode
####################################

def helpMousePressed(event, data):
    pass

def helpKeyPressed(event, data):
    data.mode = "playGame"

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    pass
    #help mode should have stroop game instruction reminders 


####################################
# playGame mode
####################################

def withinCircle(data, clickX, clickY):
    if data.stage == 1:
        #red
        cornerx = 15
        cornery = 142
        width = 24
        height = 13
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound1_stage1_score += 1
            print("red")

        #green
        cornerx2 = 131
        cornery2 = 82
        width2 = 37
        height2 = 17
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound1_stage1_score += 1
            print("green")
            

        #blue
        cornerx3 = 258
        cornery3 = 168
        width3 = 30
        height3 = 20
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound1_stage1_score += 1
            print("blue")

    if data.stage == 2:
        #pink
        cornerx = 15
        cornery = 108
        width = 24
        height = 22
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound1_stage2_score += 1
            print("pink")

        #green
        cornerx2 = 132
        cornery2 = 79
        width2 = 37
        height2 = 20
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound1_stage2_score += 1
            print("green")
            

        #orange
        cornerx3 = 253
        cornery3 = 168
        width3 = 43
        height3 = 20
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound1_stage2_score += 1
            print("orange")

    if data.stage == 3:
        #green
        cornerx = 13
        cornery = 108
        width = 29
        height = 23
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound1_stage3_score += 1
            print("green")

        #red
        cornerx2 = 132
        cornery2 = 168
        width2 = 40
        height2 = 22
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound1_stage3_score += 1
            print("red")
            

        #orange
        cornerx3 = 255
        cornery3 = 138
        width3 = 38
        height3 = 22
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound1_stage3_score += 1
            print("orange")

        ## sound 2 ##

    if data.stage == 5:
        #red
        cornerx = 15
        cornery = 142
        width = 24
        height = 13
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound2_stage1_score += 1
            print("red")

        #green
        cornerx2 = 131
        cornery2 = 82
        width2 = 37
        height2 = 17
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound2_stage1_score += 1
            print("green")
            

        #blue
        cornerx3 = 258
        cornery3 = 168
        width3 = 30
        height3 = 20
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound2_stage1_score += 1
            print("blue")

    if data.stage == 6:
        #pink
        cornerx = 15
        cornery = 108
        width = 24
        height = 22
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound2_stage2_score += 1
            print("pink")

        #green
        cornerx2 = 132
        cornery2 = 79
        width2 = 37
        height2 = 20
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound2_stage2_score += 1
            print("green")
            

        #orange
        cornerx3 = 253
        cornery3 = 168
        width3 = 43
        height3 = 20
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound2_stage2_score += 1
            print("orange")

    if data.stage == 7:
        #green
        cornerx = 13
        cornery = 108
        width = 29
        height = 23
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound2_stage3_score += 1
            print("green")

        #red
        cornerx2 = 132
        cornery2 = 168
        width2 = 40
        height2 = 22
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound2_stage3_score += 1
            print("red")
            

        #orange
        cornerx3 = 255
        cornery3 = 138
        width3 = 38
        height3 = 22
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound2_stage3_score += 1
            print("orange")

    ## sound 3 ##

    if data.stage == 9:
        #red
        cornerx = 15
        cornery = 142
        width = 24
        height = 13
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound3_stage1_score += 1
            print("red")

        #green
        cornerx2 = 131
        cornery2 = 82
        width2 = 37
        height2 = 17
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound3_stage1_score += 1
            print("green")
            

        #blue
        cornerx3 = 258
        cornery3 = 168
        width3 = 30
        height3 = 20
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound3_stage1_score += 1
            print("blue")

    if data.stage == 10:
        #pink
        cornerx = 15
        cornery = 108
        width = 24
        height = 22
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound3_stage2_score += 1
            print("pink")

        #green
        cornerx2 = 132
        cornery2 = 79
        width2 = 37
        height2 = 20
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound3_stage2_score += 1
            print("green")
            

        #orange
        cornerx3 = 253
        cornery3 = 168
        width3 = 43
        height3 = 20
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound3_stage2_score += 1
            print("orange")

    if data.stage == 11:
        #green
        cornerx = 13
        cornery = 108
        width = 29
        height = 23
        if (cornerx <= clickX <= cornerx + width and
            cornery <= clickY <= cornery + height) == True:
            data.sound3_stage3_score += 1
            print("green")

        #red
        cornerx2 = 132
        cornery2 = 168
        width2 = 40
        height2 = 22
        if (cornerx2 <= clickX <= cornerx2 + width2 and
            cornery2 <= clickY <= cornery2 + height2) == True:
            data.sound3_stage3_score += 1
            print("red")
            

        #orange
        cornerx3 = 255
        cornery3 = 138
        width3 = 38
        height3 = 22
        if (cornerx3 <= clickX <= cornerx3 + width3 and
            cornery3 <= clickY <= cornery3 + height3) == True:
            data.sound3_stage3_score += 1
            print("orange")

def playGameMousePressed(event, data):
    if data.time > 0:
        if data.stage == 1:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 2:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 3:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 5:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 6:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 7:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 9:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 10:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
        if data.stage == 11:
            if withinCircle(data, event.x, event.y) == True:
                print("yes")
    if data.stage == 4:
        exec(open("graphClassical.py").read())
    if data.stage == 8:
        exec(open("graphNature.py").read())
    if data.stage == 12:
        exec(open("graphCrowd.py").read())
    if data.stage == 12.5:
        data.stage = 14
    if data.stage == 14:
        exec(open("graphOverall.py").read())
        


def playGameKeyPressed(event, data):
    if data.stage == 0:
        if event.char == "s":
            data.stage = 0.5
    if data.stage == 0.5:
        if event.char == "s":
            data.stage = 1
            data.time = 50

            #start sound 1
            data.songName = "classical"
            data.song1 = soundThread(data.songName)
            data.song1.start()

    if data.stage == 1:
        #callTGC()
        if data.time == 0 and event.keysym == "2":
            data.stage = 1.5
            data.time = 50
    if data.stage == 1.5:
        if event.char == "s":
            data.stage = 2
            data.time = 50
    if data.stage == 2:
        # callTGC()
        if data.time == 0 and event.keysym == "3":
            data.stage = 2.5
            data.time = 50
    if data.stage == 2.5:
        if event.char == "s":
            data.stage = 3
    if data.stage == 3:
        # callTGC()
        if data.time == 0 and event.keysym == "r":
            data.stage = 4
            #stop sound 1
            data.song1.finished = True
    if data.stage == 4:
        if event.keysym == "c":
            data.stage = 4.5 #instructions for stage 5

        ## sound 2 ##
    if data.stage == 4.5:
        if event.keysym == "s":
            data.stage = 5
            data.time = 50

            #start sound 2
            data.songName = "nature"
            data.song2 = soundThread(data.songName)
            data.song2.start()

    if data.stage == 5:
        if data.time == 0 and event.keysym == "2":
            data.stage = 5.5 #instructions for stage 6
            data.time = 50
    if data.stage == 5.5:
        if event.keysym == "s":
            data.stage = 6
            data.time = 50
    if data.stage == 6:
        if data.time == 0 and event.keysym == "3":
            data.stage = 6.5 #instructions for stage 7
            data.time = 50
    if data.stage == 6.5:
        if event.keysym == "s":
            data.stage = 7
            data.time = 50
    if data.stage == 7:
        # callTGC()
        if data.time == 0 and event.keysym == "r":
            data.stage = 8
            #stop sound 2
            data.song2.finished = True
    if data.stage == 8:
        if event.keysym == "c":
            data.stage = 8.5 #instructions 

    ## sound 3 ##

    if data.stage == 8.5:
        if event.keysym == "s":
            data.stage = 9
            data.time = 50

            #start sound 3
            data.songName = "crowd"
            data.song3 = soundThread(data.songName)
            data.song3.start()

    if data.stage == 9:
        if data.time == 0 and event.keysym == "2":
            data.stage = 9.5 #instructions 
            data.time = 50
    if data.stage == 9.5:
        if event.keysym == "s":
            data.stage = 10
            data.time = 50
    if data.stage == 10:
        if data.time == 0 and event.keysym == "3":
            data.stage = 10.5
            data.time = 50
    if data.stage == 10.5:
        if event.keysym == "s":
            data.stage = 11
            data.time = 50
    if data.stage == 11:
        # callTGC()
        if data.time == 0 and event.keysym == "r":
            data.stage = 12
            # stop sound 3
            data.song3.finished = True
    if data.stage == 12:
        if event.keysym == "c":
            data.stage = 12.5 #FINAL summary stage
    if data.stage == 14:
        if event.keysym == "c":
            data.stage = "jediSplash"
    if data.stage == "jediSplash":
        if event.keysym == "p":
            data.stage = "jediGame"



def playGameTimerFired(data):
    if data.time != 0:
        data.time -= 1

def readUrl(classical_url):
    with urllib.request.urlopen(classical_url) as response:
       return response.read()

def loadImageFromWeb(classical_url):
    assert(classical_url.endswith(".gif")) # only works for gif's!
    return PhotoImage(data=base64.encodebytes(readUrl(classical_url)))

def stage1Instructions(canvas, data):
    imageSize = ( (data.classical_image.width(), data.classical_image.height()) )
    canvas.create_image(data.width//2 + 50, 30, anchor=N, image=data.classical_image)

    # canvas.create_text(data.width/2, 0, text = "Stroop Test:", 
    #                    font = "Times 30 bold underline")
    canvas.create_text(data.width/2, 15, text = "Classical Music Stage 1", 
                       font = "Times 22 bold underline")

    canvas.create_text(data.width/2, (data.height//10) + 6, 
                        text = " Directions: Quickly choose the word that ", 
                        font = "Helvetica 14 italic", fill = "midnight blue")
    canvas.create_text(data.width/2, (data.height//10) + 26, 
                        text = "matches the color within the rectangles on top", 
                        font = "Helvetica 14 italic", fill = "midnight blue")

    canvas.create_text(data.width/2, (data.height//10) + 210, 
                       text = "Look at the adjacent screen to", 
                       font = "Hevetica 14 bold", fill = "maroon")
    canvas.create_text(data.width/2, (data.height//10) + 224, 
                       text = "see your Attention Level and Raw EEG data", 
                       font = "Hevetica 14 bold", fill = "maroon")

    canvas.create_text(data.width/2 + 10, (data.height) - 10, text = "Press s to play", 
                        font = "Helvetica 18 italic bold", fill = "maroon")


def stage1(canvas,data):

    canvas.create_rectangle(data.width/60, data.height/30,
                            data.width/5, data.height/8,
                            fill = "red")
    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink")
    canvas.create_text(27,150, text = "red") #correct answer - done
    # ##TEMP##
    # canvas.create_text(15, 142, text = ".", fill = "red")
    # canvas.create_text(39, 155, text = ".", fill = "red")
    # ########
    canvas.create_text(27,180, text = "black")

    canvas.create_rectangle(data.width/2 - 30, data.height/30,
                            (data.width/2) + 30, data.height/8,
                            fill = "green")
    canvas.create_text(data.width//2,60, text = "blue")
    canvas.create_text(data.width//2,90, text = "green") #correct answer - done
    # ##TEMP##
    # canvas.create_text(131, 82, text = ".", fill = "green")
    # canvas.create_text(168, 99, text = ".", fill = "green")
    # ########
    canvas.create_text(data.width//2,120, text = "pink")
    canvas.create_text(data.width//2,150, text = "red")
    canvas.create_text(data.width//2,180, text = "black")

    canvas.create_rectangle(data.width - data.width/60, data.height/30,
                            data.width - data.width/5, data.height/8,
                            fill = "blue")
    canvas.create_text(data.width - (55//2),60, text = "black")
    canvas.create_text(data.width - (55//2),90, text = "green")
    canvas.create_text(data.width - (55//2),120, text = "pink")
    canvas.create_text(data.width - (55//2),150, text = "red")
    canvas.create_text(data.width - (55//2),180, text = "blue") #correct answer
    # ##TEMP##
    # canvas.create_text(258, 168, text = ".", fill = "blue")
    # canvas.create_text(288, 188, text = ".", fill = "blue")
    # ########

def stage2Instructions(canvas, data):
    imageSize = ( (data.classical_image.width(), data.classical_image.height()) )
    canvas.create_image(data.width//2 + 50, 30, anchor=N, image=data.classical_image)

    canvas.create_text(data.width/2, 15, text = "Classical Music Stage 2", 
                       font = "Times 22 bold underline")

    canvas.create_text(data.width/2, (data.height//10) + 6, 
                        text = " Directions: Quickly choose the word that ", 
                        font = "Helvetica 14 italic", fill = "midnight blue")
    canvas.create_text(data.width/2, (data.height//10) + 26, 
                        text = "matches the word on top", 
                        font = "Helvetica 14 italic", fill = "midnight blue")

    canvas.create_text(data.width/2, (data.height//10) + 210, 
                       text = "Look at the adjacent screen to", 
                       font = "Hevetica 14 bold", fill = "maroon")
    canvas.create_text(data.width/2, (data.height//10) + 224, 
                       text = "see your Attention Level and Raw EEG data", 
                       font = "Hevetica 14 bold", fill = "maroon")

    canvas.create_text(data.width/2 + 10, (data.height) - 10, text = "Press s to play", 
                        font = "Helvetica 18 italic bold", fill = "maroon")


def stage2(canvas,data):      
    canvas.create_text(27, 30, text = "pink", fill = "deep pink", font = "Arial 20")

    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink")
    # ##TEMP##
    # canvas.create_text(15, 108, text = ".", fill = "pink")
    # canvas.create_text(39, 130, text = ".", fill = "pink")
    # ########
    canvas.create_text(27,150, text = "red")
    canvas.create_text(27,180, text = "black")

    canvas.create_text(data.width/2, 30, text = "green", fill = "green", font = "Arial 20")

    canvas.create_text(data.width/2,60, text = "blue")
    canvas.create_text(data.width/2,90, text = "green")
    # ##TEMP##
    # canvas.create_text(132, 79, text = ".", fill = "green")
    # canvas.create_text(169, 99, text = ".", fill = "green")
    # ########
    canvas.create_text(data.width/2,120, text = "pink")
    canvas.create_text(data.width/2,150, text = "red")
    canvas.create_text(data.width/2,180, text = "black")

    canvas.create_text(data.width - (55/2), 30, text = "orange", fill = "orange", font = "Arial 20")

    canvas.create_text(data.width - (55/2),60, text = "blue")
    canvas.create_text(data.width - (55/2),90, text = "green")
    canvas.create_text(data.width - (55/2),120, text = "pink")
    canvas.create_text(data.width - (55/2),150, text = "red")
    canvas.create_text(data.width - (55/2),180, text = "orange")
    # ##TEMP##
    # canvas.create_text(253, 168, text = ".", fill = "orange")
    # canvas.create_text(296, 188, text = ".", fill = "orange")
    # ########

def stage3Instructions(canvas, data):
    imageSize = ( (data.classical_image.width(), data.classical_image.height()) )
    canvas.create_image(data.width//2, 30, anchor=N, image=data.classical_image)

    canvas.create_text(data.width/2, 15, text = "Classical Music Stage 3", 
                       font = "Times 22 bold underline")

    canvas.create_text(data.width/2, (data.height//10) + 6, 
                        text = " Directions: Choose the color the word on top is", 
                        font = "Helvetica 14 italic", fill = "midnight blue")
    canvas.create_text(data.width/2, (data.height//10) + 20, 
                        font = "Helvetica 14 italic",
                         text = "shown in, rather than the color the word names", fill = "midnight blue")
    canvas.create_text(data.width/2, (data.height//10) + 210, 
                       text = "Look at the adjacent screen to", 
                       font = "Hevetica 14 bold", fill = "maroon")
    canvas.create_text(data.width/2, (data.height//10) + 224, 
                       text = "see your Attention Level and Raw EEG data", 
                       font = "Hevetica 14 bold", fill = "maroon")

    canvas.create_text(data.width/2 + 10, (data.height) - 10, text = "Press s to play", 
                        font = "Helvetica 18 italic bold", fill = "maroon")


def stage3(canvas,data):
    canvas.create_text(27, 30, text = "green", fill = "deep pink", font = "Arial 20")

    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink") #correct answer
    # ##TEMP##
    # canvas.create_text(13, 108, text = ".", fill = "black")
    # canvas.create_text(42, 131, text = ".", fill = "black")
    # ########
    canvas.create_text(27,150, text = "red")
    canvas.create_text(27,180, text = "black")

    canvas.create_text(data.width/2, 30, text = "red", fill = "purple", font = "Arial 20")

    canvas.create_text(data.width/2,60, text = "blue")
    canvas.create_text(data.width/2,90, text = "green")
    canvas.create_text(data.width/2,120, text = "pink")
    canvas.create_text(data.width/2,150, text = "red")
    canvas.create_text(data.width/2,180, text = "purple") #correct answer
    # ##TEMP##
    # canvas.create_text(132, 168, text = ".", fill = "black")
    # canvas.create_text(172, 190, text = ".", fill = "black")
    # ########

    canvas.create_text(data.width - (55/2), 30, text = "orange", fill = "blue", font = "Arial 20")

    canvas.create_text(data.width - (55/2),60, text = "red")
    canvas.create_text(data.width - (55/2),90, text = "green")
    canvas.create_text(data.width - (55/2),120, text = "pink")
    canvas.create_text(data.width - (55/2),150, text = "blue") #correct answer
    # ##TEMP##
    # canvas.create_text(255, 138, text = ".", fill = "black")
    # canvas.create_text(293, 160, text = ".", fill = "black")
    # ########
    canvas.create_text(data.width - (55/2),180, text = "orange")

# Reference: https://docs.python.org/3/library/functions.html
def stage4(canvas,data): #conclusion page 
    imageSize = ( (data.classical_image.width(), data.classical_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.classical_image)

    stage1 = (data.sound1_stage1_score/3) * 100
    stage2 = (data.sound1_stage2_score/3) * 100
    stage3 = (data.sound1_stage3_score/3) * 100

    s1 = str(stage1)
    s2 = str(stage2)
    s3 = str(stage3)

    filename = "sound1scores"

    graph = open(filename, mode='w')
    graph.write(s1 + "\n")
    graph.write(s2 + "\n")
    graph.write(s3 + "\n")
    

    graph.close()

    canvas.create_text(data.width//2, data.height//10 - 20, text = "Click to open an adjacent ",
                        font = "Helvetica 20 bold", fill = "maroon" )
    canvas.create_text(data.width//2, data.height//10, text = "screen with your scores!",
                        font = "Helvetica 20 bold", fill = "maroon" )
    canvas.create_text(data.width//2, data.height - 40, text = "Press c to change stage",
                        font = "Helvetica 20 bold", fill = "maroon" ) 

def readUrl(nature_url):
    with urllib.request.urlopen(nature_url) as response:
       return response.read()

def loadImageFromWeb(nature_url):
    assert(nature_url.endswith(".gif")) # only works for gif's!
    return PhotoImage(data=base64.encodebytes(readUrl(nature_url)))

def stage5Instructions(canvas, data):
    imageSize = ( (data.nature_image.width(), data.nature_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.nature_image)

    canvas.create_text(data.width/2, 35, text = "Nature Sounds Stage 1", 
                       font = "Times 25 bold underline")

    canvas.create_text(data.width/2, data.height//2 + 40, 
                        text = " Directions: Quickly choose the word that ", 
                        font = "Helvetica 14 italic ", fill = "black")
    canvas.create_text(data.width/2, data.height//2 + 60, 
                        text = "matches the color within the rectangles on top", 
                        font = "Helvetica 14 italic ", fill = "black")

    canvas.create_text(data.width/2, (data.height//10) + 220, 
                       text = "Look at the adjacent screen to see", 
                       font = "Hevetica 14 bold", fill = "midnight blue")
    canvas.create_text(data.width/2, (data.height//10) + 234, 
                       text = "your Attention Level and Raw EEG data", 
                       font = "Hevetica 14 bold", fill = "midnight blue")
    canvas.create_text(data.width/2 + 50, (data.height) - 20, text = "Press s to play", fill = "red", 
                        font = "Helvetica 14 bold")


def stage5(canvas,data):

    canvas.create_rectangle(data.width/60, data.height/30,
                            data.width/5, data.height/8,
                            fill = "red")
    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink")
    canvas.create_text(27,150, text = "red") #correct answer - done
    # ##TEMP##
    # canvas.create_text(15, 142, text = ".", fill = "red")
    # canvas.create_text(39, 155, text = ".", fill = "red")
    # ########
    canvas.create_text(27,180, text = "black")

    canvas.create_rectangle(data.width/2 - 30, data.height/30,
                            (data.width/2) + 30, data.height/8,
                            fill = "green")
    canvas.create_text(data.width//2,60, text = "blue")
    canvas.create_text(data.width//2,90, text = "green") #correct answer - done
    # ##TEMP##
    # canvas.create_text(131, 82, text = ".", fill = "green")
    # canvas.create_text(168, 99, text = ".", fill = "green")
    # ########
    canvas.create_text(data.width//2,120, text = "pink")
    canvas.create_text(data.width//2,150, text = "red")
    canvas.create_text(data.width//2,180, text = "black")

    canvas.create_rectangle(data.width - data.width/60, data.height/30,
                            data.width - data.width/5, data.height/8,
                            fill = "blue")
    canvas.create_text(data.width - (55//2),60, text = "black")
    canvas.create_text(data.width - (55//2),90, text = "green")
    canvas.create_text(data.width - (55//2),120, text = "pink")
    canvas.create_text(data.width - (55//2),150, text = "red")
    canvas.create_text(data.width - (55//2),180, text = "blue") #correct answer
    # ##TEMP##
    # canvas.create_text(258, 168, text = ".", fill = "blue")
    # canvas.create_text(288, 188, text = ".", fill = "blue")
    # ########

def stage6Instructions(canvas, data):
    imageSize = ( (data.nature_image.width(), data.nature_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.nature_image)


    canvas.create_text(data.width/2, 35, text = "Nature Sounds Stage 2", 
                       font = "Times 25 bold underline")

    canvas.create_text(data.width/2, data.height//2 + 40, 
                        text = " Directions: Quickly choose the word that ", 
                        font = "Helvetica 14 italic ", fill = "black")
    canvas.create_text(data.width/2, data.height//2 + 60, 
                        text = "matches the the word on top", 
                        font = "Helvetica 14 italic ", fill = "black")

    canvas.create_text(data.width/2, (data.height//10) + 220, 
                       text = "Look at the adjacent screen to see", 
                       font = "Hevetica 14 bold", fill = "midnight blue")
    canvas.create_text(data.width/2, (data.height//10) + 234, 
                       text = "your Attention Level and Raw EEG data", 
                       font = "Hevetica 14 bold", fill = "midnight blue")
    canvas.create_text(data.width/2 + 50, (data.height) - 20, text = "Press s to play", fill = "red", 
                        font = "Helvetica 14 bold")


def stage6(canvas,data):      
    canvas.create_text(27, 30, text = "pink", fill = "deep pink", font = "Arial 20")

    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink")
    # ##TEMP##
    # canvas.create_text(15, 108, text = ".", fill = "pink")
    # canvas.create_text(39, 130, text = ".", fill = "pink")
    # ########
    canvas.create_text(27,150, text = "red")
    canvas.create_text(27,180, text = "black")

    canvas.create_text(data.width/2, 30, text = "green", fill = "green", font = "Arial 20")

    canvas.create_text(data.width/2,60, text = "blue")
    canvas.create_text(data.width/2,90, text = "green")
    # ##TEMP##
    # canvas.create_text(132, 79, text = ".", fill = "green")
    # canvas.create_text(169, 99, text = ".", fill = "green")
    # ########
    canvas.create_text(data.width/2,120, text = "pink")
    canvas.create_text(data.width/2,150, text = "red")
    canvas.create_text(data.width/2,180, text = "black")

    canvas.create_text(data.width - (55/2), 30, text = "orange", fill = "orange", font = "Arial 20")

    canvas.create_text(data.width - (55/2),60, text = "blue")
    canvas.create_text(data.width - (55/2),90, text = "green")
    canvas.create_text(data.width - (55/2),120, text = "pink")
    canvas.create_text(data.width - (55/2),150, text = "red")
    canvas.create_text(data.width - (55/2),180, text = "orange")
    # ##TEMP##
    # canvas.create_text(253, 168, text = ".", fill = "orange")
    # canvas.create_text(296, 188, text = ".", fill = "orange")
    # ########

def stage7Instructions(canvas, data):
    imageSize = ( (data.nature_image.width(), data.nature_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.nature_image)


    canvas.create_text(data.width/2, 35, text = "Nature Sounds Stage 3", 
                       font = "Times 25 bold underline")

    canvas.create_text(data.width/2, (data.height//10) + 80, 
                        text = "Directions: Quickly choose the color in which")
    canvas.create_text(data.width/2, (data.height//10) + 100, 
                        text = "the word on top is displayed, rather")
    canvas.create_text(data.width/2, (data.height//10) + 120, 
                        text = "than the color that the word names")



    canvas.create_text(data.width/2, (data.height//10) + 220, 
                       text = "Look at the adjacent screen to see", 
                       font = "Hevetica 14 bold", fill = "midnight blue")
    canvas.create_text(data.width/2, (data.height//10) + 234, 
                       text = "your Attention Level and Raw EEG data", 
                       font = "Hevetica 14 bold", fill = "midnight blue")
    canvas.create_text(data.width/2 + 50, (data.height) - 20, text = "Press s to play", fill = "red", 
                        font = "Helvetica 14 bold")


def stage7(canvas,data):
    canvas.create_text(27, 30, text = "green", fill = "deep pink", font = "Arial 20")

    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink") #correct answer
    # ##TEMP##
    # canvas.create_text(13, 108, text = ".", fill = "black")
    # canvas.create_text(42, 131, text = ".", fill = "black")
    # ########
    canvas.create_text(27,150, text = "red")
    canvas.create_text(27,180, text = "black")

    canvas.create_text(data.width/2, 30, text = "red", fill = "purple", font = "Arial 20")

    canvas.create_text(data.width/2,60, text = "blue")
    canvas.create_text(data.width/2,90, text = "green")
    canvas.create_text(data.width/2,120, text = "pink")
    canvas.create_text(data.width/2,150, text = "red")
    canvas.create_text(data.width/2,180, text = "purple") #correct answer
    # ##TEMP##
    # canvas.create_text(132, 168, text = ".", fill = "black")
    # canvas.create_text(172, 190, text = ".", fill = "black")
    # ########

    canvas.create_text(data.width - (55/2), 30, text = "orange", fill = "blue", font = "Arial 20")

    canvas.create_text(data.width - (55/2),60, text = "red")
    canvas.create_text(data.width - (55/2),90, text = "green")
    canvas.create_text(data.width - (55/2),120, text = "pink")
    canvas.create_text(data.width - (55/2),150, text = "blue") #correct answer
    # ##TEMP##
    # canvas.create_text(255, 138, text = ".", fill = "black")
    # canvas.create_text(293, 160, text = ".", fill = "black")
    # ########
    canvas.create_text(data.width - (55/2),180, text = "orange")

# Reference: https://docs.python.org/3/library/functions.html
def stage8(canvas,data): #conclusion page 
    imageSize = ( (data.nature_image.width(), data.nature_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.nature_image)

    stage1 = (data.sound2_stage1_score/3) * 100
    stage2 = (data.sound2_stage2_score/3) * 100
    stage3 = (data.sound2_stage3_score/3) * 100

    s1 = str(stage1)
    s2 = str(stage2)
    s3 = str(stage3)

    filename = "sound2scores"

    graph = open(filename, mode='w')
    graph.write(s1 + "\n")
    graph.write(s2 + "\n")
    graph.write(s3 + "\n")
    

    graph.close()

    canvas.create_text(data.width//2, data.height - 80, text = "Click to see open an adjacent",
                        font = "Times 20 bold")
    canvas.create_text(data.width//2, data.height - 60, text = "screen with your scores!",
                        font = "Times 20 bold")

    canvas.create_text(data.width//2, data.height - 30, text = "Press c to change stage", 
                        font = "Times 18 bold")

def readUrl(crowd_url):
    with urllib.request.urlopen(crowd_url) as response:
       return response.read()

def loadImageFromWeb(crowd_url):
    assert(crowd_url.endswith(".gif")) # only works for gif's!
    return PhotoImage(data=base64.encodebytes(readUrl(crowd_url)))

def stage9Instructions(canvas, data):
    imageSize = ( (data.crowd_image.width(), data.crowd_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.crowd_image)

    canvas.create_text(data.width/2, (data.height//2) - 20, text = "Coffee House Sounds Stage 1", 
                       font = "Times 22 bold")

    canvas.create_text(data.width/2, (data.height//2) + 30 , 
                        text = "Quickly choose the word that matches", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height//2) + 50 , 
                        text = "the color within the rectangles on top", font = "Helvetica 15")
    canvas.create_text(data.width/2, (data.height//2) + 80, 
                       text = "Look at the adjacent screen to", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height//2) + 100, 
                       text = "see your Attention Level", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height) - 20, text = "Press s to play", 
                        font = "Times 20 italic bold")


def stage9(canvas,data):

    canvas.create_rectangle(data.width/60, data.height/30,
                            data.width/5, data.height/8,
                            fill = "red")
    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink")
    canvas.create_text(27,150, text = "red") #correct answer - done
    # ##TEMP##
    # canvas.create_text(15, 142, text = ".", fill = "red")
    # canvas.create_text(39, 155, text = ".", fill = "red")
    # ########
    canvas.create_text(27,180, text = "black")

    canvas.create_rectangle(data.width/2 - 30, data.height/30,
                            (data.width/2) + 30, data.height/8,
                            fill = "green")
    canvas.create_text(data.width//2,60, text = "blue")
    canvas.create_text(data.width//2,90, text = "green") #correct answer - done
    # ##TEMP##
    # canvas.create_text(131, 82, text = ".", fill = "green")
    # canvas.create_text(168, 99, text = ".", fill = "green")
    # ########
    canvas.create_text(data.width//2,120, text = "pink")
    canvas.create_text(data.width//2,150, text = "red")
    canvas.create_text(data.width//2,180, text = "black")

    canvas.create_rectangle(data.width - data.width/60, data.height/30,
                            data.width - data.width/5, data.height/8,
                            fill = "blue")
    canvas.create_text(data.width - (55//2),60, text = "black")
    canvas.create_text(data.width - (55//2),90, text = "green")
    canvas.create_text(data.width - (55//2),120, text = "pink")
    canvas.create_text(data.width - (55//2),150, text = "red")
    canvas.create_text(data.width - (55//2),180, text = "blue") #correct answer
    # ##TEMP##
    # canvas.create_text(258, 168, text = ".", fill = "blue")
    # canvas.create_text(288, 188, text = ".", fill = "blue")
    # ########

def stage10Instructions(canvas, data):
    imageSize = ( (data.crowd_image.width(), data.crowd_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.crowd_image)

    canvas.create_text(data.width/2, (data.height//2) - 20, text = "Coffee House Sounds Stage 2", 
                       font = "Times 22 bold")

    canvas.create_text(data.width/2, (data.height//2) + 30 , 
                        text = "Quickly choose the word that matches", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height//2) + 50 , 
                        text = "the word on top", font = "Helvetica 15")
    canvas.create_text(data.width/2, (data.height//2) + 80, 
                       text = "Look at the adjacent screen to", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height//2) + 100, 
                       text = "see your Attention Level", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height) - 20, text = "Press s to play", 
                        font = "Times 20 italic bold")


def stage10(canvas,data):      
    canvas.create_text(27, 30, text = "pink", fill = "deep pink", font = "Arial 20")

    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink")
    # ##TEMP##
    # canvas.create_text(15, 108, text = ".", fill = "pink")
    # canvas.create_text(39, 130, text = ".", fill = "pink")
    # ########
    canvas.create_text(27,150, text = "red")
    canvas.create_text(27,180, text = "black")

    canvas.create_text(data.width/2, 30, text = "green", fill = "green", font = "Arial 20")

    canvas.create_text(data.width/2,60, text = "blue")
    canvas.create_text(data.width/2,90, text = "green")
    # ##TEMP##
    # canvas.create_text(132, 79, text = ".", fill = "green")
    # canvas.create_text(169, 99, text = ".", fill = "green")
    # ########
    canvas.create_text(data.width/2,120, text = "pink")
    canvas.create_text(data.width/2,150, text = "red")
    canvas.create_text(data.width/2,180, text = "black")

    canvas.create_text(data.width - (55/2), 30, text = "orange", fill = "orange", font = "Arial 20")

    canvas.create_text(data.width - (55/2),60, text = "blue")
    canvas.create_text(data.width - (55/2),90, text = "green")
    canvas.create_text(data.width - (55/2),120, text = "pink")
    canvas.create_text(data.width - (55/2),150, text = "red")
    canvas.create_text(data.width - (55/2),180, text = "orange")
    # ##TEMP##
    # canvas.create_text(253, 168, text = ".", fill = "orange")
    # canvas.create_text(296, 188, text = ".", fill = "orange")
    # ########

def stage11Instructions(canvas, data):
    imageSize = ( (data.crowd_image.width(), data.crowd_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.crowd_image)

    canvas.create_text(data.width/2, (data.height//2) - 20, text = "Coffee House Sounds Stage 3", 
                       font = "Times 22 bold")

    canvas.create_text(data.width/2, (data.height//2) + 30 , 
                        text = "Quickly choose the color in which the word on", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height//2) + 50 , 
                        text = "top is displayed, rather", font = "Helvetica 15")
    canvas.create_text(data.width/2, (data.height//2) + 70 , 
                        text = "than the color that the word names", font = "Helvetica 15")
    canvas.create_text(data.width/2, (data.height//2) + 90, 
                       text = "Look at the adjacent screen to", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height//2) + 110, 
                       text = "see your Attention Level", font = "Helvetica 15 ")
    canvas.create_text(data.width/2, (data.height) - 20, text = "Press s to play", 
                        font = "Times 20 italic bold")


def stage11(canvas,data):
    canvas.create_text(27, 30, text = "green", fill = "deep pink", font = "Arial 20")

    canvas.create_text(27,60, text = "blue")
    canvas.create_text(27,90, text = "green")
    canvas.create_text(27,120, text = "pink") #correct answer
    # ##TEMP##
    # canvas.create_text(13, 108, text = ".", fill = "black")
    # canvas.create_text(42, 131, text = ".", fill = "black")
    # ########
    canvas.create_text(27,150, text = "red")
    canvas.create_text(27,180, text = "black")

    canvas.create_text(data.width/2, 30, text = "red", fill = "purple", font = "Arial 20")

    canvas.create_text(data.width/2,60, text = "blue")
    canvas.create_text(data.width/2,90, text = "green")
    canvas.create_text(data.width/2,120, text = "pink")
    canvas.create_text(data.width/2,150, text = "red")
    canvas.create_text(data.width/2,180, text = "purple") #correct answer
    # ##TEMP##
    # canvas.create_text(132, 168, text = ".", fill = "black")
    # canvas.create_text(172, 190, text = ".", fill = "black")
    # ########

    canvas.create_text(data.width - (55/2), 30, text = "orange", fill = "blue", font = "Arial 20")

    canvas.create_text(data.width - (55/2),60, text = "red")
    canvas.create_text(data.width - (55/2),90, text = "green")
    canvas.create_text(data.width - (55/2),120, text = "pink")
    canvas.create_text(data.width - (55/2),150, text = "blue") #correct answer
    # ##TEMP##
    # canvas.create_text(255, 138, text = ".", fill = "black")
    # canvas.create_text(293, 160, text = ".", fill = "black")
    # ########
    canvas.create_text(data.width - (55/2),180, text = "orange")

# Reference: https://docs.python.org/3/library/functions.html
def stage12(canvas,data): #conclusion page 
    imageSize = ( (data.crowd_image.width(), data.crowd_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.crowd_image)

    stage1 = (data.sound3_stage1_score/3) * 100
    stage2 = (data.sound3_stage2_score/3) * 100
    stage3 = (data.sound3_stage3_score/3) * 100

    s1 = str(stage1)
    s2 = str(stage2)
    s3 = str(stage3)

    filename = "sound3scores"

    graph = open(filename, mode='w')
    graph.write(s1 + "\n")
    graph.write(s2 + "\n")
    graph.write(s3 + "\n")
    

    graph.close()

    canvas.create_text(data.width//2, data.height//2, text = "Click to see open an adjacent ", 
                        font = "Helvetica 20 bold")
    canvas.create_text(data.width//2, data.height//2 + 20, text = "screen with your scores!", 
                        font = "Helvetica 20 bold")

    canvas.create_text(data.width//2, data.height - 30, text = "Press c to change stage", 
                        font = "Helvetica 20 bold")

def readUrl(reveal_url):
    with urllib.request.urlopen(reveal_url) as response:
       return response.read()

def loadImageFromWeb(reveal_url):
    assert(reveal_url.endswith(".gif")) # only works for gif's!
    return PhotoImage(data=base64.encodebytes(readUrl(reveal_url)))

def stage13(canvas, data):
    imageSize = ( (data.reveal_image.width(), data.reveal_image.height()) )
    canvas.create_image(data.width//2, 0, anchor=N, image=data.reveal_image)

    canvas.create_text(data.width//2, data.height//2 + 50 , 
                       text = " Click to reveal your", 
                       font = "Times 17 bold", fill = "white")
    canvas.create_text(data.width//2, data.height//2 + 70, 
                       text = "most productive pitch!!", 
                       font = "Times 17 bold", fill = "white")


def stage14(canvas, data):
    data.sound1_meanScore = ((data.sound1_stage1_score + data.sound1_stage2_score + data.sound1_stage3_score) / 3) * 100
    data.sound2_meanScore = ((data.sound2_stage1_score + data.sound2_stage2_score + data.sound2_stage3_score) / 3) * 100
    data.sound3_meanScore = ((data.sound3_stage1_score + data.sound3_stage2_score + data.sound3_stage3_score) / 3) * 100


    s1 = str(stage1)
    s2 = str(stage2)
    s3 = str(stage3)

    filename = "meanscores"

    graph = open(filename, mode='w')
    graph.write(s1 + "\n")
    graph.write(s2 + "\n")
    graph.write(s3 + "\n")
    

    graph.close()

    productivePitch = ""

    if data.sound1_meanScore == max(data.sound1_meanScore, data.sound2_meanScore, 
                                    data.sound3_meanScore):
        productivePitch = "Classical Music"
        imageSize = ( (data.classical_image.width(), data.classical_image.height()) )
        canvas.create_image(data.width//2, 0, anchor=N, image=data.classical_image)

    if data.sound2_meanScore == max(data.sound1_meanScore, data.sound2_meanScore, 
                                    data.sound3_meanScore):
        productivePitch = "Nature Sounds"
        imageSize = ( (data.nature_image.width(), data.nature_image.height()) )
        canvas.create_image(data.width//2, 0, anchor=N, image=data.nature_image)

    if data.sound3_meanScore == max(data.sound1_meanScore, data.sound2_meanScore, 
                                    data.sound3_meanScore):
        productivePitch = "Coffee House Sounds"
        imageSize = ( (data.crowd_image.width(), data.crowd_image.height()) )
        canvas.create_image(data.width//2, 0, anchor=N, image=data.crowd_image)

    canvas.create_text(data.width//2, data.height//2, 
                       text = productivePitch , font = "Times 20 bold")
    canvas.create_text(data.width//2, data.height//2 + 20, 
                       text = " is your most productive pitch!", font = "Times 20 bold")
    canvas.create_text(data.width//2, data.height - 20, text = "Thanks for playing, happy studying!", 
                        font = "Helvetica 17 italic bold")


def playGameRedrawAll(canvas, data):

    if data.stage not in [0,1.5, 2.5,4, 4.5, 5.5, 6.5, 8, 8.5, 9.5, 10.5, 12, 12.5, 14, "jediGame", "jediSplash"]:
        if data.time <= 10:
            fill = "red"
        else:
            fill = "black"
        canvas.create_text(data.width/2, data.height - 10, 
            text="Time: " + str(data.time) + "s", font="Arial 15", fill = fill)
    if data.stage == 0:
        stage1Instructions(canvas, data)
    if data.stage == 1:
        stage1(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2 , data.height/2 + 60,
                text = "Time's Up! Press 2 to continue to Stage 2!", font = "Arial 15", fill = "red")
    if data.stage == 1.5:
        stage2Instructions(canvas, data)
    if data.stage == 2:
        stage2(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2, data.height/2 + 60,
                text = "Time's Up! Press 3 to continue to Stage 3!", font = "Arial 15", fill = "red") 
    if data.stage == 2.5:
        stage3Instructions(canvas, data)
    if data.stage == 3:
        stage3(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2, data.height/2 + 60,
                text = "Press r to continue to see your results!", font = "Arial 15", fill = "red")

    if data.stage == 4:
        stage4(canvas,data)

### sound 2####
    if data.stage == 4.5:
        stage5Instructions(canvas, data)
    if data.stage == 5:
        stage5(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2 , data.height/2 + 60,
                text = "Time's Up! Press 2 to continue to Stage 2!", font = "Arial 15", fill = "red")
    if data.stage == 5.5:
        stage6Instructions(canvas, data)
    if data.stage == 6:
        stage6(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2, data.height/2 + 60,
                text = "Time's Up! Press 3 to continue to Stage 3!", font = "Arial 15", fill = "red") 
    if data.stage == 6.5:
        stage7Instructions(canvas, data)
    if data.stage == 7:
        stage7(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2, data.height/2 + 60,
                text = "Press r to continue to see your results!", font = "Arial 15", fill = "red")

    if data.stage == 8:
        stage8(canvas,data)
    if data.stage == 8.5:
        stage9Instructions(canvas, data)

### sound 3 ####
    if data.stage == 9:
        stage9(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2 , data.height/2 + 60,
                text = "Time's Up! Press 2 to continue to Stage 2!", font = "Arial 15", fill = "red")
    if data.stage == 9.5:
        stage10Instructions(canvas, data)
    if data.stage == 10:
        stage10(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2, data.height/2 + 60,
                text = "Time's Up! Press 3 to continue to Stage 3!", font = "Arial 15", fill = "red") 
    if data.stage == 10.5:
        stage11Instructions(canvas, data)
    if data.stage == 11:
        stage11(canvas,data)
        if data.time == 0:
            canvas.create_text(data.width/2, data.height/2 + 60,
                text = "Press r to continue to see your results!", font = "Arial 15", fill = "red")

    if data.stage == 12:
        stage12(canvas,data)
    if data.stage == 12.5:
        stage13(canvas, data)
    if data.stage == 14:
        stage14(canvas, data)
    if data.stage == "jediSplash":
        jediSplash(canvas, data)
    if data.stage == "jediGame":
        jediGame(canvas, data)

####################################
# endGame mode
####################################

#game ends after user has finished each trial
#at the end of the game a bar graph should be shown of the users results


####################################
# use the run function as-is
####################################

# Run function: http://www.cs.cmu.edu/~112/notes/events-example0.py

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds

    # create the root and the canvas (Note Change: do this BEFORE calling init!)
    root = Tk()

    # Store root in data so buttons can access
    data.root = root
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def go():
    run(300, 300)

def main():
    go()
    tr1 = soundThread()
    tr1.start()
    time.sleep(10)
    print("skip")
    tr1.finished = True
    tr1.join()

# if __name__ == '__main__':
#         main()
#main()

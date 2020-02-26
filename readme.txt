Project Information:
Productive Pitches is an application that allows the user to determine what background noises make them the most productive. This project uses the Stroop Task, which requires the user to be attentive. EEG and attention data are live streamed using the MindWave Mobile EEG headset while the user is playing the game to show them at what sounds they are the most attentive. Accuracy on the tasks is used to determine the most productive pitch!

My project should be installed by loading all the files in the submitted folder and by importing the necessary modules. The project is run by running the streamingData.py, which threads together all the files so that the EEG data and game can run simultaneously with music.

tgc.py is the file that connects to the headset and parses the information. It uses the following modules:
Built-in python socket module: 
This was used to create a connection between the headset and my computer and allowed data to be passed through
https://docs.python.org/3/library/socket.html
TCP Echo Client reference:
This source was used in conjunction with the socket module to create a client server environment for the EEG data to be sent.
ThinkGearConnector:
This was used to connect the EEG and configure it to my computer
http://developer.neurosky.com/docs/doku.php?id=thinkgear_connector_tgc
Plotly (python graphing library):
This was used to live-stream the EEG and attention data for the user.
https://plot.ly/python/
https://plot.ly/python/getting-started/
Built-in python time module:
This was used to control the amount of time the EEG data was being sent for.

TPsoundThreading.py is the file that threads the sounds used in the program so that they can be run within tkinter calls:
Built-in python module threading:
This was used to run sound and the game simultaneously
https://docs.python.org/3/library/threading.html
Pyaudio:
This was used to play the sound
https://people.csail.mit.edu/hubert/pyaudio/

graphClassical.py, graphNature.py, graphCrowd.py, graphOverall.py are the files that opened up a tkinter window with a graph of the users scores:
Built-in module tkinter
Matplotlib:
http://matplotlib.org/index.html
http://matplotlib.org/users/installing.html

gameTPTEST.py is the main game file that runs the Productive Pitches Application 
Built-in module tkinter 
Pyaudio:
This was used to play the sound
https://people.csail.mit.edu/hubert/pyaudio/
TPSoundThreading - this is my class that is imported in order to connect the sound to tkinter
urllib.request and base64 are Built-in:
They were imported for using online gif images in the program
time Built-in module:
This was use to measure execution time so that the songs had time to buffer
https://docs.python.org/2/library/timeit.html

streamingData.py is the only file that has to be run for the application and the graphical data to be presented:
Built-in tkinter
Pyaudio:
This was used to play the sound
https://people.csail.mit.edu/hubert/pyaudio/
gameTPTEST - this is my game file
TGC - this is my class for parsing EEG data
Built-in module threading


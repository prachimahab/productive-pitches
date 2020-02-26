#https://matplotlib.org/examples/user_interfaces/embedding_in_wx5.html
import matplotlib

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import sys
import tkinter as Tk




root = Tk.Tk()
root.wm_title("Coffee House Sounds Results")


figure = Figure(figsize=(4, 4), dpi=100)
a = figure.add_subplot(111)
t = [1, 2,3]
#need to pass in scores of user

def getScore(filename):

# ######reads file with data #########
#filename = "sound1scores"

	#print("### reading ", filename)
	graph = open(filename,mode='r')
	#line = f.readline()

	s1 = graph.readline()
	s2 = graph.readline()
	s3 = graph.readline()
	print(s1, s2, s3)
	return [float(s1), float(s2), float(s3)]

	#graph.close()

s = getScore("sound1scores")

a.plot(t, s)
a.set_title('Percent Accuracy vs. Difficulty of Task')
a.set_xlabel('Difficulty Level ( i.e. 1 = Stage 1 = easiest)')
a.set_ylabel('Percent Accuracy')

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(figure, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
"""
import tkinter as tk
from PIL import ImageTk, Image

#This creates the main window of an application
window = tk.Tk()
window.title("Join")
window.geometry("300x300")
window.configure(background='grey')

path = "weanFloorPlans/"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")

#Start the GUI
window.mainloop()
"""
"""
# button-demo1.py
# Simple buttons

# button-demo3.py
# button with an image 
# (otherwise, same as button-demo2.py)

from tkinter import *
import random

####################################
# customize these functions
####################################

def button1Pressed(data):
    data.count1 += 1

def button2Pressed(data):
    data.count2 += 1
    
def redrawAll(canvas, data):
    # background (fill canvas)
    canvas.create_rectangle(0,0,300,300,fill="cyan")
    # print counts
    msg = "count1: " + str(data.count1)
    canvas.create_text(150,130,text=msg)
    msg = "count2: " + str(data.count2)
    canvas.create_text(150,170,text=msg)

def onButton(data, buttonId):
    if (buttonId == 1): button1Pressed(data)
    elif (buttonId == 2): button2Pressed(data)

def init(data):
    data.count1 = 0
    data.count2 = 0
    buttonFrame = Frame(data.root)
    b1 = Button(buttonFrame, text="button1", command=lambda:onButton(data,1))
    b1.grid(row=0,column=0)

    buttonImage = PhotoImage(file="button.gif")
    b2 = Button(buttonFrame, image=buttonImage, width=50, height=50,
                bg="yellow", command=lambda:onButton(data,2))
    b2.image = buttonImage # save image from garbage collector (needed!)

    b2.grid(row=0,column=1)
    buttonFrame.pack(side=BOTTOM)

def mousePressed(event, data): pass
def keyPressed(event, data): pass
def timerFired(event): pass

####################################
# use the run function as-is
####################################

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

run(300, 300)
"""
"""
from tkinter import Tk, font
root = Tk()
print(font.families())
"""

import tkinter as tk

root = tk.Tk()
image = tk.PhotoImage(file="backgroundImage.gif")
label = tk.Label(image=image)
label.pack()
root.mainloop()













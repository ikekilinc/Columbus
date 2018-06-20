# Columbus - A Smart Navigation System for the Visually-Impaired

# This is the main file that controls the functionalities of Columbus. This file
# calls others in the main project folder to import and export data as needed to
# operate Columbus and create a cogent user-experience. This file will call
# Columbus' speech engine, node mapper, path finder, and image number reader.

from speech_to_text import *
from node_mapper import *
from path_finder import *
from main_algo import *
from tkinter import *


#####################################################################
#####################################################################

class Button(object):
    def __init__(self, purpose, coords, text):
        self.coords = coords
        self.text = text
        self.purpose = purpose
    def __repr__(self):
        return self.purpose
    def __hash__(self):
        return hash(self.purpose)
    def getCoords(self):
        return self.coords
    def pointInButton(self, xP, yP):
        (x0, y0, x1, y1) = (self.coords[0], self.coords[1],
                            self.coords[2], self.coords[3])
        return ((x0 <= xP <= x1) and (y0 <= yP <= y1))
    def getText(self):
        return self.text
    def getPurpose(self):
        return self.purpose


#####################################################################
#####################################################################

def init(data):
    data.startScreen = True
    data.modeSelection = False
    data.audioControl = False
    data.mode = None
    data.margin = data.width/16
    data.topMargin = data.height/3.5
    data.buttons = initButtons(data)
    data.startClicks = 0
    # data.backgroundImage = PhotoImage(file="backgroundImage.gif")
    # data.backgroundImageHalfSize = data.backgroundImage.subsample(2,2)
    # data.majorTitleFont = tkFont.Font(family="Helvetica", size=80, weight=bold)
    # data.minorTitleFont = tkFont.Font(family="Helvetica", size=50, weight=bold)
    # data.buttonFont = tkFont.Font(family="Helvetica", size=25)
    
    data.mapView = False
    data.startRoute = False
    data.nodesPath = None
    data.allSegments = None
    data.currSegmentNum = 0
    data.WH1Image = PhotoImage(file="WH_F1.gif")#.subsample(2,2)
    data.WH5Image = PhotoImage(file="WH_F5.gif")
    data.currFloor = 0
    data.nodeCircleRadius = 6
    data.offsetX = 0
    data.offsetY = 0


def initButtons(data):
    (w, h, m, tm) = (data.width, data.height, data.margin, data.topMargin)
    (butW, butH, diff) = (w/4, h/6, 20)

    buttonA = Button("specificDestination", [m-diff, tm*(4/3), m+butW+diff, tm*(4/3)+butH], "Find Destination")
    buttonB = Button("popularDestinations", [2*m+butW-diff, tm*(4/3), 2*m+2*butW+diff, tm*(4/3)+butH], "Popular Destinations")
    buttonC = Button("savedDestinations", [3*m+2*butW-diff, tm*(4/3), 3*m+3*butW+diff, tm*(4/3)+butH], "Saved Destinations")
    buttonD = Button("nearestRestroom", [m-diff, tm*(3/2)+butH, m+butW+diff, tm*(3/2)+2*butH], "Nearest Restroom")
    buttonE = Button("nearestPrinter", [2*m+butW-diff, tm*(3/2)+butH, 2*m+2*butW+diff, tm*(3/2)+2*butH], "Nearest Printer")
    buttonF = Button("findGod", [3*m+2*butW-diff, tm*(3/2)+butH, 3*m+3*butW+diff, tm*(3/2)+2*butH], "Find God")
    buttonG = Button("audioControl", [w/2-w/6-diff, h-tm/2, w/2+w/6+diff, h], "Enable Audio Control")

    buttons = [buttonA, buttonB, buttonC, buttonD, buttonE, buttonF, buttonG]
    return buttons

def mousePressed(event, data):
    if data.startScreen:
        data.startClicks += 1
        if data.startClicks > 1:
            data.startScreen = False
            data.modeSelection = True

    elif data.modeSelection:
        (x, y) = (event.x, event.y)
        for button in data.buttons:
            if button.pointInButton(x, y):
                if button.purpose == "audioControl":
                    data.audioControl = not data.audioControl
                    data.mode = startupModeSelection()
                else:
                    data.mode = button.getPurpose()
                data.modeSelection = False
                data.mapView = True
                data.startRoute = True
                print(data.mode)


                if data.mode == "specificDestination":
                    destination = destinationInput()
                    # startLocation = startLocationInput()
                    startLocation = input()
                elif data.mode == "nearestRestroom":
                    # startLocation = startLocationInput()
                    startLocation = input()
                    destination = None

                elif data.mode == "nearestPrinter":
                    # startLocation = startLocationInput()
                    startLocation = input()
                    destination = None

                elif data.mode == "popularDestinations":
                    # Columbus gives user choice options of popular destinations.
                    destination = popularLocationsInput()
                    # startLocation = startLocationInput()
                    startLocation = input()

                elif data.mode == "savedDestinations":
                    # Columbus gives user choice of previously saved destinations.
                    destination = savedLocationsInput()
                    # startLocation = startLocationInput()
                    startLocation = input()

                elif data.mode == "findGod":
                    pass

                # startLocation = input()
                # destination = input()

                data.nodesPath = pathFinder(startLocation, destination, data.mode)
                data.allSegments = createAllSegments(data.nodesPath)

                print(data.nodesPath)
                print(data.allSegments)
                for segment in data.allSegments:
                    print(segment.getSegBounds())

                startSegment = data.allSegments[0]
                data.currFloor = startSegment.getSegFloor()



    elif data.mapView:
        pass
        # enable click and drag functionality


def keyPressed(event, data):
    print(event.keysym)
    if data.startScreen:
        data.startClicks += 1
        if data.startClicks > 1:
            data.startScreen = False
            data.modeSelection = True

    elif data.modeSelection:
        if (event.keysym != "BackSpace"):
            data.audioControl = not data.audioControl
            data.mode = startupModeSelection()
            data.modeSelection = False
            data.mapView = True
            data.startRoute = True
            print(data.mode)
        else:
            data.startScreen = True
            data.modeSelection = False
    
    elif data.mapView:
        if (event.keysym == "space"):
            data.currSegmentNum += 1
            data.currFloor = data.allSegments[data.currSegmentNum].getSegFloor()
            print(data.currSegmentNum)
        elif (event.keysym == "BackSpace"):
            if data.currSegmentNum == 0:
                data.mapView = False
                data.startRoute = False
                data.modeSelection = True
            else:
                data.currSegmentNum -= 1
                data.currFloor = data.allSegments[data.currSegmentNum].getSegFloor()
                print(data.currSegmentNum)
        
        elif (event.keysym == "Left"):
            data.offsetX += 40
        elif (event.keysym == "Right"):
            data.offsetX -= 40
        elif (event.keysym == "Up"):
            data.offsetY += 40
        elif (event.keysym == "Down"):
            data.offsetY -= 40
        
        # print("cx,cy: ", data.width/2, data.height)
        # print("offx,offy: ", data.offsetX, data.offsetY)

        # print("result:", (data.width/2 + data.offsetX), -1* (data.height/2 - data.offsetY))


def timerFired(data):
    """
    if data.mapView == True:
        currSeg = data.allSegments[data.currSegmentNum]
        cx = data.width/2
        cy = data.height/2
        segCenterX = currSeg.getCenter()[0]
        segCenterY = currSeg.getCenter()[1]
        data.offsetX = -1 * segCenterX
        data.offsetY = -1 * segCenterY

        # data.offsetX = abs(cx - segCenterX)
        # data.offsetY = abs(cy - segCenterY)
        # print("segCX,segCY: ", segCenterX, segCenterY)
        # print("offx,offy: ", data.offsetX, data.offsetY)

        # data.offsetX = 
    """



def redrawAll(canvas, data):
    if data.startScreen:
        # canvas.create_image(data.width/2, data.height/2, image=data.backgroundImageHalfSize)
        canvas.create_text(data.width/2, 390, text="Columbus", anchor=S, font="Avenir 205 bold")
        canvas.create_text(data.width/2, 350, text="A Smart Navigation System for the Visually-Impaired",
                           anchor=N, font="Avenir 35 bold")
        canvas.create_text(data.width/2, 400, text="Click anywhere or press any button to continue",
                           anchor=N, font="Avenir 20")

    elif data.modeSelection:
        canvas.create_text(data.width/2, 10, text="Columbus", anchor=N, font="Avenir 185 bold")
        for button in data.buttons:
            coords = button.getCoords()
            (x0, y0, x1, y1) = (coords[0], coords[1], coords[2], coords[3])
            (cx, cy) = ((x1+x0)/2, (y1+y0)/2)
            if (button.getPurpose() == "audioControl") and (data.audioControl):
                buttonColor = "red"
            else:
                buttonColor = "black"
            canvas.create_rectangle(x0,y0,x1,y1, width=5, outline=buttonColor)
            canvas.create_text(cx, cy, text=button.getText(),
                               fill=buttonColor, font="Avenir 30")

    elif data.mapView:
        # currSegment = data.allSegments[data.currSegmentNum]
        # currSegmentFloor = currSegment.getSegFloor()
        # currFloor = "WH_F%d" % currSegmentFloor
        # currFloorImageName = currFloor + ".gif"
        # currFloorImage = PhotoImage(file="backgroundImage.gif")
        # print(data.currFloor)

        if data.currFloor == 1:
            currFloorImage = data.WH1Image

        elif data.currFloor == 5:
            currFloorImage = data.WH5Image

        canvas.create_image((data.offsetX),
                            (data.offsetY),
                            image=currFloorImage, anchor=NW)

        for segment in data.allSegments:
            # print(segment.getSegFloor(), data.currFloor)
            # print("isFloorChange: ", segment.getIsFloorChange())
            # print("segFloor==currFloor: ", segment.getSegFloor() == data.currFloor)
            # print("isFloorChange==False: ", segment.getIsFloorChange==False)
            # print("segment.getIsFloorChange: ", segment.getIsFloorChange())
            if (segment.getSegFloor() == data.currFloor and (segment.getIsFloorChange()==False)):
                segBounds = segment.getSegBounds()
                (x0,y0,x1,y1) = (segBounds[0] + data.offsetX, segBounds[1] + data.offsetY,
                                 segBounds[2] + data.offsetX, segBounds[3] + data.offsetY)
                # print(x0,y0,x1,y1)
                canvas.create_line(x0,y0,x1,y1, fill="green", width=5)
                # print(segBounds)

                r = data.nodeCircleRadius
                canvas.create_oval(x0-r, y0-r, x0+r, y0+r, fill="red")
                canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill="red")
                if data.allSegments.index(segment) == 0:
                    # start node indication
                    r = data.nodeCircleRadius + 1.5
                    canvas.create_oval(x0-r, y0-r, x0+r, y0+r, fill="blue")
                elif data.allSegments.index(segment) == len(data.allSegments)-1:
                    # end destination node symbol
                    r = data.nodeCircleRadius + 1.5
                    canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill="blue")
                    



#####################################################################
#####################################################################

def run(width=1000, height=600):
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
    # create the root and the canvas
    root = Tk()
    init(data)
    root.title("Columbus")
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

# run(2520, 1530)

# run(1265, 740)

# run(1008, 612)

run(1000, 600)







# Columbus - A Smart Navigation System for the Visually-Impaired
# ^^^^ Columbus - An A* Integrated Smart Navigation System

# This is the main file that controls the functionalities of Columbus. This file
# calls others in the main project folder to import and export data as needed to
# operate Columbus and create a cogent user-experience. This file will call
# Columbus' speech engine, node mapper, path finder, and image number reader.

from speech_to_text import *
from node_mapper import *
from path_finder import *
from main_algo import *
from tkinter import *
from audio_engine import *

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
    data.margin = data.width/16
    data.topMargin = data.height/3.5
    data.startClicks = 0
    data.allNodesMap = mapAllNodes()

    data.backgroundImage = PhotoImage(file="brownPaperBackground.gif")
    data.modeSelection = False
    data.audioControl = False
    data.mode = None
    data.modeButtons = initButtons(data)
    data.popLocsButtons = initPopLocsButtons(data)
    data.savedLocations = initSavedLocs(data)
    data.savedLocationButtons = initSavedLocsButtons(data)
    data.selectPopLocsScreen = False
    data.selectSavedLocsScreen = False
    # data.prevModesList = []
    
    data.mapView = False
    data.startRoute = False
    data.startLocation = None
    data.destination = None
    data.nodesPath = None
    data.allSegments = None

    data.currSegmentNum = 0
    data.currFloor = 0
    data.WH1Image = PhotoImage(file="WH_F1.gif")#.subsample(2,2)
    data.WH5Image = PhotoImage(file="WH_F5.gif")
    
    data.offsetX = 0
    data.offsetY = 0
    data.mapOffsetX = data.offsetX
    data.mapOffsetY = data.offsetY
    data.atDestination = False

    data.nodeCircleRadius = 6


def initButtons(data):
    (w, h, m, tm) = (data.width, data.height, data.margin, data.topMargin)
    (butW, butH, diff) = (w/4, h/6, 20)

    buttonA = Button("specificDestination", [m-diff, tm*(4/3), m+butW+diff, tm*(4/3)+butH], "Find Destination")
    buttonB = Button("popularDestinations", [2*m+butW-diff, tm*(4/3), 2*m+2*butW+diff, tm*(4/3)+butH], "Popular Destinations")
    buttonC = Button("savedDestinations", [3*m+2*butW-diff, tm*(4/3), 3*m+3*butW+diff, tm*(4/3)+butH], "Saved Destinations")
    buttonD = Button("nearestRestroom", [m-diff, tm*(3/2)+butH, m+butW+diff, tm*(3/2)+2*butH], "Nearest Restroom")
    buttonE = Button("nearestPrinter", [2*m+butW-diff, tm*(3/2)+butH, 2*m+2*butW+diff, tm*(3/2)+2*butH], "Nearest Printer")
    buttonF = Button("findGod", [3*m+2*butW-diff, tm*(3/2)+butH, 3*m+3*butW+diff, tm*(3/2)+2*butH], "Find God")
    buttonZ = Button("audioControl", [w/2-w/6-diff, h-tm/2-10, w/2+w/6+diff, h-10], "Enable Audio Control")

    buttons = [buttonA, buttonB, buttonC, buttonD, buttonE, buttonF, buttonZ]
    return buttons


def initPopLocsButtons(data):
    (w, h, m, tm) = (data.width, data.height, data.margin, data.topMargin)
    (butW, butH, diff) = (w/4, h/6, 20)

    buttonA = Button("5Prima", [m-diff, tm*(4/3), m+butW+diff, tm*(4/3)+butH], "Prima")
    buttonB = Button("4Sorrells", [2*m+butW-diff, tm*(4/3), 2*m+2*butW+diff, tm*(4/3)+butH], "Sorrells")
    buttonZ = Button("audioControl", [w/2-w/6-diff, h-tm/2-10, w/2+w/6+diff, h-10], "Enable Audio Control")

    buttons = [buttonA, buttonB, buttonZ]
    return buttons


def initSavedLocs(data):
    savedLocations = []
    currContents = readFile("savedLocations.txt")
    print("currContents: ", currContents)
    for location in currContents.splitlines():
        locationFloor = "WH%s" % location[0]
        locationNode = data.allNodesMap[locationFloor][location]
        savedLocations.append(locationNode)
    return savedLocations


def saveLocation(data, newLocation):
    finalStr = ""
    for location in data.savedLocations:
        # print(location)
        # if str(location) not in finalStr:
        finalStr = finalStr + str(location) + "\n"

    print("finalStr1: ", finalStr)
    if str(newLocation) not in finalStr:
        finalStr = finalStr + newLocation
        print("finalStr2: ", finalStr)
    else:
        finalStr = finalStr[:-1]
        print("finalStr: ", finalStr)
    print(finalStr)
    writeFile("savedLocations.txt", finalStr)


def initSavedLocsButtons(data):
    (w, h, m, tm) = (data.width, data.height, data.margin, data.topMargin)
    (butW, butH, diff) = (w/4, h/6, 20)
    allButtons = []

    for i in range(len(data.savedLocations)):
        location = data.savedLocations[i]
        x0 = (i%3 + 1)*m + (i%3)*butW - diff
        y0 = (tm*(4/3)) if (i//3 < 1) else (tm*(3/2) + butH)
        x1 = (i%3 + 1)*m + (i%3 + 1)*butW - diff
        y1 = (tm*(4/3)+butH) if (i//3 < 1) else (tm*(3/2)+2*butH)
        button = Button(str(location), [x0, y0, x1, y1], str(location))
        allButtons.append(button)

    # buttonA = Button("5Prima", [m-diff, tm*(4/3), m+butW+diff, tm*(4/3)+butH], "Prima")
    # buttonB = Button("4Sorrells", [2*m+butW-diff, tm*(4/3), 2*m+2*butW+diff, tm*(4/3)+butH], "Sorrells")
    # buttonC = Button("savedDestinations", [3*m+2*butW-diff, tm*(4/3), 3*m+3*butW+diff, tm*(4/3)+butH], "Saved Destinations")
    # buttonD = Button("nearestRestroom", [m-diff, tm*(3/2)+butH, m+butW+diff, tm*(3/2)+2*butH], "Nearest Restroom")
    # buttonE = Button("nearestPrinter", [2*m+butW-diff, tm*(3/2)+butH, 2*m+2*butW+diff, tm*(3/2)+2*butH], "Nearest Printer")
    # buttonF = Button("findGod", [3*m+2*butW-diff, tm*(3/2)+butH, 3*m+3*butW+diff, tm*(3/2)+2*butH], "Find God")
    # buttonZ = Button("audioControl", [w/2-w/6-diff, h-tm/2-10, w/2+w/6+diff, h-10], "Enable Audio Control")

    buttonZ = Button("audioControl", [w/2-w/6-diff, h-tm/2-10, w/2+w/6+diff, h-10], "Enable Audio Control")
    allButtons.append(buttonZ)

    return allButtons



def readFile(path): # From 15-112 "Strings" notes
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents): # From 15-112 "Strings" notes
    with open(path, "wt") as f:
        f.write(contents)

def runStartupSequence(data):
    if data.mode == "specificDestination":
        data.destination = destinationInput()
        # data.startLocation = startLocationInput()
        data.startLocation = input()
    elif data.mode == "nearestRestroom":
        # data.startLocation = startLocationInput()
        data.startLocation = input()
        # PLAY CONFIRMATION BEEP
        data.destination = None
    elif data.mode == "nearestPrinter":
        # data.startLocation = startLocationInput()
        data.startLocation = input()
        # PLAY CONFIRMATION BEEP
        data.destination = None
    elif data.mode == "popularDestinations" and data.startLocation == None:
        # Columbus gives user choice of popular destinations.
        data.selectPopLocsScreen = not data.selectPopLocsScreen
    elif data.mode == "savedDestinations" and data.startLocation == None:
        # Columbus gives user choice of previously saved destinations.
        data.selectSavedLocsScreen = not data.selectSavedLocsScreen
    elif data.mode == "findGod":
        # Columbus finds God.
        pass

    # data.startLocation = input()
    # data.destination = input()
    # print("Got here too!")
    # print("startLocation: ", data.startLocation)

    if data.startLocation != None:
        # print("Got to map maker area")
        data.modeSelection = False
        data.mapView = True
        data.startRoute = True
        # print(data.mode)

        data.nodesPath = pathFinder(data.startLocation, data.destination, data.mode)
        data.allSegments = createAllSegments(data.nodesPath)

        data.destination = str(data.nodesPath[-1])
        print(data.nodesPath)
        print(data.allSegments)
        for segment in data.allSegments:
            print(segment.getSegBounds())

        startSegment = data.allSegments[0]
        data.currFloor = startSegment.getSegFloor()


def mousePressed(event, data):
    if data.startScreen:
        data.startClicks += 1
        if data.startClicks > 1:
            data.startScreen = False
            data.modeSelection = True

    elif data.selectPopLocsScreen:
        (x, y) = (event.x, event.y)
        for button in data.popLocsButtons:
            if button.pointInButton(x, y):
                if button.purpose == "audioControl":
                    data.destination = popularLocationsInput(data)
                    # play("voiceCommands/confirmationBeep.wav")
                    data.startLocation = startLocationInput()
                else:
                    data.destination = button.getPurpose()
                    data.startLocation = input()
                # print(data.startLocation, data.destination)
                data.selectPopLocsScreen = False
                runStartupSequence(data)

    elif data.selectSavedLocsScreen:
        (x, y) = (event.x, event.y)
        for button in data.savedLocationButtons:
            if button.pointInButton(x, y):
                print("buttonPurpose: ", button.purpose)
                if button.purpose == "audioControl":
                    data.destination = savedLocationsInput(data)
                    # play("voiceCommands/confirmationBeep.wav")
                    data.startLocation = startLocationInput()
                else:
                    data.destination = button.getPurpose()
                    print("Input start location:")
                    data.startLocation = input()
                data.selectSavedLocsScreen = False
                runStartupSequence(data)


    elif data.modeSelection:
        (x, y) = (event.x, event.y)
        for button in data.modeButtons:
            if button.pointInButton(x, y):
                # print(data.mode)
                if button.purpose == "savedDestinations":
                    print(data.savedLocations)
                if button.purpose == "audioControl":
                    data.audioControl = not data.audioControl
                    data.mode = startupModeSelection()
                else:
                    data.mode = button.getPurpose()
                # print(data.mode)
                data.selectSavedLocsScreen = False
                runStartupSequence(data)

    elif data.mapView:
        pass
        # enable click and drag functionality

def keyPressed(event, data):
    if data.startScreen:
        print(event.keysym)
        data.startClicks += 1
        if data.startClicks > 1:
            data.startScreen = False
            data.modeSelection = True


    elif data.selectPopLocsScreen:
        if (event.keysym == "space"):
            # data.audioControl = not data.audioControl
            data.destination = popularLocationsInput(data)
            data.startLocation = startLocationInput()
            data.selectPopLocsScreen = False
            runStartupSequence(data)

        elif (event.keysym == "BackSpace"):
            data.modeSelection = True
            data.selectPopLocsScreen = False
            data.mode = None


    elif data.selectSavedLocsScreen:
        if (event.keysym == "space"):
            # data.audioControl = not data.audioControl
            data.destination = savedLocationsInput(data)
            data.startLocation = startLocationInput()

        elif (event.keysym == "BackSpace"):
            data.modeSelection = True
            data.selectSavedLocsScreen = False
            data.mode = None


    elif data.modeSelection:
        if (event.keysym == "space"):
            # data.audioControl = not data.audioControl
            data.mode = startupModeSelection()
            print(data.mode)

            runStartupSequence(data)

        elif (event.keysym == "BackSpace"):
            data.startScreen = True
            data.modeSelection = False
    

    elif data.mapView:
        if data.atDestination == True:
            # play("voiceCommands/arrivedAtDestination.wav")
            # play("voiceCommands/destinationSavePrompt.wav")
            if (event.keysym == "space"):
                data.startScreen = True
                data.mapView = False
                data.startRoute = False
                data.startLocation = None
                data.destination = None
            elif (event.keysym == "Return"):
                print(data.destination)
                saveLocation(data, data.destination)
                data.startScreen = True
                data.mapView = False
                data.startRoute = False
                data.startLocation = None
                data.destination = None
            data.savedLocations = initSavedLocs(data)
            data.savedLocationButtons = initSavedLocsButtons(data)

        if data.atDestination == False:
            # if data.currSegmentNum == 0:
            #     play("voiceCommands/startRoutePrompt.wav")
            if (event.keysym == "space"):
                if data.currSegmentNum < len(data.allSegments)-1:
                    data.currSegmentNum += 1
                    data.currFloor = data.allSegments[data.currSegmentNum].getSegFloor()
                    (data.offsetX, data.offsetY) = (0, 0)
                    print(data.currSegmentNum)
                else:
                    # play("voiceCommands/arrivedAtDestination.wav")
                    # play("voiceCommands/destinationSavePrompt.wav")
                    data.atDestination = True
            elif (event.keysym == "BackSpace"):
                if data.currSegmentNum == 0:
                    data.mapView = False
                    data.startRoute = False
                    data.modeSelection = True
                    data.startLocation = None
                    data.destination = None
                else:
                    data.currSegmentNum -= 1
                    data.currFloor = data.allSegments[data.currSegmentNum].getSegFloor()
                    (data.offsetX, data.offsetY) = (0, 0)
                    print(data.currSegmentNum)
            elif (event.keysym == "Left"):
                data.offsetX += 40
            elif (event.keysym == "Right"):
                data.offsetX -= 40
            elif (event.keysym == "Up"):
                data.offsetY += 40
            elif (event.keysym == "Down"):
                data.offsetY -= 40
        
            # if data.currSegmentNum == len(data.allSegments)-1:
            #     data.atDestination = True

        """
        else:
            if (event.keysym == )
        """

def timerFired(data):
    if data.mapView:
        currSeg = data.allSegments[data.currSegmentNum]
        cx = data.width/2
        cy = data.height/2
        segBounds = currSeg.getSegBounds()
        (x0,y0,x1,y1) = (segBounds[0], segBounds[1],
                         segBounds[2], segBounds[3])

        data.mapOffsetX = data.offsetX - x0 + cx
        data.mapOffsetY = data.offsetY - y0 + cy


def redrawAll(canvas, data):
    if data.startScreen:
        canvas.create_image(data.width/2, data.height/2, image=data.backgroundImage)
        canvas.create_text(data.width/2, 390, text="Columbus", anchor=S, font="Avenir 205 bold")
        canvas.create_text(data.width/2, 350, text="A Smart Navigation System for the Visually-Impaired",
                           anchor=N, font="Avenir 35 bold")
        canvas.create_text(data.width/2, 400, text="Click anywhere or press any button to continue",
                           anchor=N, font="Avenir 20")

    elif data.selectPopLocsScreen:
        canvas.create_image(data.width/2, data.height/2, image=data.backgroundImage)
        canvas.create_text(data.width/2, 10, text="Columbus", anchor=N, font="Avenir 185 bold")
        for button in data.popLocsButtons:
            coords = button.getCoords()
            (x0, y0, x1, y1) = (coords[0], coords[1], coords[2], coords[3])
            (cx, cy) = ((x1+x0)/2, (y1+y0)/2)
            # if (button.getPurpose() == "audioControl") and (data.audioControl):
            #     buttonColor = "red"
            # else:
            buttonColor = "black"
            canvas.create_rectangle(x0,y0,x1,y1, width=5, outline=buttonColor)
            canvas.create_text(cx, cy, text=button.getText(),
                               fill=buttonColor, font="Avenir 30")

    elif data.selectSavedLocsScreen:
        canvas.create_image(data.width/2, data.height/2, image=data.backgroundImage)
        canvas.create_text(data.width/2, 10, text="Columbus", anchor=N, font="Avenir 185 bold")
        for button in data.savedLocationButtons:
            coords = button.getCoords()
            (x0, y0, x1, y1) = (coords[0], coords[1], coords[2], coords[3])
            (cx, cy) = ((x1+x0)/2, (y1+y0)/2)
            # if (button.getPurpose() == "audioControl") and (data.audioControl):
            #     buttonColor = "red"
            # else:
            buttonColor = "black"
            canvas.create_rectangle(x0,y0,x1,y1, width=5, outline=buttonColor)
            canvas.create_text(cx, cy, text=button.getText(),
                               fill=buttonColor, font="Avenir 30")

    elif data.modeSelection:
        canvas.create_image(data.width/2, data.height/2, image=data.backgroundImage)
        canvas.create_text(data.width/2, 10, text="Columbus", anchor=N, font="Avenir 185 bold")
        for button in data.modeButtons:
            coords = button.getCoords()
            (x0, y0, x1, y1) = (coords[0], coords[1], coords[2], coords[3])
            (cx, cy) = ((x1+x0)/2, (y1+y0)/2)
            # if (button.getPurpose() == "audioControl") and (data.audioControl):
            #     buttonColor = "red"
            # else:
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

        canvas.create_image((data.mapOffsetX),
                            (data.mapOffsetY),
                            image=currFloorImage, anchor=NW)

        for segment in data.allSegments:
            # print(segment.getSegFloor(), data.currFloor)
            # print("isFloorChange: ", segment.getIsFloorChange())
            # print("segFloor==currFloor: ", segment.getSegFloor() == data.currFloor)
            # print("isFloorChange==False: ", segment.getIsFloorChange==False)
            # print("segment.getIsFloorChange: ", segment.getIsFloorChange())
            if (segment.getSegFloor() == data.currFloor and (segment.getIsFloorChange()==False)):
                segBounds = segment.getSegBounds()
                (x0,y0,x1,y1) = (segBounds[0] + data.mapOffsetX, segBounds[1] + data.mapOffsetY,
                                 segBounds[2] + data.mapOffsetX, segBounds[3] + data.mapOffsetY)
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
        
        start = data.startLocation
        dest = data.destination

        if dest == "5Prima":
            dest = "Prima"
        elif dest == "4Sorrells":
            dest = "Sorrells"
        elif "Print" in dest:
            dest = "Printer"
        elif data.mode == "findGod":
            dest = "God"

        canvas.create_rectangle(0,0,150,50, fill="gray")
        canvas.create_text(75,25, text="Start: " + start, font="Avenir 20")
        canvas.create_rectangle(800,0,1000,50, fill="gray")
        canvas.create_text(900,25, text="Destination: " + dest, font="Avenir 20")


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

run(1000, 600)

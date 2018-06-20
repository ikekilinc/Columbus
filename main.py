# Columbus - A Smart Navigation System for the Visually-Impaired

# This is the main file that controls the functionalities of Columbus. This file
# calls others in the main project folder to import and export data as needed to
# operate Columbus and create a cogent user-experience. This file will call
# Columbus' speech engine, node mapper, path finder, and image number reader.

from speech_engine import *
from node_mapper import *
from path_finder import *


"""
import speech_engine as speech_engine
import node_mapper as node_mapper
import path_finder as path_finder

class MainProgram(object):
    def __init__(self):
        pass
"""

def run():
    # User inputs destination.
    destination = destinationInput()

    # Columbus asks where user is (TEMP).
    startLocationInput = startLocationInput()

    # Columbus searches for and determines path to destination.
    

    # Columbus speaks path directions.


def destinationInput():
    # Columbus asks where user would like to go.
    speakText = "Where would you like to go?"
    speakColumbus(speakText)

    # User inputs destination
    destination = recognizeSpeech("location")

    # Columbus repeats destination for confirmation.
    speechText = "Is your destination %s" % destination

    # User confirms or corrects (if incorrect, repeat destination input).
    confirmation = recognizeSpeech("filter") 
    if confirmation == "yes":
        return destination
    else:
        return destinationInput()


def startLocationInput():
    # Columbus asks where user is now.
    speakText = "Where are you now?"
    speakColumbus(speakText)

    # User inputs start location.
    startLocation = recognizeSpeech("location")

    # Columbus repeats start location for confirmation.
    speakText = "Is your current location Wean Hall %s" % startLocation
    speakColumbus(speakText)

    # User confirms or corrects (if incorrect, repeat start location input).
    confirmation = recognizeSpeech("filter") 
    if confirmation == "yes":
        return startLocation
    else:
        return startLocationInput()


def speakColumbus(speechText):
    pass






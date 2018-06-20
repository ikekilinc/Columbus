# Speech to Text Engine

# The Speech to Text Engine enables the user to operate Columbus entirely
# with voice commands. Doing so makes Columbus accessible to a wider user base,
# specifically including the visually-impaired, who this product is intended to
# support. This engine utilizes the Google Cloud Speech API to convert user
# speech into strings and uses certain speech keywords to facilitate the user
# experience and determine the user's intended final destination.

import sys

sys.path.append('/')
import speech_recognition as sr
import pyaudio

def recognizeSpeech(formatFilter=None): # recognize speech using CMU Sphinx
    r = sr.Recognizer() # obtain audio from the microphone
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        output = r.recognize_google(audio)
        output = output.lower()
        print(output)
        if formatFilter==None:
            return output
        elif formatFilter=="location":
            output = filter(output)
            output = locationFilter(output)
        elif formatFilter=="confirm":
            output = filter(output)
            output = confirmFilter(output)
        else:
            output = filter(output)
        return output
    except sr.UnknownValueError:
        print("I could not understand audio")
    except sr.RequestError as e:
        print("Recognition error; {0}".format(e))

def filter(text): # format the text to be interpreted by Columbus
    if text == "": return None
    text = textNumbersToIntegers(text)
    text = correctCommands(text)
    return text

def textNumbersToIntegers(text): # turn text numbers into integers
    output = ''
    curNum = 0
    num = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,
        "eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,
        "fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,
        "nineteen":19,"twenty":20,"thirty":30,"fourty":40,"fifty":50,"sixty":60,
        "seventy":70,"eighty":80,"ninety":90,"hundred":100,"thousand":1000}
    for word in text.split():
        if word in num.keys():
            if word == "hundred" or word == "thousand":
                curNum = ((curNum%10) * num[word]) + ((curNum//10) * 10)
            else:
                curNum += num[word]
        else:
            if curNum != 0: output += ' ' + str(curNum)
            curNum = 0
            output += ' ' + word
    return output

def correctCommands(text):
    output = ""
    corrections = {}
    for word in text.split():
        if word in corrections.keys():
            word = corrections[word]
        output += word + ' '
    return output

def locationFilter(text):
    output = ""
    for word in text.split():
        if isNumber(word):
            output += word
    return output

def isNumber(string):
    try:
        float(s)
        return True
    except ValueError:
        return False

def confirmFilter(text):
    affirm = set(["yep", "yeah", "correct", "confirm", "confirmed"])
    negate = set(["nope", "nah", "incorrect", "wrong"])
    for word in text.split()
        if word in affirm:
            return "yes"
        elif word in negate:
            return "no"
    return None







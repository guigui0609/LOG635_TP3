from gtts import gTTS
import os
from playsound import playsound
import speech_recognition as sr

import keyboard
from enum import Enum

class SpecificKeys(Enum):
    UP_ARROW = "Top"
    DOWN_ARROW = "Right"
    LEFT_ARROW = "Bottom"
    RIGHT_ARROW = "Left"
    YES = "1"
    NO = "2"
    INVALID = "INVALID"

def outputToTerminal(textToOutput):
    print(textToOutput)

def outputTextAsSound(textToOutput):
    language = 'fr'
    myobj = gTTS(text=textToOutput, lang=language, slow=False)
    myobj.save("speech.mp3")

    playsound('speech.mp3', True)
    os.remove("speech.mp3")

def inputTextFromTerminal():
    return input()

def inputYesNoFromTerminal():
    print("Entrez 1 pour OUI ou 2 pour NON")
    keyPressed = SpecificKeys.INVALID

    while keyPressed == SpecificKeys.INVALID:
        if keyboard.is_pressed('1'):
            keyPressed = SpecificKeys.YES
        elif keyboard.is_pressed('2'):
            keyPressed = SpecificKeys.NO

    print()
    return keyPressed

def inputArrowKeyFromTerminal():
    print("Entrez une touche directionnelle pour changer de pièce")
    keyPressed = SpecificKeys.INVALID

    while keyPressed == SpecificKeys.INVALID:
        if keyboard.is_pressed('left'):
            keyPressed = SpecificKeys.LEFT_ARROW
        elif keyboard.is_pressed('right'):
            keyPressed = SpecificKeys.RIGHT_ARROW
        elif keyboard.is_pressed('up'):
            keyPressed = SpecificKeys.UP_ARROW
        elif keyboard.is_pressed('down'):
            keyPressed = SpecificKeys.DOWN_ARROW

    print()
    return keyPressed

# Canal de communication 1 : À travers un fichier texte.
# Le fichier texte doit se nommer inputFile.txt et doit se situer dans le même dossier que le fichier présent.
def inputFromFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'inputFile.txt')

    f = open(filename, "r")
    return f.read()

def inputFromMic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response
from gtts import gTTS
import os
import time
from playsound import playsound
import speech_recognition as sr

import keyboard
from enum import Enum

# Class enum utilisé pour la communication avec les touches directionnelles et les touches oui et non
from data.constants import Constants


class SpecificKeys(Enum):
    UP_ARROW = "Top"
    DOWN_ARROW = "Bottom"
    LEFT_ARROW = "Left"
    RIGHT_ARROW = "Right"
    YES = "1"
    NO = "2"
    INVALID = "INVALID"

class IOController:
    def __init__(self):
        self.__micInputUsed = False
        self.__micInputFailedAttempt = 0
        self.__soundOutputUsed = False
        self.__textFileInputUsed = False

        keyboard.on_release_key("1", self.__yesButtonReleased)
        keyboard.on_release_key("2", self.__noButtonReleased)

        keyboard.on_release_key("left", self.__leftArrowReleased)
        keyboard.on_release_key("right", self.__rightArrowReleased)
        keyboard.on_release_key("up", self.__upArrowReleased)
        keyboard.on_release_key("down", self.__downArrowReleased)

    # Méthode pour demander un input de l'utilisateur
    # On commence par demandé avec la reconnaissance vocale (1 succès ou 2 tentative sinon)
    # Ensuite, on utilise le input avec le fichier inputFile.txt
    # Finalement, le program utilisera le input avec la ligne de commande jusqu'à la fin
    def input(self):
        if not self.__micInputUsed:
            response = self.__inputFromMic()

            if not response["success"]:
                self.outputToTerminal("Je ne peux pas accéder à Google Speach en ce moment. Veuillez entrer"
                                        "le texte sur la ligne de commande et nous réessaierons plus tard!")
                return self.__inputTextFromTerminal()

            else:
                inputText = response["transcription"]

                if inputText is None:
                    output = "Je n'ai pas réussi à capter votre voix."
                    self.outputToTerminal(output)
                    self.__outputTextAsSound(output)
                    self.__incrementSpeechFailedCounter()
                    return self.__handleInputFailed(True)

                else:

                    # Pour simuler une vrai conversation avec un robot :)
                    self.output("J'ai compris " + inputText + ". Est-ce correct?")
                    self.__outputTextAsSound("J'ai compris " + inputText + ". Est-ce correct?")
                    promptAnswer = self.inputYesNoFromTerminal()
                    if promptAnswer == SpecificKeys.YES:
                        self.__micInputUsed = True
                        return inputText
                    else:
                        self.__incrementSpeechFailedCounter()
                        return self.__handleInputFailed(True)

        elif not self.__textFileInputUsed:
            inputText = self.__inputFromFile()
            self.outputToTerminal("J'ai lu: \"" + inputText + "\". Est-ce correct?")

            promptAnswer = self.inputYesNoFromTerminal()
            if promptAnswer == SpecificKeys.YES:
                self.__textFileInputUsed = True
                return inputText
            else:
                return self.__handleInputFailed()

        else:
            return self.__inputTextFromTerminal()

    # Méthode pour gérer les output
    # On commence par le output avec le son
    # Ensuite, le program utilisera la ligne de commande jusqu'à la fin
    def output(self, text):
        if not self.__soundOutputUsed:
            self.__soundOutputUsed = True
            self.outputToTerminal(text)
            self.__outputTextAsSound(text)
        else:
            self.outputToTerminal(text)

    # Méthode pour avoir une touche directionnelle. Utilisé pour se déplacer de pièces en pièces.
    # Canal de communication 4: L'utilisateur utilise les touches directionnelles dans le terminal
    def inputArrowKeyFromTerminal(self):
        self.__keyPressed = SpecificKeys.INVALID
        print("Entrez une touche directionnelle pour changer de pièce.")

        while self.__keyPressed == SpecificKeys.INVALID:
            time.sleep(Constants.TIME_BETWEEN_DIALOG)

        print()
        return self.__keyPressed

    # Canal de communication 4: l'utilisateur dit oui ou non à travers le terminal
    def inputYesNoFromTerminal(self):
        self.__keyPressed = SpecificKeys.INVALID
        print("Entrez 1 pour OUI ou 2 pour NON")

        while self.__keyPressed == SpecificKeys.INVALID:
            time.sleep(1)

        print()
        return self.__keyPressed

    # Canal de communication 3: L'agent écrit à l'utilisateur via le terminal
    def outputToTerminal(self, textToOutput):
        print(textToOutput)
        time.sleep(Constants.TIME_BETWEEN_DIALOG)

    # Méthodes privés

    def __handleInputFailed(self, playSound=False):
        output = "Veuillez entrer votre texte dans la console:"
        self.outputToTerminal(output)

        if playSound:
            self.__outputTextAsSound(output)

        return self.__inputTextFromTerminal()

    def __incrementSpeechFailedCounter(self):
        self.__micInputFailedAttempt += 1

        if self.__micInputFailedAttempt == 2:
            self.__micInputUsed = True  # On abandonne le mic si ça ne marche pas après 2 essais!

    # Canal de communication 2, l'agent communique à l'utilisateur à travers le son
    def __outputTextAsSound(self, textToOutput):
        language = 'fr'
        myobj = gTTS(text=textToOutput, lang=language, slow=False)
        myobj.save("speech.mp3")

        playsound('speech.mp3', True)
        os.remove("speech.mp3")

    # Canal de communication 3: l'utilisateur écrit dans le terminal
    def __inputTextFromTerminal(self):
        return input()

    def __yesButtonReleased(self, e):
        self.__keyPressed = SpecificKeys.YES

    def __noButtonReleased(self, e):
        self.__keyPressed = SpecificKeys.NO

    def __leftArrowReleased(self, e):
        self.__keyPressed = SpecificKeys.LEFT_ARROW

    def __rightArrowReleased(self, e):
        self.__keyPressed = SpecificKeys.RIGHT_ARROW

    def __upArrowReleased(self, e):
        self.__keyPressed = SpecificKeys.UP_ARROW

    def __downArrowReleased(self, e):
        self.__keyPressed = SpecificKeys.DOWN_ARROW

    # Canal de communication 1 : À travers un fichier texte.
    # Le fichier texte doit se nommer inputFile.txt et doit se situer dans le même dossier que le fichier présent.
    def __inputFromFile(self):
        readyToRead = False
        while not readyToRead:
            self.outputToTerminal("Veuillez entrer le texte dans le fichier inputFile.txt")
            self.outputToTerminal("Est-ce que le fichier inputFile.txt est prêt à être lu?")
            promptInput = self.inputYesNoFromTerminal()

            if promptInput == SpecificKeys.YES:
                readyToRead = True

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, 'inputFile.txt')

        f = open(filename, "r", encoding="utf-8")
        return f.read()

    # Canal de communication 2, l'utilisateur utilise le microphone pour communiquer au programme
    def __inputFromMic(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

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

        self.outputToTerminal("Parlez maintenant:")

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
            response["transcription"] = recognizer.recognize_google(audio, language="fr-CA")
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response
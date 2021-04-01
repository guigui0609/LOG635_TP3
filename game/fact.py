class Fact:

    # La phrase interrogative permettant d'interroger l'humain sur le fait
    INTERROGATION_SENTENCE: str = None

    def __init__(self, fcfg):

        self.fcfg = fcfg
        self.information = None

    def get_interrogation_sentence(self):
        return self.__class__.INTERROGATION_SENTENCE

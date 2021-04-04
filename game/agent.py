import json

import nltk

from data.data import Directions
from game.CrimeInference import CrimeInference


class Agent:

    INITIAL_FACTS_PATH = "initial_facts.json"

    def __init__(self, rooms, characters, weapons):
        self.current_room = None
        self.crime_inference = CrimeInference(rooms, characters, weapons)

    def move(self, direction: Directions):
        self.current_room = self.current_room.get_neighbour_room(direction)

    # Repris de Reasoning System.ipynb
    def results_as_string(self, results):
        res = ''
        for result in results:
            # synrep = syntactic representation
            # semrep = semantic representation
            for (synrep, semrep) in result:
                res += str(semrep)
        return res

    # Repris de Reasoning System.ipynb
    def to_fol(self, fact, grammar):

        results = nltk.interpret_sents([fact,], grammar)
        sent = self.results_as_string(results)
        print(sent)
        return sent

    # L'agent demande à l'humain un fait. L'humain lui répond avec une phrase contenant ce fait. L'agent transforme
    # la phrase contenant le fait en clause de type FOL
    def ask_for_fact(self, interrogation_sentece, fcfg):

        answer = input(interrogation_sentece)
        fol = self.to_fol(answer, fcfg)
        self.crime_inference.add_clause(fol)


    # L'agent transforme les faits initiaux en clauses de type FOL
    def get_initial_facts(self):

        with open(Agent.INITIAL_FACTS_PATH, encoding="utf-8") as r:
            data = json.load(r)

            for fact in data.values():
                fol = self.to_fol(fact["texte"], fact["fichier"])
                self.crime_inference.add_clause(fol)

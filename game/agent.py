import json

import nltk

from data.data import Directions
from game.crime_inference import CrimeInference
from gameIO.gameIO import IOController
from util import Util


class Agent:

    INITIAL_FACTS_PATH = "initial_facts.json"

    def __init__(self, start_room, rooms, characters, weapons, crime_time, drop_weapon_time):

        self.game_io = IOController()
        self.current_room = start_room
        self.crime_inference = CrimeInference(rooms, characters, weapons)
        self.crime_time = crime_time
        self.drop_weapon_time = drop_weapon_time

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
        return sent

    # L'agent demande à l'humain un fait. L'humain lui répond avec une phrase contenant ce fait. L'agent transforme
    # la phrase contenant le fait en clause de type FOL
    def ask_for_fact(self, interrogation_sentece, fcfg):

        self.game_io.output(interrogation_sentece)
        answer = self.game_io.input()
        fol = self.to_fol(answer, fcfg)
        self.crime_inference.add_clause(fol)

    # L'agent transforme les faits initiaux en clauses de type FOL
    def get_initial_facts(self):

        with open(Agent.INITIAL_FACTS_PATH, encoding="utf-8") as r:
            data = json.load(r)

            for fact in data.values():
                fol = self.to_fol(fact["texte"], fact["fichier"])
                self.crime_inference.add_clause(fol)

    def interrogate(self, character):

        self.game_io.output("Voulez-vous demander qui " + character.character_type.value + " a rencontré une heure après le crime?")
        key = self.game_io.inputYesNoFromTerminal().value
        if key == "1":
            self.interrogate_at_time(character, self.drop_weapon_time)

    def interrogate_at_time(self, character, time):

        encounters = character.encounters[time]
        room = character.rooms[time].room_type.value

        for encounter in encounters:
            self.game_io.output(
                encounter.character_type.value + " se trouvait dans le/la " + room + " à " + str(time) + "h")
            encounter = encounter.character_type.value
            self.crime_inference.create_clause(self.crime_inference.person_room_hour_clause, encounter, room, time)

    def discover_weapon(self, weapon, room):

        self.game_io.output("L'agent trouve un/une " + weapon)
        self.crime_inference.create_clause(self.crime_inference.weapon_room_clause, weapon, room)

    def discover_victim(self, character, room, time):

        self.game_io.output("L'agent découvre le corps de " + character.character_type.value)

        self.crime_inference.create_clause(self.crime_inference.victim_clause, character.character_type.value)
        self.crime_inference.create_clause(self.crime_inference.person_room_hour_clause, character.character_type.value,
                                                     room, time)

        self.ask_for_fact("Dans quel état est le corps de " + character.character_type.value + "?", "grammars/personne_marque.fcfg")

    def discover_character(self, character, room, time):

        self.game_io.output("L'agent rencontre " + character.character_type.value + ".")
        self.game_io.output("Voulez-vous interroger cette personne?")
        key = self.game_io.inputYesNoFromTerminal().value

        if key == "1":
            self.interrogate(character)

        self.crime_inference.create_clause(self.crime_inference.person_room_hour_clause, character.character_type.value,
                                               room, time)

    def move(self):

        agent_moved = False
        while not agent_moved:
            key = self.game_io.inputArrowKeyFromTerminal().value

            direction = Util.convert_key_to_direction(key)

            if direction is None:
                self.game_io.output("La touche entrée " + key + " n'est pas valide.")
            else:
                neighbour_room = self.current_room.get_neighbour_room(direction)

                if neighbour_room is None:
                    self.game_io.output("Il n'y a pas de pièce dans la direction demandée. Entrez une autre direction.")
                else:
                    agent_moved = True
                    self.current_room = neighbour_room

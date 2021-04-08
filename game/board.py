import math
import random
import time
from typing import List

from data.constants import Constants
from data.data import Directions
from data.game_data import RoomTypes, CharacterTypes, WeaponTypes
from game.agent import Agent
from game.character import Character
from game.room import Room

class Board:

    BEGIN_TIME = 8
    START_ROOM = RoomTypes.HALL

    def __init__(self, nb_rooms, nb_characters, nb_weapons):

        self.nb_rooms = nb_rooms
        self.nb_characters = nb_characters
        self.nb_weapons = nb_weapons
        self.rooms = []
        self.characters: List[Character] = []
        self.weapons = []
        self.criminal = None
        self.victim = None
        self.start_room = None
        self.agent = None

        self.crime_time = None
        self.drop_weapon_time = None

        self.ticks = 0

    def start_game(self):

        self.generate_rooms()
        self.place_characters()
        self.place_weapons()
        self.generate_crime()

        self.agent = Agent(self.start_room, self.rooms, self.characters, self.weapons, self.crime_time, self.drop_weapon_time)
        self.agent.get_initial_facts()

        print("L'agent AI arrive sur les lieux du crime afin d'enquêter sur le meurtre.")
        time.sleep(Constants.TIME_BETWEEN_DIALOG)
        self.agent.game_io.output("Désirez-vous commencer l'enquête?")
        self.agent.game_io.inputYesNoFromTerminal()

        self.start_investigation()

    def generate_rooms(self):

        room_types = []

        room_types_iter = RoomTypes.__iter__()
        for i in range(self.nb_rooms):
            room_types.append(room_types_iter.__next__())

        random.shuffle(room_types)

        room_width = int(math.sqrt(len(room_types)))
        room_height = math.ceil(len(room_types) / room_width)

        for i in range(room_height):
            for j in range(room_width):

                if room_width * i + j >= len(room_types):
                    break

                bottom_room = None
                if i > 0:
                    bottom_room = self.rooms[room_width * (i - 1) + j]

                left_room = None
                if j > 0:
                    left_room = self.rooms[room_width * i + j - 1]

                room_type = room_types[room_width * i + j]
                room = Room(room_type)

                if room_type is self.__class__.START_ROOM:
                    self.start_room = room

                if bottom_room is not None:
                    room.add_neighbour_room(bottom_room, Directions.BOTTOM)

                if left_room is not None:
                    room.add_neighbour_room(left_room, Directions.LEFT)

                self.rooms.append(room)

    def place_characters(self):

        indexes = []

        character_types_iter = CharacterTypes.__iter__()

        for i in range(self.nb_characters):

            if not indexes or len(indexes) == 0:
                for i in range(len(self.rooms)):
                    indexes.append(i)

            index = int(random.random() * len(indexes))
            character_type = character_types_iter.__next__()
            character = Character(character_type, self.rooms[index])
            self.rooms[index].add_character(character)
            self.characters.append(character)
            indexes.pop(index)

    def place_weapons(self):

        indexes = []

        weapon_types_iter = WeaponTypes.__iter__()

        for i in range(self.nb_weapons):

            if not indexes or len(indexes) == 0:
                for i in range(len(self.rooms)):
                    indexes.append(i)

            index = int(random.random() * len(indexes))
            weapon = weapon_types_iter.__next__()
            self.rooms[index].add_weapon(weapon)
            self.weapons.append(weapon)
            indexes.pop(index)

    def get_current_time_value(self):
        return (self.__class__.BEGIN_TIME + self.ticks) % 12

    # On génère les circonstances entourant le meurtre, c'est-à-dire les actions des personnages avant et après le meurtre
    def generate_crime(self):

        character_index = int(random.random() * len(self.characters))
        self.criminal = self.characters[character_index]

        weapon_taken = False
        victim_killed = False
        victim_discovered = False

        # Tant qu'une victime n'est pas découverte, les personnages se déplacent dans le manoir de manière aléatoire
        while not victim_discovered:

            self.ticks += 1
            time_value = self.get_current_time_value()

            for character in self.characters:

                # À chaque heure, chaque personnage vivant se déplace vers une pièce adjacente
                if not character.victim:
                    character.move_to_adjacent_room(time_value)

            for character in self.characters:

                # Une fois que les personnages ont changé de pièce, ils se rencontrent
                character.encounter(time_value)

            # Lorsque le meurtrier entre dans une pièce qui contient une arme, il récupère celle-ci
            if self.criminal.room.weapon != None and not weapon_taken:

                print("Il est {}. Le criminel, {}, trouve un(e) {} dans le/la {}. Il le/la ramasse avec appréhension".format(
                    str(time_value) + "h",
                    self.criminal.character_type.value,
                    self.criminal.room.weapon.value,
                    self.criminal.room.room_type.value))
                time.sleep(Constants.TIME_BETWEEN_DIALOG)

                self.criminal.take_weapon()
                weapon_taken = True

            # Lorsque le meurtrier a pris son arme et qu'il se trouve dans la même pièce qu'un autre personnage,
            # il l'assassine et ce personnage devient la victime
            elif weapon_taken and len(self.criminal.room.characters) > 1 and not victim_killed:

                characters = self.criminal.room.characters.values()

                for character in characters:

                    # Le criminel assassine un des personnages de la pièce qui n'est pas lui-même
                    if character.character_type is not self.criminal.character_type:

                        character.victim = True
                        self.victim = character
                        victim_killed = True
                        self.crime_time = time_value

                        print("Il est {} heure. Le criminel, {}, assassine {} avec son/sa {} dans le/la {}".format(
                            str(time_value) + "h",
                            self.criminal.character_type.value,
                            self.victim.character_type.value,
                            self.criminal.weapon.value,
                            self.criminal.room.room_type.value))
                        time.sleep(Constants.TIME_BETWEEN_DIALOG)
                        break

            elif victim_killed:

                # Après avoir tué sa victime, le criminel laisse tomber son arme dans la salle dans laquelle il se
                # trouve
                if self.criminal.weapon is not None:

                    self.criminal.drop_weapon()
                    self.drop_weapon_time = time_value

                # Lorsqu'il y a un autre personnage dans la pièce de la victime, celui-ci découvre la victime
                if len(self.victim.room.characters) > 1:

                    characters = self.victim.room.characters.values()

                    # Le personnage dans la pièce qui n'est pas la victime elle-même découvre la victime
                    for character in characters:
                        if character.character_type is not self.victim.character_type:
                            victim_discovered = True
                            print("Il est {} heure. {} découvre le corps de {} dans le/la {}".format(
                                str(time_value) + "h",
                                character.character_type.value,
                                self.victim.character_type.value,
                                self.victim.room.room_type.value))
                            time.sleep(Constants.TIME_BETWEEN_DIALOG)
                            break

    def start_investigation(self):

        self.agent.ask_for_fact("À quelle heure le meurtrier a laissé tomber son arme ?", "grammars/arme_tombee_heure.fcfg")

        current_time = self.get_current_time_value()
        self.agent.crime_inference.create_clause(self.agent.crime_inference.heure_actuelle_clause, current_time)
        continue_investigation = True

        while continue_investigation:

            room = self.agent.current_room.room_type.value

            print("L'agent se trouve dans le/la " + room)
            time.sleep(Constants.TIME_BETWEEN_DIALOG)

            # L'agent recueille les informations sur la pièce dans laquelle il se trouve présentement
            if not self.agent.current_room.visited:

                self.agent.crime_inference.create_clause(self.agent.crime_inference.piece_clause, room)
                self.agent.current_room.visited = True

                # L'agent note la pièce de chaque arme
                if self.agent.current_room.weapon is not None:
                    self.agent.discover_weapon(self.agent.current_room.weapon.value, room)

                # L'agent note la pièce de l'arme du meurtrier sans savoir qu'il s'agit de l'arme du meurtrier
                if self.agent.current_room.dropped_weapon is not None:
                    self.agent.discover_weapon(self.agent.current_room.dropped_weapon.value, room)


            characters = self.agent.current_room.characters.values()
            for character in characters:

                if not character.met:

                    character.met = True

                    # L'agent note la pièce dans laquelle se trouve chaque suspect ainsi que la pièce de la victime
                    if character.victim:
                        self.agent.discover_victim(character, room, current_time)
                    else:
                        self.agent.discover_character(character, room, current_time)

            # Ensuite, l'humain termine l'enquête ou déplace l'agent à la pièce suivante
            self.agent.game_io.output("Voulez-vous poursuivre l'enquête?")
            key = self.agent.game_io.inputYesNoFromTerminal().value

            if key == "2":
                continue_investigation = False
                continue

            self.agent.move()

        self.identify_murderer()

    def identify_murderer(self):

        suspect = self.agent.crime_inference.get_suspect()
        print("L'agent AI amène le(s) suspect(s) " + str(suspect) + " au poste de police pour un interrogatoire plus approfondi.")
        time.sleep(Constants.TIME_BETWEEN_DIALOG)

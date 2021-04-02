import math
import random
from typing import List

from data.data import Directions
from data.game_data import RoomTypes, CharacterTypes, WeaponTypes
from game.agent import Agent
from game.character import Character
from game.room import Room


class Board:

    BEGIN_TIME = 8

    def __init__(self, nb_rooms, nb_characters, nb_weapons):

        self.nb_rooms = nb_rooms
        self.nb_characters = nb_characters
        self.nb_weapons = nb_weapons
        self.rooms = []
        self.characters: List[Character] = []
        self.weapons = []
        self.criminal = None
        self.victim = None
        self.agent = Agent(self.rooms, self.characters, self.weapons)

        self.ticks = 0
        self.afternoon = True

    def start_game(self):

        self.generate_rooms()
        self.place_characters()
        self.place_weapons()
        self.generate_crime()
        self.agent.get_initial_facts()

        input("L'agent AI arrive sur les lieux du crime afin d'enquêter sur le meurtre. Entrez n'importe quelle touche"
                    "afin de commencer l'enquête.")

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

                if bottom_room is not None:
                    room.add_neighbour_room(bottom_room, Directions.BOTTOM)

                if left_room is not None:
                    room.add_neighbour_room(left_room, Directions.LEFT)

                self.rooms.append(room)

    def place_characters(self):

        indexes = []
        for i in range(len(self.rooms)):
            indexes.append(i)

        character_types_iter = CharacterTypes.__iter__()

        for i in range(self.nb_characters):

            index = int(random.random() * len(indexes))
            character_type = character_types_iter.__next__()
            character = Character(character_type, self.rooms[index])
            self.rooms[index].add_character(character)
            self.characters.append(character)
            indexes.pop(index)

    def place_weapons(self):

        indexes = []
        for i in range(len(self.rooms)):
            indexes.append(i)

        weapon_types_iter = WeaponTypes.__iter__()

        for i in range(self.nb_weapons):

            index = int(random.random() * len(indexes))
            weapon = weapon_types_iter.__next__()
            self.rooms[index].add_weapon(weapon)
            self.weapons.append(weapon)
            indexes.pop(index)

    # On génère les circonstances entourant le meurtre, c'est-à-dire les actions des personnages avant et après le meurtre
    def generate_crime(self):

        character_index = int(random.random() * len(self.characters))
        self.criminal = self.characters[character_index]

        weapon_taken = False
        victim_killed = False
        victim_discovered = False

        # Tant qu'une victime n'est pas découverte, les personnages se déplacent dans le manoir de manière aléatoire
        while not victim_discovered:

            hour = (self.__class__.BEGIN_TIME + self.ticks) % 12
            time = str(hour) + ":00"

            #print("L'horloge sonne " + str(hour) + " coups. Il est " + time + " heure")
            self.ticks += 1

            for character in self.characters:

                # À chaque heure, chaque personnage vivant se déplace vers une pièce adjacente
                if not character.victim:
                    character.move_to_adjacent_room()


            # Lorsque le meurtrier entre dans une pièce qui contient une arme, il récupère celle-ci
            if self.criminal.room.weapon != None and not weapon_taken:

                print("Il est {} heure. Le criminel, {}, trouve un(e) {} dans le/la {}. Il le/la ramasse avec appréhension".format(
                    time,
                    self.criminal.character_type.value,
                    self.criminal.room.weapon.value,
                    self.criminal.room.room_type.value))

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

                        print("Il est {} heure. Le criminel, {}, assassine {} avec son/sa {} dans le/la {}".format(
                            time,
                            self.criminal.character_type.value,
                            self.victim.character_type.value,
                            self.criminal.weapon.value,
                            self.criminal.room.room_type.value))
                        break

            # Lorsqu'il y a un autre personnage dans la pièce de la victime, celui-ci découvre la victime
            elif victim_killed and len(self.victim.room.characters) > 1:

                characters = self.criminal.room.characters.values()

                # Le personnage dans la pièce qui n'est pas la victime elle-même découvre la victime
                for character in characters:
                    if character.character_type is not self.victim.character_type:
                        victim_discovered = True
                        print("Il est {} heure. {} découvre le corps de {} dans le/la {}".format(
                            time,
                            character.character_type.value,
                            self.victim.character_type.value,
                            self.victim.room.room_type.value))
                        break

    def start_investigation(self):

        # TODO
        pass

import math
import random

from data.data import Directions
from data.game_data import RoomTypes, CharacterTypes, WeaponTypes
from game.room import Room


class Board:

    def __init__(self, nb_rooms, nb_characters, nb_weapons):

        self.nb_rooms = nb_rooms
        self.nb_characters = nb_characters
        self.nb_weapons = nb_weapons
        self.rooms = []
        self.characters = []
        self.weapons = []
        self.crime = None

    def generate(self):

        self.generate_rooms()
        self.place_characters()
        self.place_weapons()

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
            character = character_types_iter.__next__()
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

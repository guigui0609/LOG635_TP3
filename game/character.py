import random

from data.game_data import CharacterTypes


class Character:

    def __init__(self, character_type: CharacterTypes, room):

        self.character_type = character_type
        self.room = room
        self.weapon = None
        self.victim = False
        self.encounters = {}
        self.rooms = {}
        self.met = False

    def move_to_adjacent_room(self, time):

        self.room.characters.pop(self.character_type)
        self.room = self.room.neighbour_rooms[int(random.random() * len(self.room.neighbour_rooms))]
        self.room.characters[self.character_type] = self
        self.rooms[time] = self.room

    def encounter(self, time):
        self.encounters[time] = list(self.room.characters.values())

        # for character in self.room.characters.values():
        #               print(self.character_type.value + " encountered " + character.character_type.value + " at " + str(time) + " dans la " + self.room.room_type.value)

    def take_weapon(self):

        self.weapon = self.room.weapon
        self.room.weapon = None

    def drop_weapon(self):

        self.room.dropped_weapon = self.weapon
        self.weapon = None

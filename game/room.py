from data.data import Directions
from data.game_data import RoomTypes, WeaponTypes, CharacterTypes
from game.character import Character


class Room:

    def __init__(self, room_type: RoomTypes):

        self.room_type = room_type
        self.top_room = None
        self.right_room = None
        self.bottom_room = None
        self.left_room = None
        self.characters = {}
        self.weapon = None
        self.dropped_weapon = None
        self.neighbour_rooms = []

    def add_neighbour_room(self, neighbour_room: "Room", direction: Directions, one_way = False):

        if not one_way:
            neighbour_room.add_neighbour_room(self, direction.get_opposite_direction(), True)

        if direction == Directions.TOP:
            self.top_room = neighbour_room
        elif direction == Directions.RIGHT:
            self.right_room = neighbour_room
        elif direction == Directions.BOTTOM:
            self.bottom_room = neighbour_room
        elif direction == Directions.LEFT:
            self.left_room = neighbour_room
        else:
            raise Exception("Unexepected value for directions. Expected values : TOP, RIGHT, BOTTOM, LEFT")

        self.neighbour_rooms.append(neighbour_room)

    def get_neighbour_room(self, direction: Directions) -> "Room":

        if direction == Directions.TOP:
            return self.top_room
        elif direction == Directions.RIGHT:
            return self.right_room
        elif direction == Directions.BOTTOM:
            return self.bottom_room
        elif direction == Directions.LEFT:
            return self.left_room
        else:
            raise Exception("Unexepected value for directions. Expected values : TOP, RIGHT, BOTTOM, LEFT")

    def add_character(self, character: Character):
        self.characters[character.character_type] = character

    def add_weapon(self, weapon_type: WeaponTypes):
        self.weapon = weapon_type

    def drop_weapon(self, weapon_type: WeaponTypes):
        self.dropped_weapon = weapon_type

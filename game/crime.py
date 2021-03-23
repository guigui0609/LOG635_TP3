from data.game_data import CharacterTypes, WeaponTypes
from game.room import Room


class Crime:

    def __init__(self, room: Room, character: CharacterTypes, weapon: WeaponTypes):

        self.room = room
        self.character = character
        self.weapon = weapon

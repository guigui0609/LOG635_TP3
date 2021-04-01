import random

from game.agent import Agent
from game.board import Board
from game.crime import Crime


class Game:

    def __init__(self, nb_rooms, nb_characters, nb_weapons):

        self.board = None
        self.crime = None
        self.board = Board(nb_rooms, nb_characters, nb_weapons)
        self.agent = Agent(self.board.rooms, self.board.characters, self.board.weapons)

    def generate(self):

        self.board.generate()
        self.generate_crime()
        self.agent.get_initial_facts()

    def generate_crime(self):

        character_index = int(random.random() * len(self.board.characters))
        character = self.board.characters[character_index]

        weapon_index = int(random.random() * len(self.board.weapons))
        weapon = self.board.weapons[weapon_index]

        index = int(random.random() * len(self.board.rooms))
        room = self.board.rooms[index]

        self.crime = Crime(character, weapon, room)

from data.constants import Constants
from game.board import Board

board = Board(Constants.NB_ROOMS, Constants.NB_CHARACTERS, Constants.NB_WEAPONS)
board.start_game()

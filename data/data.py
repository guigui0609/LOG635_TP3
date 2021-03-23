from enum import Enum


class Directions(Enum):

    TOP = "Top"
    RIGHT = "Right"
    BOTTOM = "Bottom"
    LEFT = "Left"

    def get_opposite_direction(self):

        if self == Directions.TOP:
            return Directions.BOTTOM
        elif self == Directions.BOTTOM:
            return Directions.TOP
        elif self == Directions.LEFT:
            return Directions.RIGHT
        elif self == Directions.RIGHT:
            return Directions.LEFT
        else:
            raise Exception("Unexepected value for directions. Expected values : TOP, RIGHT, BOTTOM, LEFT")

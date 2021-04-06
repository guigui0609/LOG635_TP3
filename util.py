from data.data import Directions


class Util:

    @staticmethod
    def convert_key_to_direction(key):

        key = str.lower(key)

        if key == "top":
            return Directions.TOP
        elif key == "left":
            return Directions.LEFT
        elif key == "bottom":
            return Directions.BOTTOM
        elif key == "right":
            return Directions.RIGHT
        else:
            return None
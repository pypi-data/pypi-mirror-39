from enum import Enum, auto
class Commands(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    BITELEFT = auto()
    BITERIGHT = auto()
    BITEUP = auto()
    BITEDOWN = auto()
    SPLIT = auto()
    MERGE = auto()

    def is_move(self):
        return self in (Commands.LEFT, Commands.RIGHT, Commands.UP, Commands.DOWN)

    def is_bite(self):
        return self in (Commands.BITELEFT, Commands.BITERIGHT, Commands.BITEUP, Commands.BITEDOWN)

    def update_coord(self, x, y):
        """Returns x,y updated based on the direction of the command"""
        if self in (Commands.UP, Commands.BITEUP):
            y += 1
        elif self in (Commands.DOWN, Commands.BITEDOWN):
            y -= 1
        elif self in (Commands.RIGHT, Commands.BITERIGHT):
            x += 1
        elif self in (Commands.LEFT, Commands.BITELEFT):
            x -= 1
        return (x, y)
import random
from slime_mind.models.commands import Commands

class PlayerBase():
    """ Base class player's must implement """ 
    def __init__(self, id, name, image_1='default', image_2='default'):
      self.id = id
      self.name = name
      self.image_1 = image_1
      self.image_2 = image_2

    def command_slime(self, map, slime, turn):
        """
          Player's should override this method to provide an AI for each slime they control.
          They must return a Command for the slime to take.
          Invalid or impossible commands (e.g. moving onto a taken coordinate or eating nothing) will be ignored.
        """
        # default implementation is a random selection from all commands
        return random.choice(list(Commands))
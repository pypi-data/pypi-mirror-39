import random
import math
import logging
from slime_mind.engine.plant import Plant
from slime_mind.engine.slime import Slime

class Sprite_man():
    def __init__(self, map, config):
        self.map = map
        self.conf = config

    def check_for_dead(self):
        for x in range(self.map.columns):
            for y in range(self.map.rows):
                gamepiece = self.map.get(x, y)
                if type(gamepiece) is Plant or type(gamepiece) is Slime:
                    if gamepiece.current_hp <= 0:
                        self.map.clear_cell(gamepiece.x,gamepiece.y)

    def check_for_merge(self):
        for x in range(self.map.columns):
            for y in range(self.map.rows):
                gamepiece = self.map.get(x, y)
                if type(gamepiece) is Slime and gamepiece.ready_to_merge:
                    for x, y in self.map.adjacent_cells(gamepiece.x, gamepiece.y):
                        neighbor = self.map.get(x, y)
                        if type(neighbor) is Slime and neighbor.ready_to_merge and gamepiece.player_id == neighbor.player_id:
                            logging.getLogger().info('%s merged with %s', gamepiece.id, neighbor.id)
                            gamepiece.xp = math.floor(1.5 * (gamepiece.xp + neighbor.xp))
                            # kill the merged neighbor
                            self.map.clear_cell(neighbor.x, neighbor.y)

    def spread_seeds(self):
        for x in range(self.map.columns):
            for y in range(self.map.rows):
                gamepiece = self.map.get(x, y)
                if type(gamepiece) is Plant and gamepiece.can_seed():
                    empty_adjacent_cells = self.map.adjacent_empty_cells(gamepiece.x, gamepiece.y)

                    # can't seed if there are no available cells
                    if len(empty_adjacent_cells) == 0:
                        continue

                    level_up_chance = random.randint(0, self.conf['Plant'].getint('seed_chance'))
                    if level_up_chance == 0:
                        x, y = random.choice(empty_adjacent_cells)
                        plant = Plant(self.conf['Plant'])
                        self.map.move_gamepiece(plant, x, y)

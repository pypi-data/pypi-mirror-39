import arcade
from random import choice
from os import listdir

from slime_mind.runners.runner_base import RunnerBase
from slime_mind.engine.engine import Engine
from slime_mind.visualizer.visualizer import Visualizer

class Runner(RunnerBase): 
    def __init__(self, player_dir, ai_one_filename=None, ai_two_filename=None):
        super().__init__("single_match", player_dir)
        self.ai_one_filename = ai_one_filename
        self.ai_two_filename = ai_two_filename

    def choose_player(self):
        """ randomly choose a player """
        players = [f for f in listdir(self.player_dir) if '.py' in f]
        return choice(players)

    def run(self):
        if self.ai_one_filename is None:
            self.ai_one_filename = self.choose_player()
        player_one = self.create_player(self.ai_one_filename, 1)
        
        if self.ai_two_filename is None:
            self.ai_two_filename = self.choose_player()
        player_two = self.create_player(self.ai_two_filename, 2)

        engine = Engine(self.config, player_one, player_two)

        # visualize or just run the match
        if self.config['visualizer'].getboolean('render'):
            visualizer = Visualizer(self.config, engine.map.dump_state(), engine.run_turn, player_one.name, player_two.name)
            arcade.window_commands.run()
        else:
            while not engine.is_game_over():
                engine.run_turn()

        results = engine.end_game()
        self.record_results(results)

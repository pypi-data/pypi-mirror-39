import arcade
from random import sample
from os import listdir

from slime_mind.runners.runner_base import RunnerBase
from slime_mind.visualizer.visualizer import Visualizer

class Runner(RunnerBase): 
    def __init__(self, player_dir, filename):
        super().__init__("visualize_recording", player_dir)
        self.player_1_name, self.player_2_name = self.get_player_names(filename)
        with open(filename, 'r') as f:
            self.recording = f.readlines()
        self.i = 0

    def get_player_names(self, filename):
        # remove .txt
        filename = filename[:-4]
        # remove /recordings
        filename = filename.split('/')[2]
        # split out the two players
        parts = filename.split('__')
        player_one = parts[1].replace("-", " ")
        player_two = parts[-1].replace("-", " ")

        return (player_one, player_two)

    def next_state(self):
        data = False
        if self.i < len(self.recording):
            data = eval(self.recording[self.i])
        self.i+= 1
        return data

    def run(self):
        visualizer = Visualizer(self.config, self.next_state(), self.next_state, self.player_1_name, self.player_2_name)
        arcade.window_commands.run()
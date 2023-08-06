import arcade
import csv
from random import sample
from os import path
from collections import defaultdict

from slime_mind.runners.runner_base import RunnerBase
from slime_mind.engine.engine import Engine
from slime_mind.visualizer.visualizer import Visualizer

class Runner(RunnerBase): 
    def __init__(self, player_dir, matches, ai_one_filename, ai_two_filename):
        super().__init__("multi_match", player_dir)
        self.matches = matches
        self.ai_one_filename = ai_one_filename
        self.ai_two_filename = ai_two_filename

    def record_results(self, results):
        stats = defaultdict(int)
        for match in results:
            stats[match['winner']]+= 1

        winner = ['tie', 0]
        for k, v in stats.items():
            print(k, v)
            if v > winner[1]:
                winner[0] = k
                winner[1] = v
        print(f"Overall winner: {winner[0]} - won {winner[1]} / {len(results)} matches")

        existing_file = path.isfile('results.csv')
        for match in results:
            with open('results.csv', 'a', newline = '') as f:
                writer = csv.DictWriter(f, fieldnames = match.keys())
                if not existing_file:
                    writer.writeheader()
                writer.writerow(match)

    def run(self):
        results = []
        for match in range(1, self.matches + 1):
            print(f"match #{match}")
            if match % 2 == 0:
                player_one = self.create_player(self.ai_one_filename, 1)
                player_two = self.create_player(self.ai_two_filename, 2)
            else:
                player_one = self.create_player(self.ai_two_filename, 1)
                player_two = self.create_player(self.ai_one_filename, 2)

            engine = Engine(self.config, player_one, player_two)
            while not engine.is_game_over():
                engine.run_turn()

            results.append(engine.end_game())
        self.record_results(results)

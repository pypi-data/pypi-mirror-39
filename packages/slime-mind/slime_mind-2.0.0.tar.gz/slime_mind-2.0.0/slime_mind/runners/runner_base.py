import logging
import configparser
import importlib.util
import csv
from os import path
from pkg_resources import resource_filename

class RunnerBase(): 
    def __init__(self, name, player_dir):
        self.name = name
        self.player_dir = player_dir
        self.config = configparser.ConfigParser()
        config_path = resource_filename('slime_mind', "resources/config.ini")
        self.config.read(config_path)

        # setup logging
        logger = logging.getLogger()
        logger.setLevel(self.config['logging']['level'])
        logger.addHandler(logging.StreamHandler())

    def create_player(self, filename, player_num):
        spec = importlib.util.spec_from_file_location("PlayerCode.Player", self.player_dir + '/' + filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Player(player_num)

    def record_results(self, results):
        for k, v in results.items():
            print(k, v)

        existing_file = path.isfile('results.csv')

        with open('results.csv', 'a', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames = results.keys())
            if not existing_file:
                writer.writeheader()
            writer.writerow(results)

    def run(self):
        raise NotImplementedError("All runners must implement this method")

    def choose_players(self):
        raise NotImplementedError("All runners must implement this method")
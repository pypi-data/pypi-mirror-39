import random
import time
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from itertools import zip_longest

from slime_mind.engine.plant import Plant
from slime_mind.engine.slime import Slime
from slime_mind.engine.rock import Rock
from slime_mind.engine.map import Map
from slime_mind.engine.sprite_man import Sprite_man
from slime_mind.engine.game_recorder import GameRecorder
from slime_mind.models.commands import Commands

def run_with_timeout(func, timeout, *args):
    """ Execute a function with a timeout """
    # NOTE: this abandons the thread, so it will continue to run to completion, we just ignore the result
    with ThreadPoolExecutor() as thread:
        future = thread.submit(func, *args)
        
        try:
            return future.result(timeout = timeout)
        except TimeoutError as e:
            print(f"player timed out")
            return None
        except:
            print("player errorred out")
            traceback.print_exc()
            return None

class Engine():
    """ Main application class. """

    def __init__(self, config, player_one, player_two):
        print(f"{player_one.name} vs {player_two.name}")
        # config
        self.conf = config
        self.max_turns = config['screen'].getint('max_turns')

        # initial game state
        self.map = Map(config)
        self.sprite_man = Sprite_man(self.map, self.conf)
        self.turn = 0
        self.player_one = player_one
        self.player_two = player_two
        self.game_recorder = GameRecorder(config, player_one.name, player_two.name)
        # start at one so we don't immediately end TODO: track this in a better way
        self.player_one_slime_count = 1
        self.player_two_slime_count = 1

        # place initial gamepieces
        self.place_pieces(self.conf['Slime'].getint('num_total'), 'SLIME')
        self.place_pieces(self.conf['Plant'].getint('num_total'), 'PLANT')
        self.place_pieces(self.conf['Rock'].getint('num_total'), 'ROCK')

    def create_piece(self, piece_type, player = None):
        if piece_type == 'SLIME':
            return Slime(self.conf['Slime'], player)
        elif piece_type == 'PLANT':
            return Plant(self.conf['Plant'])
        elif piece_type == 'ROCK':
            return Rock()

    def place_pieces(self, number, piece_type):
        pieces = 0
        while pieces < number: 
            x = random.randint(0, self.map.columns / 2 - 1)
            y = random.randint(0, self.map.rows - 1)
            if self.map.is_cell_empty(x, y):
                # left half
                piece = self.create_piece(piece_type, self.player_one)
                self.map.move_gamepiece(piece, x, y)

                # mirrored across x and y axis for right half
                x = (self.map.columns - 1) - x
                y = (self.map.rows - 1) - y
                piece = self.create_piece(piece_type, self.player_two)
                self.map.move_gamepiece(piece, x, y)

                pieces += 2

    def bite_thing(self, command, x, y, attack):
        # Slime tries to bite a target, then if successful this method awards 1 xp
        (x, y) = command.update_coord(x, y)
        if not self.map.valid_coord(x, y):
            return 0

        target = self.map.get(x, y)

        if target is None or type(target) is Rock:
            return 0

        target.current_hp -= attack
        return 1 if type(target) is Slime else 2

    def split(self, slime):
        """ split slime into random empty adjacent cell """
        empty_adjacent_cells = self.map.adjacent_empty_cells(slime.x, slime.y)

        # can't split if there are no available cells
        if len(empty_adjacent_cells) == 0:
            return
        
        # can't split if the slime is not high enough level
        if slime.level >= self.conf['Slime'].getint('min_split_level'):
            x, y = random.choice(empty_adjacent_cells)
            slime.split()

            new_slime = self.create_piece('SLIME', slime.player)
            self.map.move_gamepiece(new_slime, x, y)

    def end_game(self):
        """ Return results of the match """
        results = {}
        results['player one team name'] = self.player_one.name
        results['player one score'] = 0
        results['player one max slime level'] = 0
        results['player one slime count'] = 0
        results['player two team name'] = self.player_two.name
        results['player two score'] = 0
        results['player two max slime level'] = 0
        results['player two slime count'] = 0
        results['winner'] = 'tie'
        results['final turn'] = self.turn

        for x in range(self.map.columns):
            for y in range(self.map.rows):
                slime = self.map.get(x, y)
                if type(slime) is Slime:
                    if slime.player_id == 1:
                        results['player one slime count'] += 1
                        results['player one score'] += (slime.level**(3.8)-slime.level**3.7+1)/5
                        if results['player one max slime level'] < slime.level:
                            results['player one max slime level'] = slime.level

                    if slime.player_id == 2:
                        results['player two slime count'] += 1
                        results['player two score'] += (slime.level**(3.8)-slime.level**3.7+1)/5
                        if results['player two max slime level'] < slime.level:
                            results['player two max slime level'] = slime.level

        if results['player one score'] > results['player two score']:
            results['winner'] = self.player_one.name
        elif results['player one score'] < results['player two score']:
            results['winner'] = self.player_two.name
        return results

    def execute_round(self, slime, player):
        # provide player with read-only copy of state so they can't cheat
        state = self.map.dump_state()
        command = run_with_timeout(player.command_slime, self.conf['engine'].getfloat('round_max_time'), state, state[slime.x][slime.y], self.turn)

        # if they error, timeout, or just want to do nothing
        if command is None:
            return

        # for any Enum member
        if not isinstance(command, Commands):
            print('Player', player.id, 'tried to command a slime to', command, '. This is an invalid command!')
            return

        # Check for move commands
        if command.is_move():
            # Attempt to move the slime if the target cell is empty
            (x, y) = command.update_coord(slime.x, slime.y)
            if self.map.valid_coord(x, y) and self.map.is_cell_empty(x, y):
                self.map.move_gamepiece(slime, x, y)

        # Check for bite commands
        if (command.is_bite()):
            # Attempt to bite things
            hit = self.bite_thing(command, slime.x, slime.y, slime.attack)
            #print('if 1 then hit', hit)
            if hit:
                slime.xp += 1
                hit -= 1
                if hit:
                    if slime.current_hp < slime.max_hp:
                        slime.current_hp += 1

        if command is Commands.SPLIT:
            self.split(slime)

        if command is Commands.MERGE:
            slime.ready_to_merge = True

        # update state
        slime.update()
        self.sprite_man.check_for_dead()
        self.sprite_man.check_for_merge()

    def get_slimes(self):
        """ return all slimes on the map """
        # get slimes
        slime_list_1 = []
        slime_list_2 = []
        for x in range(self.map.columns):
            for y in range(self.map.rows):
                gamepiece = self.map.get(x, y)
                if type(gamepiece) is Slime:
                    if gamepiece.player_id == 1:
                        slime_list_1.append(gamepiece)
                    else:
                        slime_list_2.append(gamepiece)
        # alternate between player 1 and player 2 slimes
        slimes_zip = zip_longest(slime_list_1, slime_list_2)
        # flatten and remove filler None
        return [item for subtuple in slimes_zip for item in subtuple if item is not None]

    def run_turn(self):
        """ Movement and game logic """
        if self.is_game_over():
            return False
        # Turn counter
        self.turn += 1

        # level up plants
        for x in range(self.map.columns):
            for y in range(self.map.rows):
                gamepiece = self.map.get(x, y)
                if type(gamepiece) is Plant:
                    gamepiece.update()

        # check to see if the plants spread seeds
        # TODO: combine this with leveling up to remove an unnecessary map iteration
        self.sprite_man.spread_seeds()

        # execute player AI for each slime
        self.player_one_slime_count = 0
        self.player_two_slime_count = 0

        # get current state of the world
        slimes = self.get_slimes()
        while len(slimes) > 0:
            slime = slimes.pop(0)
            # do not run for dead slimes
            if not self.map.is_cell_empty(slime.x, slime.y):
                if slime.player_id == 1:
                    self.execute_round(slime, self.player_one)
                    self.player_one_slime_count += 1
                if slime.player_id == 2:
                    self.execute_round(slime, self.player_two)
                    self.player_two_slime_count += 1

        # track state for later visualization
        state = self.map.dump_state()
        self.game_recorder.write_state_to_file(state)
        return state

    def is_game_over(self):
        # Check for end of game conditions
        return self.turn >= self.max_turns or self.player_one_slime_count == 0 or self.player_two_slime_count == 0

import arcade
import random
import os
import time
import logging
import csv

from slime_mind.visualizer.plant_sprite import PlantSprite
from slime_mind.visualizer.slime_sprite import SlimeSprite
from slime_mind.visualizer.rock_sprite import RockSprite
from slime_mind.timer.timer import turn_timer

class Visualizer(arcade.Window):
    """ Main application class. """

    def __init__(self, config, initial_state, get_state, player_1_name, player_2_name):
        super().__init__(config['screen'].getint('width'),
                         config['screen'].getint('height'),
                         "SlimeMind")
        # config
        self.conf = config
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height')
        self.rows = config['screen'].getint('rows')
        self.columns = config['screen'].getint('columns')
        self.step_x = self.width // self.columns
        self.step_y = self.height // self.rows
        self.do_draw_grid = config['screen'].getboolean('draw_grid')
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name

        # initial game state
        self.all_sprites_list = arcade.SpriteList(use_spatial_hash=False)
        self.turn = 0
        self.start = 0
        self.get_state = get_state
        # initialize sprites
        for piece in self.flatten_state(initial_state):
            self.add_sprite(piece)

    def set_sprite_position(self, sprite, x, y):
        center_x = (x + 1/2) * self.step_x
        center_y = (y + 1/2) * self.step_y
        if self.turn == 0 or sprite.center_x != center_x or sprite.center_y != center_y:
            sprite.set_position(center_x, center_y)

    def flatten_state(self, state):
        flat = []
        for x in range(len(state)):
            for y in range(len(state[x])):
                piece = state[x][y]
                if piece is not None:
                    flat.append(piece)
        return flat

    def hashify_state(self, state):
        flat = self.flatten_state(state)
        state_dict = {}
        for piece in flat:
            state_dict[piece['id']] = piece
        return state_dict

    def add_sprite(self, piece):
        if piece['type'] == 'PLANT':
            sprite = PlantSprite(self.conf, piece['id'])
            self.set_sprite_position(sprite, piece['x'], piece['y'])
        elif piece['type'] == 'SLIME':
            sprite = SlimeSprite(self.conf, piece)
            self.set_sprite_position(sprite, piece['x'], piece['y'])
        elif piece['type'] == 'ROCK':
            sprite = RockSprite(self.conf, piece['id'])
            self.set_sprite_position(sprite, piece['x'], piece['y'])
        else:
            raise Exception("Unrecognized piece type")
        self.all_sprites_list.append(sprite)

    def draw_grid(self):
        if self.do_draw_grid:
            for row in range(self.rows):
                for column in range(self.columns):
                    # Figure out what color to draw the box
                    color = arcade.color.BLACK

                    # Do the math to figure out where the box is
                    x_box = (self.width/self.columns) * (column) + (self.width/self.columns)/2
                    y_box = (self.height/self.rows) * (row) + (self.height/self.rows)/2

                    # Draw the box
                    arcade.draw_rectangle_outline(x_box, y_box, self.width/self.columns-2, self.height/self.rows-2, color, 4)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        self.draw_grid()
        self.all_sprites_list.draw()

        plant_number = 0
        rock_number = 0
        slime_number = 0

        for sprite in self.all_sprites_list:
            if type(sprite) is PlantSprite:
                plant_number += 1
            if type(sprite) is RockSprite:
                rock_number += 1
            if type(sprite) is SlimeSprite:
                slime_number += 1

        # Put the text on the screen.
        elapsed = time.perf_counter() - self.start
        self.start = time.perf_counter()
        output = f"turn: {self.turn} seconds since last turn: {elapsed}"
        #print(f"full_turn,{self.turn},timer,{round(elapsed,5)}, Number of plants,{plant_number}, rocks,{rock_number}, slimes,{slime_number},")
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

        # Put code team names on the screens
        arcade.draw_text(self.player_1_name, 10, self.height - 20, arcade.color.BLACK, 14)
        arcade.draw_text(self.player_2_name, self.width - 200, self.height - 20, arcade.color.BLACK, 14)

        # Delay to slow game down        
        time.sleep(self.conf['visualizer'].getfloat('sleep'))

    def update_texture_and_position(self, sprite, state_dict):
        """Moves and updates textures of a sprite based on state"""
        # rocks never change
        if type(sprite) is RockSprite:
            return

        piece = state_dict[sprite.id]
        # update textures based on level
        sprite.update_texture(piece)

        # movement
        if type(sprite) is SlimeSprite:
            self.set_sprite_position(sprite, piece['x'], piece['y'])

    def add_new_sprites(self, state_dict):
        ids = [sprite.id for sprite in self.all_sprites_list]
        to_add = [piece for piece in state_dict.values() if piece['id'] not in ids]
        for piece in to_add:
            self.add_sprite(piece)

    def kill_missing_sprites(self, state_dict):
        to_kill = [sprite for sprite in self.all_sprites_list if sprite.id not in state_dict]
        for sprite in to_kill:
            sprite.kill()

    def update_positions(self, state_dict):
        for sprite in self.all_sprites_list:
            if type(sprite) is SlimeSprite:
                piece = state_dict[sprite.id]
                self.set_sprite_position(sprite, piece['x'], piece['y'])

    def update_textures(self, state_dict):
        for sprite in self.all_sprites_list:
            if type(sprite) is not RockSprite:
                piece = state_dict[sprite.id]
                sprite.update_texture(piece)

    def update(self, delta_time):
        """ Movement and game logic """
        state = self.get_state()

        # stop visualizing when there's no more state to render
        if state is False:
            arcade.window_commands.close_window()
            return

        # Turn counter
        self.turn += 1
        state_dict = self.hashify_state(state)

        self.add_new_sprites(state_dict)

        self.kill_missing_sprites(state_dict)

        self.update_positions(state_dict)

        self.update_textures(state_dict)

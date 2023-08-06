import random
import arcade
from PIL import Image
from pkg_resources import resource_filename 

class PlantSprite(arcade.Sprite):
    def __init__(self, config, id):
        self.conf = config
        self.max_level = config['Plant'].getint('max_level')
        self.filename = resource_filename('slime_mind', self.conf['Plant'].get('filename1'))
        self.low_filename = self.conf['Plant'].get('filename1')
        self.high_filename = self.conf['Plant'].get('filename2')
        self.id = id
        im = Image.open(self.filename)
        width, height = im.size
        self.scale_adj = (config['screen'].getfloat('width')/config['screen'].getfloat('columns'))/(width)*1.2
        super().__init__(self.filename, self.scale_adj)

    def update_texture(self, piece):
        if piece['level'] < self.max_level * 3 // 4:
            filename = self.low_filename
        else:
            filename = self.high_filename
        filename = resource_filename('slime_mind', filename)
        # only load texture on changes
        if self.filename != filename:
            self.filename = filename
            self.texture = arcade.draw_commands.load_texture(filename, scale = self.scale_adj)

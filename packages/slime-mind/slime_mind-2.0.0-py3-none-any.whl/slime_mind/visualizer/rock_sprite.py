import arcade
from PIL import Image
from pkg_resources import resource_filename 

class RockSprite(arcade.Sprite):
    def __init__(self, config, id):
        filename = resource_filename('slime_mind', config['Rock'].get('filename1'))
        im = Image.open(filename)
        width, height = im.size
        scale_adj = (config['screen'].getfloat('width') / config['screen'].getfloat('columns')) / (width) * 1.1
        super().__init__(filename, scale_adj)
        self.id = id
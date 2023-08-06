import arcade
from PIL import Image
from pkg_resources import resource_filename 

class SlimeSprite(arcade.Sprite):
    def __init__(self, config, piece):
        self.conf = config
        self.filename = self.choose_texture(piece)
        self.id = piece['id']
        im = Image.open(self.filename)
        width, height = im.size
        self.scale_adj = (config['screen'].getfloat('width')/config['screen'].getfloat('columns'))/(width)*1.2
        super().__init__(self.filename, self.scale_adj)

    def choose_texture(self, piece):
        if piece['level'] <10:
            if piece['image_1'] == 'default':
                if piece['player_id'] == 1:
                    filename = resource_filename('slime_mind', self.conf['Slime'].get('player_one_basic'))
                else:
                    filename = resource_filename('slime_mind', self.conf['Slime'].get('player_two_basic'))
            else:
                filename = piece['image_1']
        else:
            if piece['image_2'] == 'default':
                if piece['player_id'] == 1:
                    filename = resource_filename('slime_mind', self.conf['Slime'].get('player_one_king'))
                else:
                    filename = resource_filename('slime_mind', self.conf['Slime'].get('player_two_king'))
            else:
                filename = piece['image_2']
        return filename

    def update_texture(self, piece):
        """Update the slimes sprites based on player and level."""
        filename = self.choose_texture(piece)
        # only load texture on changes
        if self.filename != filename:
            self.filename = filename
            self.texture = arcade.draw_commands.load_texture(filename, scale = self.scale_adj)
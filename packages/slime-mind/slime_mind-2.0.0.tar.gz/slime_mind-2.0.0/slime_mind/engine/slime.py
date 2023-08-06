import uuid

class Slime():
    def __init__(self, config, player):
        self.id = str(uuid.uuid4())
        self.player_id = player.id
        self.player = player
        self.x = None
        self.y = None
        self.conf = config
        self.level = 1
        self.xp = 1
        self.max_level = config.getint('max_level')

        self.hp_exponent = config.getfloat('hp_exponent')
        self.hp_base = config.getint('hp_base')
        self.max_hp = self.hp_base
        self.current_hp =config.getint('hp_base')

        self.attack_exponent = config.getfloat('attack_exponent')
        self.attack_base = config.getint('attack_base')
        self.attack =config.getint('attack_base')

        self.min_split_level = config.getint('min_split_level')
        self.ready_to_merge = False

    def update(self):
        self.level_check()

    def split(self):
        self.xp = self.xp // 4

    def max_hp_check(self, level):
        return (level**self.hp_exponent) + self.hp_base

    def level_check(self):
        # Save current level
        starting_level = self.level

        # Update level based on xp
        self.level = int(1.847*self.xp**0.286)

        # Check if the slime level is at or above maximum
        if self.level >= self.max_level:
            self.level = self.max_level

        # Update attack based on level
        self.attack = self.level**self.attack_exponent+self.attack_base

        # Add hp on level up
        if starting_level < self.level:
            # Update max_hp
            self.max_hp = self.max_hp_check(self.level)

            if self.max_hp > self.max_hp_check(starting_level):
                self.current_hp += (self.max_hp - self.max_hp_check(starting_level))
                # make sure current hp isn't above max hp
                if self.current_hp >= self.max_hp:
                    self.current_hp = self.max_hp

    def __dict__(self):
        return {
            'type': 'SLIME',
            'image_1': self.player.image_1,
            'image_2': self.player.image_2,
            'id': self.id,
            'player_id': self.player_id,
            'x': self.x,
            'y': self.y,
            'level': self.level,
            'xp': self.xp,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp_check(self.level),
            'attack': self.attack,
            'ready_to_merge': self.ready_to_merge
        }

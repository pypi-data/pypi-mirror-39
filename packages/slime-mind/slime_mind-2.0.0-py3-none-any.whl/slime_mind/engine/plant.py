import random
import uuid

class Plant():
    def __init__(self, config):
        self.id = str(uuid.uuid4())
        self.x = None
        self.y = None
        self.conf = config
        self.level = 1
        self.max_hp = config.getint('max_hp')
        self.current_hp = self.max_hp
        self.max_level = config.getint('max_level')
        self.hp_increment = config.getint('hp_increment')

    def update(self):
        self.level_up()

    def level_up(self):
        # Check if the plant levels up
        do_level_up = 0

        level_up_chance = random.randint(0,self.conf.getint('level_up_chance_one'))
        if level_up_chance == 0:
            level_up_chance = random.randint(0,self.max_level + self.conf.getint('level_up_chance_two'))
            if level_up_chance > self.level and self.level < self.max_level:
                do_level_up = 1

        # If the plant levels up do the following
        if do_level_up:
            self.level += 1

            # Change max hp on level up
            self.max_hp += self.hp_increment

            # Add hp on level up, not exceeding max
            self.current_hp = min(self.current_hp + self.max_hp//2, self.max_hp)

    def reset_level(self):
        self.level = 1
        self.max_hp = self.conf.getint('max_hp')
        self.current_hp = self.max_hp

    def can_seed(self):
        return self.level == self.max_level

    def __dict__(self):
        return {
            'type': 'PLANT',
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'level': self.level,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp,
            'can_seed': self.can_seed()
        }


import datetime

class GameRecorder():
    def __init__(self, config, player_one_name, player_two_name, filename=None):
        self.record_state = config['engine'].getboolean('record_state')
        if filename is None:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')
            player_one = player_one_name.replace(" ", "-")
            player_two = player_two_name.replace(" ", "-")
            self.filename = f"./recordings/{timestamp}__{player_one}__vs__{player_two}.txt"
        else:
            self.filename = filename

    def write_state_to_file(self, state):
        if self.record_state:
            with open(self.filename, 'a+') as f:
                f.write(f"{str(state)}\n")

    def read_state_from_file(self):
        pass
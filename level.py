class Level():
    def __init__(self):
        self.level_number = 1
        self.load_next()

    def load_next(self):
        with open(f'./levels/level{self.level_number}.txt', 'r') as f:
            self.board = [list(map(int, line.split(', '))) for line in f.readlines()]

    def increase(self):
        if self.level_number < 3:
            self.level_number += 1
            self.load_next()
        else:
            self.board = None


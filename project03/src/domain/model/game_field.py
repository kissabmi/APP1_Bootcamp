class GameField:
    SIZE = 3
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2

    def __init__(self, field=None):
        if field is None:
            self.field = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        else:
            self.field = field

    def get_cell(self, row, col):
        return self.field[row][col]

    def set_cell(self, row, col, value):
        self.field[row][col] = value

    def is_empty(self, row, col):
        return self.field[row][col] == self.EMPTY

    def get_field(self):
        return self.field
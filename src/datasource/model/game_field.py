class GameField:
    #хранилище работает со своим полем (отдельно от domain)
    #чтобы слои не зависели друг от друга напрямую
    SIZE = 3
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2

    def __init__(self, field=None):
        if field is None:
            self.field = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        else:
            self.field = field

    def get_field(self):
        return self.field
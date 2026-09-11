from src.datasource.model.game_field import GameField


class CurrentGame:
    #текущая игра в хранилище — просто id + поле
    def __init__(self, game_field=None, game_id=None):
        if game_field is None:
            self.game_field = GameField()
        else:
            self.game_field = game_field
        self.game_id = game_id

    def get_field(self):
        return self.game_field

    def get_id(self):
        return self.game_id
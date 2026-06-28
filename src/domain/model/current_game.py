import uuid
from src.domain.model.game_field import GameField


class CurrentGame:
    def __init__(self, game_field=None, game_id=None):
        if game_field is None:
            self.game_field = GameField()
        else:
            self.game_field = game_field
        if game_id is None:
            self.game_id = str(uuid.uuid4())
        else:
            self.game_id = game_id

    def get_field(self):
        return self.game_field

    def get_id(self):
        return self.game_id
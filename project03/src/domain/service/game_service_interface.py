from src.domain.model.current_game import CurrentGame


class GameServiceInterface:

    def get_next_move(self, current_game):
        # возвращает текущую игру с ходом компьютера
        raise NotImplementedError

    def validate_field(self, current_game, previous_game):
        # проверяет что предыдущие ходы не изменены
        raise NotImplementedError

    def check_game_over(self, current_game):
        # проверяет окончание игры
        raise NotImplementedError
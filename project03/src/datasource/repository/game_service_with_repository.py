from src.domain.model.current_game import CurrentGame
from src.domain.model.game_field import GameField
from src.domain.service.game_service_impl import GameService
from src.datasource.repository.game_repository import GameRepository


class GameServiceWithRepository(GameService):
    #тот же сервис но теперь он дёргает репозиторий чтобы брать/сохранять игру
    def __init__(self, repository):
        self._repository = repository

    def save_game(self, current_game):
        self._repository.save(current_game)

    def get_game(self, game_id):
        return self._repository.get(game_id)
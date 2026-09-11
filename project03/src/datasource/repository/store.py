import threading
from src.datasource.model.current_game import CurrentGame


class Store:
    #потокобезопасное хранилище игр
    #dict + lock чтобы несколько потоков сразу не ломали данные
    def __init__(self):
        self._games = {}
        self._lock = threading.Lock()

    def save(self, game):
        with self._lock:
            self._games[game.get_id()] = game

    def get(self, game_id):
        with self._lock:
            return self._games.get(game_id)

    def exists(self, game_id):
        with self._lock:
            return game_id in self._games
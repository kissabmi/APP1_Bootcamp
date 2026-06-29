from src.datasource.repository.store import Store
from src.datasource.repository.game_repository import GameRepository
from src.datasource.repository.game_service_with_repository import GameServiceWithRepository
from src.web.route.game_controller import create_app


class Container:
    #граф зависимостей — кто кому нужен
    #store -> repository -> service -> app
    def __init__(self):
        #хранилище одно на всё приложение (singleton)
        self._store = None
        self._repository = None
        self._service = None
        self._app = None

    def get_store(self):
        if self._store is None:
            self._store = Store()
        return self._store

    def get_repository(self):
        if self._repository is None:
            self._repository = GameRepository(self.get_store())
        return self._repository

    def get_service(self):
        if self._service is None:
            self._service = GameServiceWithRepository(self.get_repository())
        return self._service

    def get_app(self):
        if self._app is None:
            self._app = create_app(self.get_service())
        return self._app
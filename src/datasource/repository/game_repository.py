from src.domain.model.current_game import CurrentGame as DomainGame
from src.datasource.mapper.ds_mapper import to_datasource, to_domain
from src.datasource.repository.store import Store


class GameRepository:
    #репозиторий работает с domain-игрой, а внутрь ходит в store через маппер
    def __init__(self, store):
        self._store = store

    def save(self, domain_game):
        #сохраняем — маппим в datasource и кладём в store
        ds_game = to_datasource(domain_game)
        self._store.save(ds_game)

    def get(self, game_id):
        #достаём из store и маппим обратно в domain
        ds_game = self._store.get(game_id)
        if ds_game is None:
            return None
        return to_domain(ds_game)

    def exists(self, game_id):
        return self._store.exists(game_id)
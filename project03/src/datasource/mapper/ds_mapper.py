from src.domain.model.game_field import GameField as DomainField
from src.domain.model.current_game import CurrentGame as DomainGame
from src.datasource.model.game_field import GameField as DatasourceField
from src.datasource.model.current_game import CurrentGame as DatasourceGame


def to_datasource(domain_game):
    #domain -> datasource
    field = [row[:] for row in domain_game.get_field().get_field()]
    return DatasourceGame(DatasourceField(field), domain_game.get_id())


def to_domain(datasource_game):
    #datasource -> domain
    field = [row[:] for row in datasource_game.get_field().get_field()]
    return DomainGame(DomainField(field), datasource_game.get_id())
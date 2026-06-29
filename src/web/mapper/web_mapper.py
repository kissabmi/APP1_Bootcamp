from src.domain.model.game_field import GameField as DomainField
from src.domain.model.current_game import CurrentGame as DomainGame
from src.web.model.game_field import GameField as WebField
from src.web.model.current_game import CurrentGame as WebGame


def to_domain(web_game):
    #web -> domain (пришёл json от игрока)
    field = [row[:] for row in web_game.get_field().get_field()]
    return DomainGame(DomainField(field), web_game.get_id())


def to_web(domain_game):
    #domain -> web (отдаём ответ)
    field = [row[:] for row in domain_game.get_field().get_field()]
    return WebGame(WebField(field), domain_game.get_id() if domain_game else None)
import os
import sys

#чтобы `python src/main.py` тоже работал (а не только `python -m src.main`)
#добавляем корень репо в path чтобы нашёлся пакет src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.di.container import Container

if __name__ == "__main__":
    #собираем граф зависимостей и запускаем сервер
    container = Container()
    app = container.get_app()

    from src.domain.model.current_game import CurrentGame
    from src.domain.model.game_field import GameField
    for gid in ["abc", "game2"]:
        container.get_service().save_game(CurrentGame(GameField(), gid))
    print("starter games ready: id=abc, id=game2")

    app.run(host="127.0.0.1", port=5000)

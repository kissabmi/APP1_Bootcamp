from flask import Flask, request, jsonify
from src.web.mapper.web_mapper import to_domain, to_web
from src.web.model.current_game import CurrentGame as WebGame
from src.web.model.game_field import GameField as WebField


def create_app(service):
    app = Flask(__name__)
    app.service = service

    @app.route("/game/<game_id>", methods=["POST"])
    def make_move(game_id):
        data = request.get_json()
        if data is None or "field" not in data:
            #нет поля в запросе — кидаем ошибку
            return jsonify({"error": "field is required"}), 400

        try:
            web_field = WebField(data["field"])
            web_game = WebGame(web_field, game_id)
            new_game = to_domain(web_game)

            #достаём прежнее состояние игры из хранилища
            previous = app.service.get_game(game_id)
            if previous is None:
                return jsonify({"error": "game not found"}), 404

            #проверяем что игрок не подменил прошлые ходы
            if not app.service.validate_field(new_game, previous):
                return jsonify({"error": "invalid move (previous cells changed)"}), 400

            #комп делает свой ход минимаксом
            app.service.get_next_move(new_game)

            #сохраняем обновлённую игру
            app.service.save_game(new_game)

            #отдаём игроку поле с ходом компа
            return jsonify({
                "game_id": new_game.get_id(),
                "field": new_game.get_field().get_field()
            })
        except Exception as e:
            #что-то пошло не так — возвращаем описание ошибки
            return jsonify({"error": str(e)}), 400

    return app
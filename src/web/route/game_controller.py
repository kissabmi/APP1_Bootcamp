from flask import Flask, jsonify, request

from src.web.mapper.web_mapper import to_domain, to_web
from src.web.model.current_game import CurrentGame as WebGame
from src.web.model.game_field import GameField as WebField

# для игры в браузере
GAME_PAGE = """
<!doctype html>
<html lang='ru'>
<head>
<meta charset='utf-8'>
<title>Крестики-нолики</title>
<style>
  body { font-family: sans-serif; text-align: center; margin-top: 40px; }
  #board { display: grid; grid-template-columns: repeat(3, 100px); gap: 4px;
           justify-content: center; margin: 20px auto; }
  .cell { width: 100px; height: 100px; font-size: 40px; cursor: pointer;
          background: #f0f0f0; display: flex; align-items: center; justify-content: center;
          border: 1px solid #ccc; }
  .cell:hover { background: #e0e0e0; }
  #msg { font-size: 20px; margin: 10px; }
  button { padding: 8px 16px; font-size: 16px; cursor: pointer; }
</style>
</head>
<body>
<h1>Крестики-нолики</h1>
<p>Ты играешь крестиком (X), комп — ноликом (O)</p>
<div id='board'></div>
<p id='msg'></p>
<button onclick='newGame()'>Новая игра</button>
<script>
const GAME_ID = 'abc';
let field = [[0,0,0],[0,0,0],[0,0,0]];

function render() {
  const b = document.getElementById('board');
  b.innerHTML = '';
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      const d = document.createElement('div');
      d.className = 'cell';
      d.textContent = field[r][c] === 1 ? 'X' : field[r][c] === 2 ? 'O' : '';
      d.onclick = () => move(r, c);
      b.appendChild(d);
    }
  }
}

async function move(r, c) {
  if (field[r][c] !== 0) return;
  field[r][c] = 1;
  const resp = await fetch('/game/' + GAME_ID, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({field: field})
  });
  const data = await resp.json();
  if (data.error) {
    document.getElementById('msg').textContent = 'Ошибка: ' + data.error;
    return;
  }
  field = data.field;
  render();
  checkOver();
}

function checkOver() {
  const lines = [[0,0,0,1,0,2],[1,0,1,1,1,2],[2,0,2,1,2,2],
                 [0,0,1,0,2,0],[0,1,1,1,2,1],[0,2,1,2,2,2],
                 [0,0,1,1,2,2],[0,2,1,1,2,0]];
  for (const l of lines) {
    const a = field[l[0]][l[1]], b = field[l[2]][l[3]], cc = field[l[4]][l[5]];
    if (a !== 0 && a === b && b === cc) {
      document.getElementById('msg').textContent = a === 1 ? 'Ты выиграл!' : 'Комп выиграл';
      return;
    }
  }
  let full = field.flat().every(x => x !== 0);
  if (full) document.getElementById('msg').textContent = 'Ничья';
  else document.getElementById('msg').textContent = '';
}

async function newGame() {
  field = [[0,0,0],[0,0,0],[0,0,0]];
  await fetch('/new/' + GAME_ID, {method: 'POST'});
  document.getElementById('msg').textContent = '';
  render();
}

render();
</script>
</body>
</html>
"""


def create_app(service):
    app = Flask(__name__)
    app.service = service

    #главная страница
    @app.route("/", methods=["GET"])
    def index():
        return GAME_PAGE

    #перезапуск игры ("Новая игра")
    @app.route("/new/<game_id>", methods=["POST"])
    def new_game(game_id):
        from src.domain.model.current_game import CurrentGame
        from src.domain.model.game_field import GameField
        app.service.save_game(CurrentGame(GameField(), game_id))
        return jsonify({"ok": True})

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

            #достаём прежнее состояние игры из хран
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
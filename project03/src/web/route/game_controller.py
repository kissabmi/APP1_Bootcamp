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
  body { font-family: sans-serif; text-align: center; margin-top: 20px; }
  .boards { display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; }
  .game { border: 1px solid #ccc; padding: 16px; border-radius: 8px; }
  .game h2 { font-size: 18px; margin: 0 0 8px; }
  .board { display: grid; grid-template-columns: repeat(3, 80px); gap: 3px;
           justify-content: center; margin: 8px auto; }
  .cell { width: 80px; height: 80px; font-size: 34px; cursor: pointer;
          background: #f0f0f0; display: flex; align-items: center; justify-content: center;
          border: 1px solid #bbb; }
  .cell:hover { background: #e0e0e0; }
  .msg { font-size: 16px; margin: 6px; min-height: 22px; }
  button { padding: 6px 14px; font-size: 14px; cursor: pointer; margin: 4px; }
  .add { margin: 16px; }
</style>
</head>
<body>
<h1>Крестики-нолики</h1>
<p>Ты — X, комп — O. Каждая доска — отдельная игра (по своему id)</p>
<div class='add'>
  <input id='newId' value='game3' size='12' placeholder='id новой игры'>
  <button onclick='addGame()'>Добавить игру</button>
</div>
<div class='boards' id='boards'></div>
<script>
const LINES = [[0,0,0,1,0,2],[1,0,1,1,1,2],[2,0,2,1,2,2],
               [0,0,1,0,2,0],[0,1,1,1,2,1],[0,2,1,2,2,2],
               [0,0,1,1,2,2],[0,2,1,1,2,0]];
const games = {};

function emptyField() { return [[0,0,0],[0,0,0],[0,0,0]]; }

async function addGame(id) {
  if (!id) id = document.getElementById('newId').value.trim() || ('game' + (Object.keys(games).length + 1));
  if (games[id]) return;
  await fetch('/new/' + id, {method: 'POST'});
  games[id] = { field: emptyField(), msg: '' };
  renderAll();
}

function renderAll() {
  const root = document.getElementById('boards');
  root.innerHTML = '';
  for (const id in games) {
    const g = games[id];
    const wrap = document.createElement('div');
    wrap.className = 'game';
    wrap.innerHTML = '<h2>Игра: ' + id + '</h2><div class="board" id="b_' + id + '"></div><p class="msg" id="m_' + id + '">' + g.msg + '</p><button onclick="resetGame(\\''+id+'\\')">Заново</button>';
    root.appendChild(wrap);
    const board = document.getElementById('b_' + id);
    for (let r = 0; r < 3; r++) {
      for (let c = 0; c < 3; c++) {
        const d = document.createElement('div');
        d.className = 'cell';
        d.textContent = g.field[r][c] === 1 ? 'X' : g.field[r][c] === 2 ? 'O' : '';
        d.onclick = () => move(id, r, c);
        board.appendChild(d);
      }
    }
  }
}

async function move(id, r, c) {
  const g = games[id];
  if (!g || g.field[r][c] !== 0) return;
  g.field[r][c] = 1;
  const resp = await fetch('/game/' + id, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({field: g.field})
  });
  const data = await resp.json();
  if (data.error) {
    g.msg = 'Ошибка: ' + data.error;
    g.field[r][c] = 0;
  } else {
    g.field = data.field;
    g.msg = checkOver(g.field);
  }
  renderAll();
}

function checkOver(field) {
  for (const l of LINES) {
    const a = field[l[0]][l[1]], b = field[l[2]][l[3]], cc = field[l[4]][l[5]];
    if (a !== 0 && a === b && b === cc) return a === 1 ? 'Ты выиграл!' : 'Комп выиграл';
  }
  if (field.flat().every(x => x !== 0)) return 'Ничья';
  return '';
}

async function resetGame(id) {
  await fetch('/new/' + id, {method: 'POST'});
  games[id] = { field: emptyField(), msg: '' };
  renderAll();
}

addGame('abc');
addGame('game2');
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

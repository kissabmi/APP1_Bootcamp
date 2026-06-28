from src.domain.model.game_field import GameField
from src.domain.model.current_game import CurrentGame
from src.domain.service.game_service_interface import GameServiceInterface


class GameService(GameServiceInterface):

    def get_next_move(self, current_game):
        field = current_game.get_field()
        best_score = -999
        best_move = None

        # перебираем пустые клетки и для каждой запускаем minimax
        # тот ход где оценка максимальная и будет лучшим
        for row in range(GameField.SIZE):
            for col in range(GameField.SIZE):
                if field.is_empty(row, col):
                    field.set_cell(row, col, GameField.PLAYER_O)
                    score = self._minimax(field, 0, False)
                    field.set_cell(row, col, GameField.EMPTY) #откатываем
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move is not None:
            field.set_cell(best_move[0], best_move[1], GameField.PLAYER_O)
        return current_game

    def _minimax(self, field, depth, is_computer_turn):
        #основное — перебираем все ходы до конца игры рекурсивно
        #комп берёт max (хочет выиграть) игрок берёт min (хочет обыграть комп)
        #отсюда и название minimax
        winner = self._check_winner(field)
        if winner == GameField.PLAYER_O:
            #комп выиграл, вычитаем depth чтобы быстрый выигрыш ценился выше
            return 10 - depth
        if winner == GameField.PLAYER_X:
            #проигрыш, отрицательное число (чем дольше тем менее обидно)
            return depth - 10
        if self._is_full(field):
            return 0

        if is_computer_turn:
            best = -999
            for row in range(GameField.SIZE):
                for col in range(GameField.SIZE):
                    if field.is_empty(row, col):
                        field.set_cell(row, col, GameField.PLAYER_O)
                        best = max(best, self._minimax(field, depth + 1, False))
                        field.set_cell(row, col, GameField.EMPTY)
            return best
        else:
            #ход игрока — он будет играть оптимально против нас
            #поэтому берём min (худший для компа вариант)
            best = 999
            for row in range(GameField.SIZE):
                for col in range(GameField.SIZE):
                    if field.is_empty(row, col):
                        field.set_cell(row, col, GameField.PLAYER_X)
                        best = min(best, self._minimax(field, depth + 1, True))
                        field.set_cell(row, col, GameField.EMPTY)
            return best

    def validate_field(self, current_game, previous_game):
        curr = current_game.get_field()
        prev = previous_game.get_field()
        changed = 0
        for row in range(GameField.SIZE):
            for col in range(GameField.SIZE):
                if curr.get_cell(row, col) != prev.get_cell(row, col):
                    #если поменял уже занятую клетку то это подмена прошлого хода
                    if prev.get_cell(row, col) != GameField.EMPTY:
                        return False
                    changed += 1
        #за один ход ставится только один крестик
        if changed != 1:
            return False
        return True

    def check_game_over(self, current_game):
        winner = self._check_winner(current_game.get_field())
        if winner != GameField.EMPTY:
            return winner
        if self._is_full(current_game.get_field()):
            return -1
        return 0

    def _check_winner(self, field):
        lines = []
        for i in range(GameField.SIZE):
            lines.append([field.get_cell(i, j) for j in range(GameField.SIZE)])      #строки
            lines.append([field.get_cell(j, i) for j in range(GameField.SIZE)])      #столбцы
        lines.append([field.get_cell(i, i) for i in range(GameField.SIZE)])          #диагональ \
        lines.append([field.get_cell(i, GameField.SIZE - 1 - i) for i in range(GameField.SIZE)])  #диагональ /

        #линия из трёх одинаковых (не пустых) = победа
        for line in lines:
            if line[0] != GameField.EMPTY and all(c == line[0] for c in line):
                return line[0]
        return GameField.EMPTY

    def _is_full(self, field):
        for row in range(GameField.SIZE):
            for col in range(GameField.SIZE):
                if field.is_empty(row, col):
                    return False
        return True
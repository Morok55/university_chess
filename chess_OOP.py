import copy


class ChessPiece:
    """Базовый класс для шахматных фигур.

    Attributes:
        color (str): Цвет фигуры ('white' или 'black').
    """

    def __init__(self, color):
        """Инициализация фигуры.

        Args:
            color (str): Цвет фигуры.
        """
        self.color = color

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для фигуры.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция фигуры (x, y).

        Raises:
            NotImplementedError: Метод должен быть переопределён в наследниках.
        """
        raise NotImplementedError

    def is_valid_move(self, board, start, end):
        """Проверяет, является ли ход допустимым.

        Args:
            board (ChessBoard): Игровая доска.
            start (tuple): Начальная позиция (x, y).
            end (tuple): Конечная позиция (x, y).

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        return end in self.valid_moves(board, start)


class King(ChessPiece):
    """Класс, представляющий короля."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для короля.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция короля.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            x, y = position[0] + dx, position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece((x, y))
                if not piece or piece.color != self.color:
                    moves.append((x, y))
        return moves


class Queen(ChessPiece):
    """Класс, представляющий ферзя."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для ферзя.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция ферзя.

        Returns:
            list: Список возможных ходов.
        """
        return Rook(self.color).valid_moves(board, position) + Bishop(self.color).valid_moves(board, position)


class Rook(ChessPiece):
    """Класс, представляющий ладью."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для ладьи.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция ладьи.

        Returns:
            list: Список возможных ходов.
        """
        return board.get_linear_moves(position, self.color, [(1, 0), (-1, 0), (0, 1), (0, -1)])


class Bishop(ChessPiece):
    """Класс, представляющий слона."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для слона.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция слона.

        Returns:
            list: Список возможных ходов.
        """
        return board.get_linear_moves(position, self.color, [(1, 1), (-1, -1), (1, -1), (-1, 1)])


class Knight(ChessPiece):
    """Класс, представляющий коня."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для коня.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция коня.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in knight_moves:
            x, y = position[0] + dx, position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece((x, y))
                if not piece or piece.color != self.color:
                    moves.append((x, y))
        return moves


class Pawn(ChessPiece):
    """Класс, представляющий пешку."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для пешки.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция пешки.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Ход вперед
        forward = (position[0] + direction, position[1])
        if board.get_piece(forward) is None:
            moves.append(forward)
            if position[0] == start_row:
                double_forward = (position[0] + 2 * direction, position[1])
                if board.get_piece(double_forward) is None:
                    moves.append(double_forward)

        # Взятие по диагонали
        for dy in [-1, 1]:
            capture = (position[0] + direction, position[1] + dy)
            if 0 <= capture[1] < 8:
                piece = board.get_piece(capture)
                if piece and piece.color != self.color:
                    moves.append(capture)

        return moves


class Archer(ChessPiece):
    """Фигура лучника: движется на 2 клетки в любом направлении и атакует по диагонали на любое расстояние."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для лучника.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция лучника.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dx, dy in directions:
            x, y = position[0] + dx, position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece((x, y))
                if not piece or piece.color != self.color:
                    moves.append((x, y))

        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in diagonal_directions:
            x, y = position
            while True:
                x, y = x + dx, y + dy
                if 0 <= x < 8 and 0 <= y < 8:
                    piece = board.get_piece((x, y))
                    if piece:
                        if piece.color != self.color:
                            moves.append((x, y))
                        break
                else:
                    break
        return moves


class Striker(ChessPiece):
    """Фигура нападающего: двигается как ферзь, но максимум на 2 клетки в любом направлении."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для нападающего.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция нападающего (x, y).

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        for dx, dy in directions:
            x, y = position
            for _ in range(2):
                x += dx
                y += dy
                if 0 <= x < 8 and 0 <= y < 8:
                    piece = board.get_piece((x, y))
                    if piece:
                        if piece.color != self.color:
                            moves.append((x, y))
                        break
                    moves.append((x, y))
                else:
                    break
        return moves


class Oracle(ChessPiece):
    """Фигура оракула: ходит на 2 клетки в любом направлении и может перепрыгивать фигуры."""

    def valid_moves(self, board, position):
        """Возвращает список возможных ходов для оракула.

        Args:
            board (ChessBoard): Игровая доска.
            position (tuple): Текущая позиция оракула (x, y).

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        directions = [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]
        for dx, dy in directions:
            x, y = position[0] + dx, position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece((x, y))
                if not piece or piece.color != self.color:
                    moves.append((x, y))
        return moves


class MoveHistory:
    """Класс для хранения истории ходов на шахматной доске."""

    def __init__(self):
        """Инициализирует историю ходов."""
        self.history = []

    def save_state(self, board):
        """Сохраняет текущее состояние доски в историю.

        Args:
            board (ChessBoard): Игровая доска.
        """
        self.history.append(copy.deepcopy(board))

    def undo(self, steps=1):
        """Откатывает состояние доски на указанное количество ходов назад.

        Args:
            steps (int, optional): Количество шагов для отката. По умолчанию 1.

        Returns:
            ChessBoard | None: Возвращает предыдущее состояние доски или None, если откат невозможен.

        Raises:
            ValueError: Если попытка отката превышает количество сохранённых ходов.
        """
        if len(self.history) <= 1:
            print("Откат невозможен: не было сделано ни одного хода.")
            return None

        if steps >= len(self.history):
            print(f"Нельзя откатить больше ходов ({steps}), чем было сделано ({len(self.history) - 1}).")
            return None

        for _ in range(steps):
            if len(self.history) > 1:
                self.history.pop()

        print(f"Откат выполнен. Осталось {len(self.history) - 1} ходов в истории.")
        return copy.deepcopy(self.history[-1])  # Возвращаем предыдущее состояние


class MoveHint:
    """Класс для хранения и отображения доступных ходов фигур на шахматной доске."""

    def __init__(self):
        """Инициализирует пустые подсказки ходов."""
        self.hints = {}

    def set_hints(self, piece, valid_moves):
        """Сохраняет подсказки для возможных ходов фигуры.

        Args:
            piece (ChessPiece): Фигура, для которой сохраняются подсказки.
            valid_moves (list): Список доступных ходов (кортежи с координатами).
        """
        self.hints = {move: 'x' if piece else '.' for move in valid_moves}

    def clear_hints(self):
        """Очищает все сохранённые подсказки."""
        self.hints = {}

    def get_hint(self, position):
        """Возвращает символ подсказки для заданной позиции.

        Args:
            position (tuple): Координаты (x, y), для которых требуется подсказка.

        Returns:
            str | None: Символ подсказки ('x' или '.'), либо None, если подсказки нет.
        """
        return self.hints.get(position, None)


class ThreatDetector:
    """Класс для определения фигур, находящихся под угрозой атаки противника."""

    def __init__(self):
        """Инициализирует объект для отслеживания угроз."""
        self.threatened_positions = set()
        self.is_check = False

    def detect_threats(self, board, current_turn):
        """Определяет фигуры под угрозой и фиксирует шах королю, если он есть.

        Args:
            board (ChessBoard): Игровая доска.
            current_turn (str): Цвет текущего игрока ('white' или 'black').
        """
        self.threatened_positions.clear()
        self.is_check = False
        king_position = None

        # Определяем местоположение короля текущего игрока
        for x in range(8):
            for y in range(8):
                piece = board.get_piece((x, y))
                if isinstance(piece, King) and piece.color == current_turn:
                    king_position = (x, y)

        # Проверяем атаки со стороны фигур противника
        for x in range(8):
            for y in range(8):
                piece = board.get_piece((x, y))
                if piece and piece.color != current_turn:
                    for move in piece.valid_moves(board, (x, y)):
                        target_piece = board.get_piece(move)
                        if target_piece and target_piece.color == current_turn:
                            self.threatened_positions.add(move)
                        if move == king_position:
                            self.is_check = True

    def get_threat_symbol(self, position):
        """Возвращает символ угрозы для заданной позиции.

        Args:
            position (tuple): Координаты (x, y) на доске.

        Returns:
            str | None: Символ '!', если позиция находится под угрозой, иначе None.
        """
        return '!' if position in self.threatened_positions else None


class ChessBoard:
    """Класс, представляющий шахматную доску."""

    def __init__(self, mode):
        """Инициализирует шахматную доску и расставляет фигуры.

        Args:
            mode (str): Режим игры ('classic' — стандартные шахматы, 'modified' — с дополнительными фигурами).
        """
        self.board = [[None] * 8 for _ in range(8)]  # Инициализация пустой доски 8x8
        self.mode = mode  # Установка режима игры
        self.setup_board()  # Расстановка фигур на доске
        self.move_hint = MoveHint()  # Экземпляр для подсказок ходов
        self.threat_detector = ThreatDetector()  # Экземпляр для определения угроз на доске

    def setup_board(self):
        """Расставляет фигуры на доске в зависимости от режима игры."""
        for i in range(8):
            self.board[1][i] = Pawn('black')
            self.board[6][i] = Pawn('white')

        back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece in enumerate(back_row):
            self.board[0][i] = piece('black')
            self.board[7][i] = piece('white')

        if self.mode == 'modified':
            self.add_custom_pieces()

    def add_custom_pieces(self):
        """Добавляет новые фигуры в модифицированную версию шахмат."""
        self.board[0][0] = Archer('black')
        self.board[7][0] = Archer('white')
        self.board[0][5] = Striker('black')
        self.board[7][5] = Striker('white')
        self.board[0][3] = Oracle('black')
        self.board[7][3] = Oracle('white')

    def setup_checkers(self):
        """Настраивает доску для игры в шашки."""
        for i in range(8):
            for j in range(i % 2, 8, 2):
                if i < 3:
                    self.board[i][j] = CheckerPiece('black')
                elif i > 4:
                    self.board[i][j] = CheckerPiece('white')

    def get_piece(self, position):
        """Возвращает фигуру, находящуюся в заданной позиции.

        Args:
            position (tuple): Координаты (x, y) на доске.

        Returns:
            ChessPiece | None: Фигура, находящаяся в указанной позиции, либо None.
        """
        x, y = position
        return self.board[x][y]

    def move_piece(self, start, end):
        """Перемещает фигуру из одной позиции в другую.

        Args:
            start (tuple): Начальная позиция (x, y).
            end (tuple): Конечная позиция (x, y).

        Returns:
            bool: True, если ход выполнен успешно, иначе False.
        """
        piece = self.get_piece(start)
        if piece and piece.is_valid_move(self, start, end):
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            return True
        return False

    def highlight_moves(self, position):
        """Подсвечивает доступные ходы для выбранной фигуры.

        Args:
            position (tuple): Координаты (x, y) фигуры.
        """
        piece = self.get_piece(position)
        if piece:
            valid_moves = piece.valid_moves(self, position)
            self.move_hint.set_hints(piece, valid_moves)

    def clear_highlight(self):
        """Очищает подсказки ходов."""
        self.move_hint.clear_hints()

    def get_linear_moves(self, position, color, directions):
        """Возвращает список возможных ходов по прямым линиям в заданных направлениях.

        Args:
            position (tuple): Координаты (x, y) фигуры.
            color (str): Цвет фигуры ('white' или 'black').
            directions (list): Список направлений в формате [(dx, dy), ...].

        Returns:
            list: Список доступных координат для хода.
        """
        moves = []
        for dx, dy in directions:
            x, y = position
            while True:
                x, y = x + dx, y + dy
                if 0 <= x < 8 and 0 <= y < 8:
                    piece = self.get_piece((x, y))
                    if piece:
                        if piece.color != color:
                            moves.append((x, y))
                        break
                    moves.append((x, y))
                else:
                    break
        return moves

    def detect_threats(self, current_turn):
        """Определяет фигуры под угрозой и обновляет информацию о шахе.

        Args:
            current_turn (str): Цвет текущего игрока ('white' или 'black').
        """
        self.threat_detector.detect_threats(self, current_turn)

    def print_board(self):
        """Выводит текущее состояние доски в консоль."""
        symbols = {
            King: 'K', Queen: 'Q', Rook: 'R', Bishop: 'B', Knight: 'N',
            Pawn: 'P', Archer: 'A', Striker: 'S', Oracle: 'O', CheckerPiece: 'C'
        }
        print('  A B C D E F G H')
        for i, row in enumerate(self.board):
            print(8 - i, end=' ')
            for j, piece in enumerate(row):
                hint = self.move_hint.get_hint((i, j))
                threat = self.threat_detector.get_threat_symbol((i, j))
                if hint:
                    print(hint, end=' ')  # Подсветка хода
                elif threat:
                    print(threat, end=' ')  # Подсветка угрозы
                elif piece is None:
                    print('.', end=' ')
                else:
                    symbol = symbols[type(piece)] if piece.color == 'white' else symbols[type(piece)].lower()
                    if isinstance(piece, CheckerPiece):  # Если это шашка
                        symbol = 'C' if piece.color == 'white' else 'c'
                    print(symbol, end=' ')
            print(8 - i)
        print('  A B C D E F G H')


class ChessGame:
    """Класс, представляющий шахматную партию."""

    def __init__(self, mode):
        """Инициализирует игру, создавая доску и устанавливая начальные параметры.

        Args:
            mode (str): Режим игры ('classic' — стандартные шахматы, 'modified' — с дополнительными фигурами).
        """
        self.board = ChessBoard(mode)  # Создание шахматной доски
        self.turn = 'white'  # Белая сторона начинает
        self.move_count = 0  # Количество ходов
        self.mode = mode  # Установленный режим игры
        self.history = MoveHistory()  # История ходов
        self.history.save_state(self.board)  # Сохраняем начальное состояние доски

    def switch_turn(self):
        """Переключает очередь хода на противоположный цвет и увеличивает счётчик ходов."""
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.move_count += 1

    def is_valid_input(self, move):
        """Проверяет корректность ввода координат.

        Args:
            move (str): Строка, представляющая координаты, например, 'e2'.

        Returns:
            bool: True, если ввод корректен, иначе False.
        """
        if len(move) != 2:
            return False
        col, row = move
        return col in 'abcdefgh' and row.isdigit() and 1 <= int(row) <= 8

    def undo_moves(self, n=1):
        """Откатывает `n` ходов назад.

        Args:
            n (int, optional): Количество ходов для отката. По умолчанию 1.
        """
        new_board = self.history.undo(n)
        if new_board:
            self.board = new_board
            self.switch_turn()

    def input_position(self, prompt):
        """Запрашивает у игрока ввод позиции фигуры или команды.

        Args:
            prompt (str): Сообщение для пользователя.

        Returns:
            tuple | None: Координаты (x, y), если ввод корректен, или None при выходе.
        """
        while True:
            move = input(prompt).strip().lower()
            if move == 'exit':
                return None
            if move.startswith('undo '):
                try:
                    steps = int(move.split()[1])
                    self.undo_moves(steps)
                    self.board.print_board()
                except ValueError:
                    print('Некорректный формат команды отката.')
                continue
            if self.is_valid_input(move):
                return 8 - int(move[1]), ord(move[0]) - ord('a')
            print('Некорректный ввод. Используйте формат e2.')

    def play(self):
        """Запускает игровой цикл, в котором игроки поочерёдно делают ходы."""
        while True:
            self.board.detect_threats(self.turn)  # Обновление угроз перед ходом
            self.board.print_board()

            if self.board.threat_detector.is_check:
                print(f'Шах! Королю {self.turn} угрожает опасность!')

            print(f'Ход {self.turn}. Всего ходов: {self.move_count}')

            # Выбор фигуры
            start = self.input_position('Выберите фигуру (например, e2): ')
            if start is None:
                break

            piece = self.board.get_piece(start)
            if not piece:
                print('На выбранной клетке нет фигуры.')
                continue

            if piece.color != self.turn:
                print('Сейчас ходит другая сторона.')
                continue

            # Подсветка доступных ходов
            self.board.highlight_moves(start)
            self.board.print_board()

            # Выбор конечной клетки
            end = self.input_position('Выберите клетку для хода (например, e4): ')
            if end is None:
                self.board.clear_highlight()
                break

            if self.board.move_piece(start, end):
                self.history.save_state(self.board)
                self.switch_turn()
            else:
                print('Неверный ход, попробуйте снова.')

            self.board.clear_highlight()


# Шашки
class CheckerPiece(ChessPiece):
    """Класс, представляющий шашку."""

    def __init__(self, color):
        """Создаёт шашку заданного цвета.

        Args:
            color (str): Цвет шашки ('white' или 'black').
        """
        super().__init__(color)

    def valid_moves(self, board, position):
        """Определяет все допустимые ходы для шашки.

        Args:
            board (CheckerBoard): Доска с расположением фигур.
            position (tuple): Текущая позиция шашки (x, y).

        Returns:
            list: Список возможных ходов [(x1, y1), (x2, y2), ...].
        """
        moves = []
        directions = [(-1, -1), (-1, 1)] if self.color == 'white' else [(1, -1), (1, 1)]

        # Ходы на одну клетку
        for dx, dy in directions:
            x, y = position[0] + dx, position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece((x, y))
                if not piece:
                    moves.append((x, y))

        # Ходы с взятием
        for dx, dy in directions:
            x, y = position[0] + 2 * dx, position[1] + 2 * dy
            middle_x, middle_y = position[0] + dx, position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece((x, y))
                middle_piece = board.get_piece((middle_x, middle_y))
                if not piece and middle_piece and middle_piece.color != self.color:
                    moves.append((x, y))

        return moves


class CheckerBoard(ChessBoard):
    """Класс, представляющий доску для игры в шашки."""

    def setup_board(self):
        """Заполняет доску шашками для начала игры."""
        for i in range(8):
            for j in range(i % 2, 8, 2):
                if i < 3:
                    self.board[i][j] = CheckerPiece('black')
                elif i > 4:
                    self.board[i][j] = CheckerPiece('white')

    def get_piece(self, position):
        """Возвращает шашку на указанной позиции.

        Args:
            position (tuple): Координаты на доске (x, y).

        Returns:
            CheckerPiece | None: Фигура на указанной позиции или None.
        """
        x, y = position
        return self.board[x][y]

    def move_piece(self, start, end):
        """Перемещает шашку, выполняя ход или взятие.

        Args:
            start (tuple): Начальная позиция (x, y).
            end (tuple): Конечная позиция (x, y).

        Returns:
            bool: True, если ход выполнен успешно, иначе False.
        """
        piece = self.get_piece(start)
        if piece and piece.is_valid_move(self, start, end):
            # Если шашка делает ход с взятием, удаляем побитую шашку
            middle_x = (start[0] + end[0]) // 2
            middle_y = (start[1] + end[1]) // 2
            middle_piece = self.get_piece((middle_x, middle_y))
            if middle_piece:  # Если на пути есть шашка противника
                self.board[middle_x][middle_y] = None  # Удаляем съеденную шашку

            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            return True
        return False


class CheckerGame(ChessGame):
    """Класс, представляющий игру в шашки."""

    def __init__(self, mode):
        """Инициализирует игру в шашки

        Args:
            mode (str): Режим игры.
        """
        super().__init__(mode)
        self.board = CheckerBoard(mode)


if __name__ == '__main__':
    print('Выберите режим игры:')
    print('1 - Классические шахматы')
    print('2 - Модифицированные шахматы (с новыми фигурами)')
    print('3 - Шашки')

    while True:
        choice = input('Введите 1, 2 или 3: ').strip()
        if choice in ('1', '2', '3'):
            mode = 'classic' if choice == '1' else 'modified' if choice == '2' else 'checkers'
            break
        print('Некорректный ввод. Введите 1, 2 или 3.')

    if mode == 'checkers':
        game = CheckerGame(mode)
    else:
        game = ChessGame(mode)

    game.play()

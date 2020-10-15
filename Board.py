class Board:
    BLANK = '?'
    X = 'X'
    O = 'O'
    VALID_INPUTS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    SUCCESS_MESSAGE = 'Success'
    TIE = 'Tie.'

    def __init__(self):
        self.reset_board()

    def get_board_data(self):
        return '\n'.join((','.join(self.board[0:3]), ','.join(self.board[3:6]), ','.join(self.board[6:9])))

    def get_guide(self):
        return "\n".join((
            "Welcome to Discord TicTacToe!",
            'Type ".move (a number from 1 to 9)" to make your move in the board.',
            "Example: .move 5",
            '1,2,3',
            '4,5,6',
            '7,8,9',
            "Let's play."
        ))

    def reset_board(self):
        self.board = [self.BLANK] * 9
        self.current_player = self.X

    def get_board_2D(self):
        return [self.board[0:3], self.board[3:6], self.board[6:9]]

    def switch_player(self):
        self.current_player = self.O if self.current_player == self.X else self.X

    def get_move_status(self, move):
        if move not in self.VALID_INPUTS: return "Invalid input"
        move = int(move)
        if self.board[move - 1] != self.BLANK: return f"Space {move} is already placed."
        return self.SUCCESS_MESSAGE

    def place(self, index):
        self.board[index - 1] = self.current_player

    def get_next_turn_message(self):
        return f'Next turn: {self.current_player}'

    def get_win_message(self):
        winner = self.get_winner()
        if winner == None and not self.is_full(): return ""
        if winner == None: return self.TIE
        return f'{winner} is the winner!'

    def get_winner(self):
        board = self.get_board_2D()
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != self.BLANK: return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != self.BLANK: return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != self.BLANK: return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != self.BLANK: return board[0][2]
        return None

    def is_full(self):
        return not any(move == self.BLANK for move in self.board)

class TicTacToe:
    """Tic-Tac-Toe game engine used by the AI agents."""

    def __init__(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]

    def display(self):
        for r, row in enumerate(self.board):
            print(" | ".join(cell if cell else " " for cell in row))
            if r < 2:
                print("-" * 9)

    def get_valid_moves(self):
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.board[r][c] == ""
        ]

    def make_move(self, row, col, player):
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.board[row][col] != "":
            return False
        self.board[row][col] = player
        return True

    def undo_move(self, row, col):
        self.board[row][col] = ""

    def check_winner(self):
        lines = [
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
        ]
        for line in lines:
            values = [self.board[r][c] for r, c in line]
            if values[0] and values[0] == values[1] == values[2]:
                return values[0]
        return None

    def is_draw(self):
        return self.check_winner() is None and not self.get_valid_moves()

    def is_terminal(self):
        return self.check_winner() is not None or self.is_draw()

    def clone(self):
        game = TicTacToe()
        game.board = [row[:] for row in self.board]
        return game

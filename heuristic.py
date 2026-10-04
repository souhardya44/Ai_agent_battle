WIN_SCORE = 100
THREAT_SCORE = 10
CENTER_SCORE = 3
CORNER_SCORE = 2


def _lines(game):
    b = game.board
    return [
        [b[0][0], b[0][1], b[0][2]],
        [b[1][0], b[1][1], b[1][2]],
        [b[2][0], b[2][1], b[2][2]],
        [b[0][0], b[1][0], b[2][0]],
        [b[0][1], b[1][1], b[2][1]],
        [b[0][2], b[1][2], b[2][2]],
        [b[0][0], b[1][1], b[2][2]],
        [b[0][2], b[1][1], b[2][0]],
    ]


def _line_counts(line, player):
    opponent = "O" if player == "X" else "X"
    mine = line.count(player)
    theirs = line.count(opponent)
    empty = line.count("")
    return mine, theirs, empty


def heuristic_h1(game, player):
    """Tactical heuristic: strongly values immediate threats."""
    opponent = "O" if player == "X" else "X"
    winner = game.check_winner()
    if winner == player:
        return WIN_SCORE
    if winner == opponent:
        return -WIN_SCORE

    score = 0
    for line in _lines(game):
        mine, theirs, empty = _line_counts(line, player)
        if mine == 2 and empty == 1:
            score += THREAT_SCORE
        if theirs == 2 and empty == 1:
            score -= THREAT_SCORE

    if game.board[1][1] == player:
        score += CENTER_SCORE
    elif game.board[1][1] == opponent:
        score -= CENTER_SCORE

    for r, c in [(0,0), (0,2), (2,0), (2,2)]:
        if game.board[r][c] == player:
            score += CORNER_SCORE
        elif game.board[r][c] == opponent:
            score -= CORNER_SCORE

    return score


def heuristic_h2(game, player):
    """Positional heuristic: rewards flexible two-in-a-row potential,
    center/corner control, and penalizes opponent potential."""
    opponent = "O" if player == "X" else "X"
    winner = game.check_winner()
    if winner == player:
        return WIN_SCORE
    if winner == opponent:
        return -WIN_SCORE

    score = 0
    for line in _lines(game):
        mine, theirs, empty = _line_counts(line, player)
        if theirs == 0:
            if mine == 2 and empty == 1:
                score += 8
            elif mine == 1 and empty == 2:
                score += 3
        if mine == 0:
            if theirs == 2 and empty == 1:
                score -= 8
            elif theirs == 1 and empty == 2:
                score -= 3

    if game.board[1][1] == player:
        score += 5
    elif game.board[1][1] == opponent:
        score -= 5

    for r, c in [(0,0), (0,2), (2,0), (2,2)]:
        if game.board[r][c] == player:
            score += 3
        elif game.board[r][c] == opponent:
            score -= 3

    return score

from dataclasses import dataclass
import math
import random


@dataclass
class SearchStats:
    nodes_evaluated: int = 0
    nodes_pruned: int = 0


def _search(game, depth, maximizing, root_player, heuristic, alpha, beta, stats):
    winner = game.check_winner()
    if winner is not None:
        stats.nodes_evaluated += 1
        return 100 if winner == root_player else -100

    if game.is_draw():
        stats.nodes_evaluated += 1
        return 0

    if depth == 0:
        stats.nodes_evaluated += 1
        return heuristic(game, root_player)

    opponent = "O" if root_player == "X" else "X"

    if maximizing:
        value = -math.inf
        for i, move in enumerate(game.get_valid_moves()):
            game.make_move(*move, root_player)
            value = max(value, _search(game, depth - 1, False, root_player,
                                       heuristic, alpha, beta, stats))
            game.undo_move(*move)
            alpha = max(alpha, value)
            if alpha >= beta:
                remaining = len(game.get_valid_moves()) - i - 1
                stats.nodes_pruned += max(0, remaining)
                break
        return value

    value = math.inf
    for i, move in enumerate(game.get_valid_moves()):
        game.make_move(*move, opponent)
        value = min(value, _search(game, depth - 1, True, root_player,
                                   heuristic, alpha, beta, stats))
        game.undo_move(*move)
        beta = min(beta, value)
        if alpha >= beta:
            remaining = len(game.get_valid_moves()) - i - 1
            stats.nodes_pruned += max(0, remaining)
            break
    return value


def choose_move(game, player, depth, heuristic, rng=None):
    rng = rng or random.Random()
    stats = SearchStats()
    moves = game.get_valid_moves()
    if not moves:
        return None, stats

    opponent = "O" if player == "X" else "X"
    scored = []

    for move in moves:
        game.make_move(*move, player)
        if game.check_winner() == player:
            value = 100
            stats.nodes_evaluated += 1
        elif game.is_draw():
            value = 0
            stats.nodes_evaluated += 1
        else:
            value = _search(
                game, max(0, depth - 1), False, player,
                heuristic, -math.inf, math.inf, stats
            )
        game.undo_move(*move)
        scored.append((value, move))

    best_value = max(v for v, _ in scored)
    best_moves = [m for v, m in scored if v == best_value]
    return rng.choice(best_moves), stats

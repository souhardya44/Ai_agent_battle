import csv
import statistics
import time
from pathlib import Path

from agents import Nexus, Titan
from game import TicTacToe
from heuristic import heuristic_h1


def run_game(first_agent_name, nexus_depth=3, titan_depth=3, seed=0):
    if first_agent_name == "NEXUS":
        nexus = Nexus("X", nexus_depth, 1000 + seed)
        titan = Titan("O", titan_depth, 2000 + seed)
    else:
        titan = Titan("X", titan_depth, 2000 + seed)
        nexus = Nexus("O", nexus_depth, 1000 + seed)

    agents = {"NEXUS": nexus, "TITAN": titan}
    game = TicTacToe()
    current = first_agent_name
    total_time = 0.0
    stats_by_agent = {
        "NEXUS": {"nodes": 0, "pruned": 0, "time": 0.0},
        "TITAN": {"nodes": 0, "pruned": 0, "time": 0.0},
    }
    moves = 0

    while not game.is_terminal():
        agent = agents[current]
        move, stats, elapsed = agent.choose_move(game)
        if move is None:
            break
        game.make_move(*move, agent.player)
        moves += 1
        stats_by_agent[current]["nodes"] += stats.nodes_evaluated
        stats_by_agent[current]["pruned"] += stats.nodes_pruned
        stats_by_agent[current]["time"] += elapsed
        total_time += elapsed
        current = "TITAN" if current == "NEXUS" else "NEXUS"

    winner_symbol = game.check_winner()
    if winner_symbol is None:
        winner = "DRAW"
    elif winner_symbol == nexus.player:
        winner = "NEXUS"
    else:
        winner = "TITAN"

    return {
        "first": first_agent_name,
        "winner": winner,
        "moves": moves,
        "nexus_nodes": stats_by_agent["NEXUS"]["nodes"],
        "titan_nodes": stats_by_agent["TITAN"]["nodes"],
        "nexus_pruned": stats_by_agent["NEXUS"]["pruned"],
        "titan_pruned": stats_by_agent["TITAN"]["pruned"],
        "execution_time_ms": total_time * 1000.0,
    }


def run_depth_experiment(depths=(1, 2, 3, 4), games_per_depth=10):
    rows = []
    for depth in depths:
        outcomes = []
        for i in range(games_per_depth):
            first = "NEXUS" if i % 2 == 0 else "TITAN"
            outcomes.append(run_game(first, depth, depth, seed=5000 + depth * 100 + i))
        rows.append({
            "depth": depth,
            "games": games_per_depth,
            "nexus_wins": sum(r["winner"] == "NEXUS" for r in outcomes),
            "titan_wins": sum(r["winner"] == "TITAN" for r in outcomes),
            "draws": sum(r["winner"] == "DRAW" for r in outcomes),
            "avg_nodes": statistics.mean(r["nexus_nodes"] + r["titan_nodes"] for r in outcomes),
            "avg_pruned": statistics.mean(r["nexus_pruned"] + r["titan_pruned"] for r in outcomes),
            "avg_time_ms": statistics.mean(r["execution_time_ms"] for r in outcomes),
        })
    return rows


def run_battle(games=10):
    return [
        {"game": i + 1, **run_game(
            "NEXUS" if i % 2 == 0 else "TITAN",
            nexus_depth=3,
            titan_depth=3,
            seed=9000 + i
        )}
        for i in range(games)
    ]


def save_battle(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "game", "first", "winner", "moves",
        "nexus_nodes", "titan_nodes",
        "nexus_pruned", "titan_pruned",
        "execution_time_ms"
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_depth(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "depth", "games", "nexus_wins", "titan_wins",
        "draws", "avg_nodes", "avg_pruned", "avg_time_ms"
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    battle = run_battle(10)
    depth = run_depth_experiment()
    save_battle(battle, "results/results.csv")
    save_depth(depth, "results/depth_experiment.csv")
    print("10-game battle:")
    for row in battle:
        print(row)
    print("\nDepth experiment:")
    for row in depth:
        print(row)

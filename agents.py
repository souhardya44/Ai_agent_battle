import random
import time
from minimax import choose_move


class Agent:
    def __init__(self, name, player, depth, heuristic, rng_seed=None):
        self.name = name
        self.player = player
        self.depth = depth
        self.heuristic = heuristic
        self.rng = random.Random(rng_seed)

    def choose_move(self, game):
        start = time.perf_counter()
        move, stats = choose_move(
            game, self.player, self.depth, self.heuristic, self.rng
        )
        elapsed = time.perf_counter() - start
        return move, stats, elapsed


class Nexus(Agent):
    def __init__(self, player="X", depth=3, rng_seed=100):
        from heuristic import heuristic_h1
        super().__init__("NEXUS", player, depth, heuristic_h1, rng_seed)


class Titan(Agent):
    def __init__(self, player="O", depth=3, rng_seed=200):
        from heuristic import heuristic_h2
        super().__init__("TITAN", player, depth, heuristic_h2, rng_seed)

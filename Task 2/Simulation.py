from Wolf import Wolf
from plot import graph_simulation
from ui import print_round_result, print_simulation_end
from file import *
import random


class Simulation(object):
    def __init__(self,
                 max_round: int,
                 current_round: int,
                 sheep_amount: int,
                 meadow_range: float,
                 sheep_step_size: float,
                 wolf_attack_range: float) -> None:
        self.max_round = max_round
        self.current_round = current_round
        self.sheep_amount = sheep_amount
        self.meadow_range = meadow_range
        self.sheep_step_size = sheep_step_size
        self.wolf_attack_range = wolf_attack_range

    def play_simulation(self) -> None:
        rounds_list = []
        alive_list = []
        last_round = 1
        sheep_count = self.sheep_amount
        sheep_list, wolf = self.create_creatures()
        for r in range(1, self.max_round + 1):
            last_round = r
            wolf_action, sheep_count = self.play_round(sheep_list, wolf)
            if wolf_action is not None:
                print_round_result(r, wolf.x_pos, wolf.y_pos,
                                   sheep_count, wolf_action)
            else:
                break
            rounds_list = get_round_info(r, wolf.x_pos, wolf.y_pos,
                                         sheep_list, rounds_list)
            save_round_to_json(rounds_list)
            alive_list.append((r, sheep_count))
            save_round_to_csv(alive_list)
        print_simulation_end(last_round, self.max_round, sheep_count)

    def create_creatures(self) -> tuple[list[Sheep], Wolf]:
        sheep_list = []
        for i in range(1, self.sheep_amount + 1):
            x = random.uniform(-self.meadow_range, self.meadow_range)
            y = random.uniform(-self.meadow_range, self.meadow_range)
            sheep = Sheep(x_pos=x, y_pos=y, sheep_id=i,
                          step_size=self.sheep_step_size)
            sheep_list.append(sheep)
        wolf = Wolf(x_pos=0.0, y_pos=0.0,
                    wolf_range=self.wolf_attack_range)
        return sheep_list, wolf

    def play_round(self, sheep_list: list[Sheep], wolf: Wolf) -> tuple[
        dict[str, int], int]:
        sheep_count = 0
        for sheep in sheep_list:
            if sheep.is_alive:
                sheep.play_sheep_turn(self.meadow_range)
                sheep_count += 1
        if sheep_count > 0:
            wolf_action = wolf.play_wolf_turn(sheep_list)
            if wolf_action["action"] == "eat":
                sheep_count -= 1
            return wolf_action, sheep_count
        return None, 0

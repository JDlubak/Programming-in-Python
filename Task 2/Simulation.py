from Sheep import Sheep
from Wolf import Wolf
from plot import graph_simulation
from ui import print_round_result
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
        self.sheep_list = []
        self.wolf = None

    def play_simulation(self):
        rounds_list = []
        alive_list = []
        self.create_creatures()
        for r in range(1, self.max_round + 1):
            sheep_counter = 0
            for sheep in self.sheep_list:
                if sheep.is_alive:
                    sheep.play_sheep_turn(self.meadow_range)
                    sheep_counter += 1
            if sheep_counter > 0:
                wolf_action = self.wolf.play_wolf_turn(self.sheep_list)
            else:
                break
            sheep_counter = sheep_counter \
                if wolf_action["action"] == "move" \
                else sheep_counter - 1
            print_round_result(r, self.wolf.x_pos, self.wolf.y_pos,
                               sheep_counter, wolf_action)
            rounds_list = get_round_info(r, self.wolf.x_pos,
                                               self.wolf.y_pos,
                                               self.sheep_list,
                                               rounds_list)
            alive_list.append((r, sheep_counter))
            save_round_to_json(rounds_list)
        save_round_to_csv(alive_list)

    def create_creatures(self):
        for i in range(1, self.sheep_amount + 1):
            x = random.uniform(-self.meadow_range, self.meadow_range)
            y = random.uniform(-self.meadow_range, self.meadow_range)
            sheep = Sheep(x_pos=x, y_pos=y, sheep_id=i,
                          step_size=self.sheep_step_size)
            self.sheep_list.append(sheep)
        self.wolf = Wolf(x_pos=0.0, y_pos=0.0,
                         wolf_range=self.wolf_attack_range)

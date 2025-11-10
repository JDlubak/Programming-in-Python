import random
from Creature import Creature


class Sheep(Creature):
    def __init__(self,
                 x_pos: float,
                 y_pos: float,
                 sheep_id: int,
                 step_size: float,
                 is_alive: bool = True) -> None:
        super().__init__(x_pos, y_pos)
        self.sheep_id = sheep_id
        self.is_alive = is_alive
        self.step_size = step_size

    def play_sheep_turn(self, step_size: float) -> None:
        available_directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        chosen_direction = random.choice(available_directions)
        self.move(chosen_direction)

    def move(self, direction: str) -> None:
        moves = {
            "UP": (0, self.step_size),
            "DOWN": (0, -self.step_size),
            "LEFT": (-self.step_size, 0),
            "RIGHT": (self.step_size, 0)
        }
        dx, dy = moves[direction]
        self.x_pos += dx
        self.y_pos += dy

    def __repr__(self) -> str:
        return f"Sheep {self.sheep_id}, {self.x_pos}, {self.y_pos}"

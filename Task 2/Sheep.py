import random


class Sheep:
    def __init__(self,
                 x_pos: float,
                 y_pos: float,
                 sheep_id: int,
                 step_size: float,
                 is_alive: bool = True) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sheep_id = sheep_id
        self.is_alive = is_alive
        self.step_size = step_size

    def play_sheep_turn(self, meadow_range: float) -> None:
        available_directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        chosen_direction = random.choice(available_directions)
        self.move(chosen_direction, meadow_range)

    def move(self, direction: str, meadow_range: float) -> None:
        moves = {
            "UP": (0, self.step_size),
            "DOWN": (0, -self.step_size),
            "LEFT": (-self.step_size, 0),
            "RIGHT": (self.step_size, 0)
        }
        dx, dy = moves[direction]
        self.x_pos += dx
        self.y_pos += dy
        self.x_pos = max(-meadow_range, min(self.x_pos, meadow_range))
        self.y_pos = max(-meadow_range, min(self.y_pos, meadow_range))

    def __repr__(self) -> str:
        return f"Sheep {self.sheep_id}, {self.x_pos}, {self.y_pos}"

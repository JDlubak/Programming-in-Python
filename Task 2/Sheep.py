import random
from logger import log_event


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
        log_event(10, f'Sheep {self.sheep_id} '
                      f'chose direction: {chosen_direction}')
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
        new_x = max(-meadow_range, min(self.x_pos, meadow_range))
        new_y = max(-meadow_range, min(self.y_pos, meadow_range))
        if new_x != self.x_pos or new_y != self.y_pos:
            log_event(30, f'Sheep {self.sheep_id} wanted '
                          f'to escape from meadow, position '
                          f'({self.x_pos}, {self.y_pos}) has been '
                          f'corrected to ({new_x}, {new_y})')
            self.x_pos, self.y_pos = new_x, new_y


        log_event(10, f'Sheep {self.sheep_id} moved to: '
                      f'({self.x_pos}, {self.y_pos})')

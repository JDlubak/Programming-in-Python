from Sheep import Sheep
from logger import log_event
import sys


class Wolf:
    def __init__(self,
                 x_pos: float,
                 y_pos: float,
                 wolf_range: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.wolf_range = wolf_range

    def play_wolf_turn(self, sheep_list: list[Sheep]) -> dict[str, int]:
        try:
            closest_sheep = self.find_closest_sheep(sheep_list)
            if closest_sheep is None:
                log_event(40, f'Wolf has not '
                              f'found any sheep!')
                return {"action": "none", "sheep_id": -1}
            closest_dist = self.calculate_distance_to_sheep(
                closest_sheep.x_pos, closest_sheep.y_pos)
            log_event(10,
                      f'Wolf has detected '
                      f'that Sheep {closest_sheep.sheep_id} '
                      f'is closest: {closest_dist} away')
            log_event(20, f'Wolf is chasing '
                          f'Sheep {closest_sheep.sheep_id} ')
            eat = closest_dist <= self.wolf_range
            sheep_id = self.eat_sheep(closest_sheep) \
                if eat else self.move_to_sheep(closest_sheep)
            log_event(20, 'Wolf has moved')
            log_event(10, f'Wolf has moved to: '
                          f'{self.x_pos}, {self.y_pos}')
            return {
                "action": "eat" if eat else "move",
                "sheep_id": sheep_id
            }
        except Exception as e:
            log_event(40, f'Wolf has encountered an error {e}')
            return {"action": "error", "sheep_id": -1}

    def find_closest_sheep(self,
                           sheep_list:
                           list[Sheep]) -> Sheep:
        alive_sheep_list = [s for s in sheep_list if s.is_alive is True]
        if not alive_sheep_list:
            log_event(30, f'No alive sheep found')
            return None
        return min(alive_sheep_list,
                   key=lambda s: self.calculate_distance_to_sheep(
                       s.x_pos, s.y_pos))

    def calculate_distance_to_sheep(self,
                                    sheep_x_pos: float,
                                    sheep_y_pos: float) -> float:
        return (
                (self.x_pos - sheep_x_pos) ** 2 +
                (self.y_pos - sheep_y_pos) ** 2
        ) ** 0.5

    def move_to_sheep(self, sheep: Sheep) -> int:
        distance = self.calculate_distance_to_sheep(sheep.x_pos,
                                                    sheep.y_pos)
        x_delta = sheep.x_pos - self.x_pos
        y_delta = sheep.y_pos - self.y_pos
        x_movement = x_delta * self.wolf_range / distance
        y_movement = y_delta * self.wolf_range / distance
        self.x_pos += x_movement
        self.y_pos += y_movement
        return sheep.sheep_id

    def eat_sheep(self, sheep: Sheep) -> int:
        if not sheep.is_alive:
            log_event(50, f'Wolf has tried to '
                          f'eat a dead sheep: {sheep.sheep_id}')
            sys.exit(-1)
        sheep.is_alive = False
        self.x_pos, self.y_pos = sheep.x_pos, sheep.y_pos
        sheep.x_pos, sheep.y_pos = None, None
        log_event(20, f'Sheep {sheep.sheep_id} '
                      f'has been eaten')
        return sheep.sheep_id

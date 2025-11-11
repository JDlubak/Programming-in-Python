def print_round_result(r: int,
                       wolf_x_pos: float,
                       wolf_y_pos: float,
                       sheep_counter: int,
                       wolf_action: dict[str, int]) -> None:
    action = "Eaten" if wolf_action["action"] == "eat" else "Chased"
    print("-----------------------------------------------------------")
    print(f'Round {r} outcome')
    print(f'Wolf position: {wolf_x_pos:.3f}, {wolf_y_pos:.3f}')
    print(f'Alive sheep: {sheep_counter}')
    print(f'{action} sheep id: {wolf_action["sheep_id"]}')


def print_simulation_end(last_round: int, max_rounds: int,
                         sheep_counter: int) -> None:
    verb = "has" if sheep_counter == 1 else "have"
    if last_round >= max_rounds:
        print(f'Simulation ended - {sheep_counter} '
              f'sheep {verb} survived!')
    else:
        print(f'Simulation ended - Wolf has eaten '
              f'last sheep on round {last_round}! ')

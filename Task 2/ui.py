

def print_all():
    print1()
    print2()
    print3()


def print_sheep_was_eaten(sheep_id: int) -> None:
    print(f'Eaten sheep: {sheep_id}')
    return


def print_round_result(r: int,
                       wolf_x_pos: float,
                       wolf_y_pos: float,
                       sheep_counter: int,
                       wolf_action: dict[str, int]) -> None:
    action = "Eaten" if wolf_action["action"] == "eat" else "Chased"
    print(f'Round {r} outcome')
    print(f'Wolf position: {wolf_x_pos:.3f}, {wolf_y_pos:.3f}')
    print(f'Alive sheep: {sheep_counter}')
    print(f'{action} sheep id: {wolf_action["sheep_id"]}')


def print1():
    return None


def print2():
    return None


def print3():
    return None

from Simulation import Simulation
from arguments import get_arguments, get_arguments_from_config
from logger import setup_logger, log_event
import os

def main():
    try:
        (config_file, rounds_amount, sheep_amount,
         logging_level, wait_after_round) = get_arguments()
        setup_logger(logging_level)
        meadow_range, sheep_step_size, wolf_attack_range = (
            get_arguments_from_config(config_file) if config_file
            else (10.0, 0.5, 1.0))
        if os.path.exists("pos.json"):
            log_event(30, f'pos.json already exists - '
                          f'it will be overwritten')
        if os.path.exists("alive.csv"):
            log_event(30, f'alive.csv already exists - '
                          f'it will be overwritten')
        simulation = Simulation(max_round=rounds_amount,
                                sheep_amount=sheep_amount,
                                meadow_range=meadow_range,
                                sheep_step_size=sheep_step_size,
                                wolf_attack_range=wolf_attack_range,
                                wait_after_round=wait_after_round)
        simulation.play_simulation()
    except Exception as e:
        log_event(50, f'An error occurred: {e}')


if __name__ == '__main__':
    main()

from Simulation import Simulation
from arguments import get_arguments, get_arguments_from_config


def main():
    (config_file, rounds_amount,
     sheep_amount, wait_after_round) = get_arguments()
    meadow_range, sheep_step_size, wolf_attack_range = (
        get_arguments_from_config(config_file) if config_file
        else (10.0, 0.5, 1.0))
    simulation = Simulation(max_round=rounds_amount,
                            sheep_amount=sheep_amount,
                            meadow_range=meadow_range,
                            sheep_step_size=sheep_step_size,
                            wolf_attack_range=wolf_attack_range,
                            wait_after_round=wait_after_round)
    simulation.play_simulation()


if __name__ == '__main__':
    main()

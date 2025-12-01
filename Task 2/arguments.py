import argparse
import configparser
import os
from logger import log_event, setup_logger

def get_arguments() -> tuple[str | None, int, int, str | None, bool]:
    parser = argparse.ArgumentParser(description='Simulation')
    parser.add_argument(
        '-c', '--config',
        metavar='FILE',
        type=str,
        help='Use configuration file specified by FILE',
    )
    # no need to add --help argument, as it is added automatically
    parser.add_argument(
        '-l', '--log',
        type=str,
        action='store',
        metavar='LEVEL',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help=('Logging events over chosen LEVEL to a chase.log file. \n'
              'Available levels: debug, info, warning, error, critical')
    )
    parser.add_argument(
        '-r', '--rounds',
        default=50,
        metavar='NUM',
        help='Number of rounds in simulation'
    )
    parser.add_argument(
        '-s', '--sheep',
        default=15,
        metavar='NUM',
        help='Number of sheep in simulation'
    )
    parser.add_argument(
        '-w', '--wait',
        action='store_true',
        help="Pause simulation after every round until a key is pressed"
    )
    args = parser.parse_args()
    setup_logger(args.log)
    sheep = validate_number_values(args.sheep, "Sheep amount", 15)
    rounds = validate_number_values(args.rounds, "Round amount", 50)
    return args.config, rounds, sheep, args.wait


def validate_number_values(value: str, name: str, default: int) -> int:
    error_has_occurred = False
    try:
        val = float(value)
    except ValueError:
        error_has_occurred = True
        log_event(40, f'Error in {name}: '
                      f'{value} is not a number!')
        val = None
    if val is not None and not val.is_integer():
        error_has_occurred = True
        log_event(40, f'Error in {name}: '
                      f'{value} is not an integer!')
    if val is not None and val <= 0:
        error_has_occurred = True
        log_event(40, f'Error in {name}: '
                  f'{value} is not a positive number!')
    if error_has_occurred:
        log_event(20, f'Using default ({default}) for {name}.')
        return default
    return int(val)


def get_arguments_from_config(config_file: str) \
        -> tuple[float, float, float]:
    config = configparser.ConfigParser()
    error_has_occurred = False
    if not os.path.exists(config_file):
        log_event(40,f'File {config_file} does not exist! '
                     f'- we will be using default values.')
        error_has_occurred = True
    elif not config_file.endswith(".ini"):
        log_event(40, f'File {config_file} '
                      f'is not a .ini file')
        error_has_occurred = True
    if not error_has_occurred:
        try:
            config.read(config_file)
        except configparser.Error:
            log_event(40, f'Error while parsing {config_file}!')
            error_has_occurred = True

    DEFAULT = (10.0, 0.5, 1.0)

    if not error_has_occurred:
        error_flag, meadow_range, sheep_step_size, wolf_attack_range = \
            get_values_from_config(config)
        if error_flag:
            error_has_occurred = True
    else:
        meadow_range, sheep_step_size, wolf_attack_range = DEFAULT

    if error_has_occurred:
        message_start = (
            "Since error has occurred, we will be using default values: "
        )
    else:
        message_start = f"Loaded values from {config_file}: "
    log_event(10,
              f'{message_start}'
              f'Meadow range: {meadow_range}, '
              f'Sheep step size: {sheep_step_size}, '
              f'Wolf attack range: {wolf_attack_range}')
    return meadow_range, sheep_step_size, wolf_attack_range


def get_values_from_config(config: configparser.ConfigParser) \
        -> tuple[bool, float, float, float]:
    sections = config.sections()
    if sorted(sections) != ['Sheep', 'Wolf']:
        log_event(40, "Invalid config file: it must "
                      "contain [Sheep] and [Wolf] sections")
        return True, 10.0, 0.5, 1.0

    def get_value(section: str, key: str, default: float) -> float:
        error, value = validate_config_value(config, section, key)
        if error:
            log_event(20, f'Default {key} value '
                          f'({default}) has been used.')
            return default
        return value
    meadow_range = get_value('Sheep', 'InitPosLimit', 10.0)
    sheep_step_size = get_value('Sheep', 'MoveDist', 0.5)
    wolf_attack_range = get_value('Wolf', 'MoveDist', 1.0)
    return False, meadow_range, sheep_step_size, wolf_attack_range


def validate_config_value(config: configparser.ConfigParser,
                          section: str, key: str) -> tuple[bool, float]:
    try:
        value = config.getfloat(section, key)
    except Exception:
        log_event(40, f'Error in {section} section: '
                         f'{key} is invalid')
        return True, None
    if value <= 0.0:
        log_event(40, f'Error in {section} section: '
                  f'{key} = {value} is lower than or equal to 0')
        return True, None
    return False, value

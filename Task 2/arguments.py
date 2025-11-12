import argparse
import configparser
import os
from logger import log_event

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
    validate_number_values(args.sheep, "Sheep amount")
    validate_number_values(args.rounds, "Round amount")
    if args.log is not None:
        if args.log.lower() not in ['debug', 'info', 'warning',
                                    'error', 'critical']:
            raise ValueError(f'Invalid log level: {args.log}')
    return (args.config, int(args.rounds), int(args.sheep),
            args.log, args.wait)


def validate_number_values(value: str, name: str) -> None:
    try:
        val = float(value)
    except ValueError:
        raise ValueError(f'Error in {name}: {value} is not a number')
    if not val.is_integer():
        raise ValueError(f'Error in {name}: {value} is not an integer')
    if val <= 0:
        raise ValueError(f'Error in {name}: '
                         f'{value} is lower than or equal to 0')


def get_arguments_from_config(config_file: str) \
        -> tuple[float, float, float]:
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"File {config_file} does not exist")
    if not config_file.endswith(".ini"):
        raise ValueError(f"File {config_file} is not a .ini file")
    try:
        config.read(config_file)
    except configparser.Error:
        raise ValueError(f"Error while parsing {config_file}")
    (meadow_range, sheep_step_size,
     wolf_attack_range) = get_values_from_config(config)
    log_event(10,
              f'Loaded values from {config_file}: '
              f'Meadow range: {meadow_range}, '
              f'Sheep step size: {sheep_step_size}, '
              f'Wolf attack range: {wolf_attack_range}')
    return meadow_range, sheep_step_size, wolf_attack_range


def get_values_from_config(config: configparser.ConfigParser) \
        -> tuple[float, float, float]:
    sections = config.sections()
    if sorted(sections) != ['Sheep', 'Wolf']:
        raise ValueError('Invalid config file: '
                         'it must contain [Sheep] and [Wolf] sections')
    meadow_range = validate_config_value(
        config, 'Sheep', 'InitPosLimit')
    sheep_step_size = validate_config_value(
        config, 'Sheep', 'MoveDist')
    wolf_attack_range = validate_config_value(
        config, 'Wolf', 'MoveDist')

    return meadow_range, sheep_step_size, wolf_attack_range


def validate_config_value(config: configparser.ConfigParser,
                          section: str, key: str) -> float:
    try:
        value = config.getfloat(section, key)
    except Exception:
        raise ValueError(f'Error in {section} section: '
                         f'{key} is invalid')
    if value <= 0.0:
        raise ValueError(f'Error in {section} section: '
                         f'{key} = {value} is lower than or equal to 0')
    return value

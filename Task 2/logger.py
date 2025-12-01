import logging


def log_event(level: int, message: str) -> None:
    logging.log(level, message)


def setup_logger(log_level: str | None) -> None:
    if log_level is not None:
        log_level = log_level.upper()
        level = getattr(logging, log_level)
        filemode = 'w'
    else:
        level = 100     # Level above every other one, which means
        filemode = 'a'  # that nothing will get logged
                        # and file will not be overwritten
    logging.basicConfig(
        filename='chase.log',
        level=level,
        filemode=filemode,
        format='%(asctime)s %(levelname)s (%(levelno)s) %(message)s'
    )

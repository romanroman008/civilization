import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger(name: str,
               level: int = logging.INFO,
               log_filename: str = "bootstrap.log",
               log_dir: str = None,
               max_bytes: int = 10_000_000,
               backup_count: int = 5,
               verbose: bool = False) -> logging.Logger:
    """
    Tworzy logger z obsługą rotacji, konsoli i pliku.
    :param name: nazwa loggera (np. "civilization.world")
    :param level: poziom logowania (domyślnie INFO)
    :param log_filename: nazwa pliku logu
    :param log_dir: ścieżka do folderu logów (domyślnie ./logs)
    :param max_bytes: maksymalny rozmiar logu przed rotacją
    :param backup_count: liczba kopii zapasowych logu
    :param verbose: czy użyć rozszerzonego formatu z path/lineno
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # nie przekazuj logów do root loggera

    if logger.handlers:
        return logger

    # Formatowanie
    if verbose:
        fmt = '[%(levelname)s] %(asctime)s - %(name)s - %(pathname)s:%(lineno)d - %(message)s'
    else:
        fmt = '[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt, datefmt='%H:%M:%S')

    # Handlery
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Ścieżka logu
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    log_dir = log_dir or os.path.join(project_root, "logs")

    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, log_filename)

    file_handler = RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Przykład użycia:
logger = get_logger("civilization.world", level=logging.DEBUG, log_filename="world.log", verbose=True)
logger.debug("Logger initialized for world module.")

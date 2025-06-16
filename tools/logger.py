import logging
import os

def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s', datefmt='%H:%M:%S')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
    os.makedirs(log_dir, exist_ok=True)

    file_path = os.path.join(log_dir, 'world_generation.log')
    file_handler = logging.FileHandler(file_path, mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

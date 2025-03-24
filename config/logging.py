import os
import logging
from datetime import datetime


def setup_logging(log_name="slack_confluence_sync"):
    # Директория логов относительно текущего файла
    log_dir = os.path.join(os.path.dirname(__file__), "../data/logs")
    os.makedirs(log_dir, exist_ok=True)

    # Имя файла с датой
    log_file = os.path.join(
        log_dir, f"{log_name}_{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    # Настройка базового логгера
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Возвращаем логгер с именем log_name
    return logging.getLogger(log_name)


def get_logger(name=None):
    # Если имя указано — вернём логгер с этим именем
    if name:
        return logging.getLogger(name)
    # Если нет — логгер по умолчанию
    return logging.getLogger("slack_confluence_sync")

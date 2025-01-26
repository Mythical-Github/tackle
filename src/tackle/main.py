import time

start_time = time.time()

from tackle import cli
from tackle.log import logger
from tackle.log_info import LOG_INFO
from tackle.file_io import SCRIPT_DIR
from tackle.customization import enable_vt100


def main_logic():
    try:
        enable_vt100()
        logger.set_log_base_dir(SCRIPT_DIR)
        logger.configure_logging(LOG_INFO)
        cli.cli()
    except Exception as error_message:
        logger.log_message(str(error_message))

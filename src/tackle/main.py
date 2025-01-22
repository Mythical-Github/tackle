import time

start_time = time.time()

from tackle import cli
from tackle import log
from tackle.log_info import LOG_INFO
from tackle.settings import SCRIPT_DIR
from tackle.customization import enable_vt100


def main_logic():
    try:
        enable_vt100()
        log.set_log_base_dir(SCRIPT_DIR)
        log.configure_logging(LOG_INFO)
        cli.cli_logic()
    except Exception as error_message:
        log.log_message(str(error_message))

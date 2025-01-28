from tackle import log


def create_offline_packages(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str]
):
    log.logger.log_message('test')


def install_offline_packages(
    offline_install_packages: list[str],
    skip_tracking_installs: bool
):
    log.logger.log_message('test')

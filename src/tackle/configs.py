import os
import shutil

from tackle.log import logger
from tackle.file_io import SCRIPT_DIR


def generate_configs_from_template(base_config: str, output_configs: list[str]):
    template_config = os.path.normpath(base_config)
    if not os.path.isfile(template_config):
        raise FileNotFoundError()
    for config in output_configs:
        if os.path.isabs(config):
            os.makedirs(os.path.dirname(os.path.normpath(config)), exist_ok=True)
            if os.path.isfile(config):
                warning_message = f'This following config already exists, and will not be recreated: "{config}"'
                raise Warning(warning_message)
            else:
                shutil.copy(template_config, config)
                success_message = f'This following config was created from the template config: "{config}"'
                logger.log_message(success_message)
        else:
            os.makedirs(os.path.dirname(os.path.normpath(config)), exist_ok=True)
            if os.path.isfile(config):
                warning_message = f'This following config already exists, and will not be recreated: "{config}"'
                logger.log_message(warning_message)
                raise Warning(warning_message)
            else:
                new_config_path = os.path.normpath(f'{SCRIPT_DIR}/{config}')
                shutil.copy(template_config, new_config_path)
                success_message = f'This following config was created from the template config: "{new_config_path}"'
                logger.log_message(success_message)


def get_game_names_from_game_configs(game_names: list[str]) -> list[str]:
    game_names = []
    return game_names


def get_project_names_from_project_configs(project_names: list[str]) -> list[str]:
    project_names = []
    return project_names

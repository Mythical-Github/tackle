import os
import shutil

import click
from trogon import tui

from tackle.log import logger
from tackle.file_io import SCRIPT_DIR


@tui()
@click.group()
def cli():
    pass


@cli.command(name='install_dependencies')

@click.option(
    '--project_configs',
    default=[],
    help='A list of project config names/paths to install dependencies for.',
    multiple=True
)

@click.option(
    '--game_configs',
    default=[],
    help='A list of game config names/paths to install dependencies for.',
    multiple=True
)

@click.option(
    '--dependencies_configs',
    default=[],
    help='A list of dependency config names/paths to install dependencies from.',
    multiple=True
)

@click.option(
    '--install_offline_packages',
    default=[],
    help='A list of paths to offline installable packages generated from tackle to install.',
    multiple=True
)

@click.option(
    '--create_offline_packages',
    default=False,
    help='Creates offline installable packages for offline installation.'
)

@click.option(
    '--generate_wrappers',
    default=False,
    help='Whether or not to create a wrapper to rerun the command that was generated from the CLI/TUI.'
)

@click.option(
    '--reinstall_dependencies',
    default=False,
    help='Whether or not to reinstall dependencies that already have been installed for this installation.'
)


def install_dependencies(
    project_configs: list[str],
    game_configs: list[str],
    dependencies_configs: list[str],
    offline_install_packages: list[str],
    create_offline_packages: list[str],
    generate_wrappers: bool,
    reinstall_dependencies: bool
):
    print(str(reinstall_dependencies))


@cli.command(name='generate_dependency_configs')

@click.option(
    '--configs',
    default=[],
    help='A list of config names/paths to create dependency configs at.',
    multiple=True
)


def generate_dependency_configs(configs):
    template_config = os.path.normpath(f'{SCRIPT_DIR}/assets/template_files/dependency.toml')
    if not os.path.isfile(template_config):
        raise FileNotFoundError()
    for config in configs:
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


@cli.command(name='generate_project_configs')

@click.option(
    '--project_config_paths',
    default=[],
    help='A list of names/paths to create project configs at.',
    multiple=True
)


def generate_project_configs(configs):
    template_config = os.path.normpath(f'{SCRIPT_DIR}/assets/template_files/project.toml')
    if not os.path.isfile(template_config):
        raise FileNotFoundError()
    for config in configs:
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


@cli.command(name='generate_game_configs')

@click.option(
    '--game_config_paths',
    default=[],
    help='A list of names/paths to create games configs at.',
    multiple=True
)


def generate_game_configs(configs):
    template_config = os.path.normpath(f'{SCRIPT_DIR}/assets/template_files/game.toml')
    if not os.path.isfile(template_config):
        raise FileNotFoundError()
    for config in configs:
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

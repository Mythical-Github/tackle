import click
from trogon import tui

from tackle import installer
from tackle.file_io import SCRIPT_DIR
from tackle.configs import generate_configs_from_template


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
    installer.install_dependencies(
    project_configs,
    game_configs,
    dependencies_configs,
    offline_install_packages,
    create_offline_packages,
    generate_wrappers,
    reinstall_dependencies
)


@cli.command(name='generate_dependency_configs')

@click.option(
    '--configs',
    default=[],
    help='A list of config names/paths to create dependency configs at.',
    multiple=True
)


def generate_dependency_configs(configs: list[str]):
    generate_configs_from_template(
        base_config=f'{SCRIPT_DIR}/assets/template_files/dependency.toml', 
        output_configs=configs
    )


@cli.command(name='generate_project_configs')

@click.option(
    '--project_config_paths',
    default=[],
    help='A list of names/paths to create project configs at.',
    multiple=True
)


def generate_project_configs(configs: list[str]):
    generate_configs_from_template(
        base_config=f'{SCRIPT_DIR}/assets/template_files/project.toml', 
        output_configs=configs
    )


@cli.command(name='generate_game_configs')

@click.option(
    '--game_config_paths',
    default=[],
    help='A list of names/paths to create games configs at.',
    multiple=True
)


def generate_game_configs(configs: list[str]):
    generate_configs_from_template(
        base_config=f'{SCRIPT_DIR}/assets/template_files/game.toml', 
        output_configs=configs
    )

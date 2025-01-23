import click
from trogon import tui


@tui()
@click.group()
def cli():
    pass


@cli.command(name='install_dependencies')

@click.option(
    '--project_names',
    default=[],
    help='A list of project names to install dependencies for.',
    multiple=True
)

@click.option(
    '--game_names',
    default=[],
    help='A list of game names to install dependencies for.',
    multiple=True
)

@click.option(
    '--specific_dependencies_names',
    default=[],
    help='A list of dependency config names to install dependencies from.',
    multiple=True
)

@click.option(
    '--offline_install_packages',
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
    project_names: list[str],
    game_names: list[str],
    specific_dependencies_names: list[str],
    offline_install_packages: list[str],
    create_offline_packages: list[str],
    generate_wrappers: bool,
    reinstall_dependencies: bool
):
    print(str(reinstall_dependencies))


@cli.command(name='generate_new_dependency_directory')

@click.option(
    '--directories',
    default=[],
    help='A list of directories to create new dependency setups.',
    multiple=True
)


def generate_new_dependency_directory(directories):
    for directory in directories:
        print(directory)


@cli.command(name='generate_new_project_config')

@click.option(
    '--project_config_paths',
    default=[],
    help='A list of paths to create new project configs at.',
    multiple=True
)


def generate_new_project_config(project_config_paths):
    for project_config_path in project_config_paths:
        print(project_config_path)


@cli.command(name='generate_new_game_config')

@click.option(
    '--game_config_paths',
    default=[],
    help='A list of paths to create new games configs at.',
    multiple=True
)


def generate_new_game_config(game_config_paths):
    for game_config_path in game_config_paths:
        print(game_config_path)

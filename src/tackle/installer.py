import tomlkit

from tackle import (
    configs, 
    wrappers, 
    dependencies, 
    offline_packages
)


def install_dependencies_from_configs(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    reinstall_dependencies: bool
):
    project_names = configs.get_project_names_from_project_configs(project_configs)
    game_names = configs.get_game_names_from_game_configs(game_configs)
    dependency_hashes = dependencies.get_dependency_hashes_dependency_configs(dependency_configs)
    dependency_hashes.extend(dependencies.get_dependency_hashes_from_game_names(game_names))
    dependency_hashes.extend(dependencies.get_dependency_hashes_from_project_names(project_names))
    for dependency_hash in dependency_hashes:
        if reinstall_dependencies:
            dependencies.install_dependency_from_hash(dependency_hash)
        else:
            if not dependencies.has_dependency_already_been_installed(hash):
                dependencies.install_dependency_from_hash(dependency_hash)


def install_dependencies(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    offline_install_packages: list[str],
    create_offline_packages: list[str],
    generate_wrappers: bool,
    reinstall_dependencies: bool
):
    if not len(project_configs) + len(game_configs) + len(dependency_configs) + len(offline_install_packages) > 0:
        print('warning that you no thing to be installed or created to be installed are being passed')
    if not len(project_configs) + len(game_configs) + len(dependency_configs) > 0 and create_offline_packages:
        print('warning that you cannot create offline install packages without any configs being passed in')
    if generate_wrappers:
        wrappers.generate_wrappers()
    if create_offline_packages:
        offline_packages.create_offline_packages(
            project_configs, 
            game_configs, 
            dependency_configs
        )
    if len(offline_install_packages) > 0:
        offline_packages.install_offline_packages(offline_install_packages)
    if len(project_configs) + len(game_configs) + len(dependency_configs) > 0:
        install_dependencies_from_configs(
            project_configs, 
            game_configs, 
            dependency_configs,
            reinstall_dependencies
        )

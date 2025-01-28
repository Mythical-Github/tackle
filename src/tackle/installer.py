import os
import subprocess
from itertools import chain

from tackle import (
    configs, 
    wrappers,
    file_io,
    dependencies, 
    offline_packages,
    data_structures,
    log
)


def turn_command_into_str(command: data_structures.Command) -> str:
    command_str = os.path.normpath(f'{file_io.SCRIPT_DIR}/temp/{command.executable}')
    for arg in command.executable_args:
        command_str = f'{command_str} {arg}'
    return command_str


def run_command_halting(command):
    command_str = turn_command_into_str(command)
    subprocess.run(command_str, shell=True, cwd=file_io.SCRIPT_DIR)


def run_command_non_halting(command):
    command_str = turn_command_into_str(command)
    subprocess.Popen(command_str, shell=True, cwd=file_io.SCRIPT_DIR)


def run_command_non_halting_wait(command):
    command_str = turn_command_into_str(command)
    process = subprocess.Popen(command_str, shell=True, cwd=file_io.SCRIPT_DIR)
    process.wait()


def download_dependency(
        executable: str,
        sha_256_hash: str,
        download_links: list[str]
    ) -> str:
    log.logger.log_message('Downloading dependency')
    path_to_dependency = os.path.normpath(f'{file_io.SCRIPT_DIR}/temp/{executable}')
    os.makedirs(os.path.dirname(path_to_dependency), exist_ok=True)

    if os.path.isfile(path_to_dependency):
        os.remove(path_to_dependency)

    for download_link in download_links:
        if file_io.download_file(download_link, path_to_dependency):
            if file_io.calculate_sha256(path_to_dependency) == sha_256_hash:
                break
            else:
                os.remove(path_to_dependency)

    if not os.path.exists(path_to_dependency):
        raise Warning(f"Dependency {executable} could not be downloaded or verified.")
    
    return path_to_dependency


def install_dependency_from_hash(
        hash: str,
        skip_tracking_installs: bool
    ):
    log.logger.log_message('Installing dependency from hash')
    config = configs.get_dependency_config_from_hash(hash)
    command = configs.from_dependency_config_get_command(config)
    executable_method = data_structures.get_enum_from_val(data_structures.ExecutionMethod, command.executable_method[0])
    download_links = configs.from_dependency_config_get_download_links(config)
    sha_256_hash = configs.from_dependency_config_get_sha_256_hash(config)
    dependency = download_dependency(command.executable, sha_256_hash, download_links)
    if not skip_tracking_installs:
        configs.add_hash_to_install_tracker_config(hash)
    if not os.path.isfile(dependency):
        raise FileNotFoundError
    if executable_method == data_structures.ExecutionMethod.HALTING:
        run_command_halting(command)
    elif executable_method == data_structures.ExecutionMethod.NON_HALTING:
        run_command_non_halting(command)
    elif executable_method == data_structures.ExecutionMethod.NON_HALTING_WAIT:
        run_command_non_halting_wait(command)
    else:
        error_message = f'There was no execution_method provided or it was invalid'
        print(command.executable_method[0])
        print(executable_method)
        raise RuntimeError(error_message)
    

def install_dependencies_from_configs(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    reinstall_dependencies: bool,
    skip_tracking_installs: bool
):
    project_names = configs.get_project_names_from_project_configs(project_configs).values()
    game_names = configs.get_config_to_game_names_from_game_configs(game_configs).values()
    dependency_hashes = list(dependencies.get_dependency_configs_to_dependency_hashes(dependency_configs).values())
    test = dependencies.get_game_names_to_dependency_hash_lists(game_names)
    dependency_hashes.extend(list(chain.from_iterable(test.values())))
    dependency_hashes.extend(list(chain.from_iterable(dependencies.get_project_names_to_dependency_hash_lists(project_names).values())))
    for dependency_hash in dependency_hashes:
        log.logger.log_message(dependency_hash)
        if reinstall_dependencies:
            install_dependency_from_hash(dependency_hash, skip_tracking_installs)
        else:
            if not dependencies.has_dependency_already_been_installed(dependency_hash):
                install_dependency_from_hash(dependency_hash, skip_tracking_installs)


def install_dependencies(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    offline_install_packages: list[str],
    create_offline_packages: list[str],
    wrapper_name: str,
    reinstall_dependencies: bool,
    skip_tracking_installs: bool
):
    if not len(project_configs) + len(game_configs) + len(dependency_configs) + len(offline_install_packages) > 0:
        log.logger.log_message('warning that you no thing to be installed or created to be installed are being passed')
    if not len(project_configs) + len(game_configs) + len(dependency_configs) > 0 and create_offline_packages:
        log.logger.log_message('warning that you cannot create offline install packages without any configs being passed in')
    wrappers.generate_wrapper(wrapper_name)
    if create_offline_packages:
        offline_packages.create_offline_packages(
            project_configs, 
            game_configs, 
            dependency_configs
        )
    if len(offline_install_packages) > 0:
        offline_packages.install_offline_packages(offline_install_packages, skip_tracking_installs)
    if len(project_configs) + len(game_configs) + len(dependency_configs) > 0:
        install_dependencies_from_configs(
            project_configs, 
            game_configs, 
            dependency_configs,
            reinstall_dependencies,
            skip_tracking_installs
        )

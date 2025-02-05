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


def turn_command_into_str(command: data_structures.Command, hash: str, offline_install: bool) -> str:
    if offline_install:
        command_str = os.path.normpath(f'{file_io.SCRIPT_DIR}/assets/dependencies/{hash}/{command.executable}')
        for arg in command.executable_args:
            command_str = f'{command_str} {arg}'
        print(f'latest command string to run: "{command_str}"')
        return command_str
    else:
        command_str = os.path.normpath(f'{file_io.SCRIPT_DIR}/temp/{hash}/{command.executable}')
        for arg in command.executable_args:
            command_str = f'{command_str} {arg}'
        print(f'latest command string to run: "{command_str}"')
        return command_str


def run_command_halting(command, hash: str, offline_install: bool):
    subprocess.run(turn_command_into_str(command, hash, offline_install), shell=True, cwd=file_io.SCRIPT_DIR)


def run_command_non_halting(command, hash: str, offline_install: bool):
    subprocess.Popen(turn_command_into_str(command, hash, offline_install), shell=True, cwd=file_io.SCRIPT_DIR)


def run_command_non_halting_wait(command, hash: str, offline_install: bool):
    process = subprocess.Popen(turn_command_into_str(command, hash, offline_install), shell=True, cwd=file_io.SCRIPT_DIR)
    process.wait()


def download_dependency(
        executable: str,
        sha_256_hash: str,
        download_links: list[str]
    ) -> str:
    log.logger.log_message('Downloading dependency')
    path_to_dependency = os.path.normpath(f'{file_io.SCRIPT_DIR}/temp/{sha_256_hash}/{executable}')
    os.makedirs(os.path.dirname(path_to_dependency), exist_ok=True)

    download_success = file_io.attempt_hash_verified_download_from_download_links(
        executable=executable, 
        sha_256_hash=sha_256_hash, 
        download_links=download_links,
        output_directory=os.path.normpath(f'{file_io.SCRIPT_DIR}/temp')
    )

    if not download_success:
        raise Warning(f"Dependency {executable} could not be downloaded or verified.")
    
    return path_to_dependency


def get_all_directories_in_directory(directory: str) -> list[str]:
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]


def get_directory_name_from_directory_path(directory_path: str) -> str:
    return os.path.basename(os.path.normpath(directory_path))


def find_dependency_from_hash(command: data_structures.Command, hash_str: str) -> str:
    main_deps_dir = os.path.normpath(f'{file_io.SCRIPT_DIR}/assets/dependencies')
    dependency_file = os.path.normpath(f'{main_deps_dir}/{hash_str}/{command.executable}')
    print(f'dependency file: {dependency_file}')
    if not os.path.isfile(dependency_file):
        raise FileNotFoundError('Could not find the desired dependency file.')
    if hash_str == file_io.get_sha_256_hash(dependency_file):
        return(dependency_file)
    else:
        invalid_hash_error = f'The following hash was compared to an invalid file: "{hash_str}"'
        log.logger.log_message(invalid_hash_error)
        raise RuntimeError(invalid_hash_error)


def install_dependency_from_hash(
        hash: str,
        skip_tracking_installs: bool,
        offline_install: bool
    ):
    log.logger.log_message('Installing dependency from hash')
    config = configs.get_dependency_config_from_hash(hash)
    command = configs.from_dependency_config_get_command(config)
    executable_method = data_structures.get_enum_from_val(data_structures.ExecutionMethod, command.executable_method[0])
    download_links = configs.from_dependency_config_get_download_links(config)
    sha_256_hash = configs.from_dependency_config_get_sha_256_hash(config)

    if offline_install:
        dependency = find_dependency_from_hash(command, hash)
        if os.path.isfile(dependency):
            dependency_hash = file_io.get_sha_256_hash(dependency)
            if not hash == dependency_hash:
                invalid_hash_error = f'The following hash was compared to an invalid file: "{hash}"'
                log.logger.log_message(invalid_hash_error)
                raise RuntimeError(invalid_hash_error)
        else:        
            raise FileNotFoundError
    else:
        dependency = download_dependency(command.executable, sha_256_hash, download_links)

    if not skip_tracking_installs:
        configs.add_hash_to_install_tracker_config(hash)
    if not os.path.isfile(dependency):
        raise FileNotFoundError
    print(f'Full Dependency Path: "{dependency}"')
    if executable_method == data_structures.ExecutionMethod.HALTING:
        run_command_halting(command, sha_256_hash, offline_install)
    elif executable_method == data_structures.ExecutionMethod.NON_HALTING:
        run_command_non_halting(command, sha_256_hash, offline_install)
    elif executable_method == data_structures.ExecutionMethod.NON_HALTING_WAIT:
        run_command_non_halting_wait(command, sha_256_hash, offline_install)
    else:
        error_message = f'There was no execution_method provided or it was invalid'
        raise RuntimeError(error_message)
    

def install_dependencies_online(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    reinstall_dependencies: bool,
    skip_tracking_installs: bool
):
    project_names = configs.get_project_configs_to_project_names(project_configs).values()
    game_names = configs.get_config_to_game_names_from_game_configs(game_configs).values()
    dependency_hashes = list(dependencies.get_dependency_configs_to_dependency_hashes(dependency_configs).values())
    test = dependencies.get_game_names_to_dependency_hash_lists(game_names)
    dependency_hashes.extend(list(chain.from_iterable(test.values())))
    dependency_hashes.extend(list(chain.from_iterable(dependencies.get_project_names_to_dependency_hash_lists(project_names).values())))
    for dependency_hash in dependency_hashes:
        log.logger.log_message(dependency_hash)
        if reinstall_dependencies:
            install_dependency_from_hash(dependency_hash, skip_tracking_installs, False)
        else:
            if not dependencies.has_dependency_already_been_installed(dependency_hash):
                install_dependency_from_hash(dependency_hash, skip_tracking_installs, False)


def install_dependencies(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    offline_install: bool,
    create_offline_packages: list[str],
    wrapper_name: str,
    reinstall_dependencies: bool,
    skip_tracking_installs: bool,
    skip_installation: bool
):
    all_configs_length = len(project_configs) + len(game_configs) + len(dependency_configs)
    if not all_configs_length > 0:
        no_configs_error_message = 'Error: You have chosen to install dependencies without passing any configs in.'
        log.logger.log_message(no_configs_error_message)
        raise RuntimeError(no_configs_error_message)

    wrappers.generate_wrapper(wrapper_name)

    if create_offline_packages:
        offline_packages.create_offline_packages(
            project_configs, 
            game_configs, 
            dependency_configs,
            wrapper_name
        )

    if not skip_installation:
            if offline_install:
                offline_packages.install_dependencies_offline(
                        project_configs, 
                        game_configs, 
                        dependency_configs,
                        reinstall_dependencies,
                        skip_tracking_installs
                    )
            else:
                install_dependencies_online(
                    project_configs, 
                    game_configs, 
                    dependency_configs,
                    reinstall_dependencies,
                    skip_tracking_installs
                )

import os
import glob
import shutil

import tomlkit

from tackle import log
from tackle import file_io
from tackle import data_structures


def get_dependency_config_from_hash(hash: str) -> str:
    dependency_config = None
    for config in get_all_dependency_configs():
        hash_to_compare_to = from_dependency_config_get_sha_256_hash(config)
        if hash == hash_to_compare_to:
            dependency_config = config
    return dependency_config


def add_hash_to_install_tracker_config(hash: str):
    toml_path = get_install_tracker_config()
    new_hash_list = get_hashes()
    new_hash_list.append(hash)

    with open(toml_path, "r") as toml_file:
        toml_content = tomlkit.parse(toml_file.read())

    dependency_config = toml_content.get("dependency_config_structure")
    if dependency_config:
        dependency_config["hashes"] = new_hash_list

    with open(toml_path, "w") as toml_file:
        toml_file.write(tomlkit.dumps(toml_content))

    log.logger.log_message(f"Hash {hash} added successfully.")


def from_dependency_config_get_config_spec_version(dependency_config: str) -> float:
    try:
        with open(dependency_config, 'r') as file:
            content = file.read()
        project_config = tomlkit.parse(content)
        structure = project_config["dependency_config_structure"]
        value = structure['config_spec_version']
    except Exception as e:
        raise RuntimeError(f"Error processing {dependency_config}: {e}")
    return value


def from_dependency_config_get_config_version(dependency_config: str) -> float:
    try:
        with open(dependency_config, 'r') as file:
            content = file.read()
        project_config = tomlkit.parse(content)
        structure = project_config["dependency_config_structure"]
        value = structure['config_version']
    except Exception as e:
        raise RuntimeError(f"Error processing {dependency_config}: {e}")
    return value


def from_dependency_config_get_display_name(dependency_config: str) -> str:
    try:
        with open(dependency_config, 'r') as file:
            content = file.read()
        project_config = tomlkit.parse(content)
        structure = project_config["dependency_config_structure"]
        value = structure['display_name']
    except Exception as e:
        raise RuntimeError(f"Error processing {dependency_config}: {e}")
    return value


def from_dependency_config_get_sha_256_hash(dependency_config: str) -> str:
    try:
        with open(dependency_config, 'r') as file:
            content = file.read()
        project_config = tomlkit.parse(content)
        structure = project_config["dependency_config_structure"]
        value = structure['sha_256_hash']
    except Exception as e:
        raise RuntimeError(f"Error processing {dependency_config}: {e}")
    return value


def from_dependency_config_get_download_links(dependency_config: str) -> list[str]:
    try:
        with open(dependency_config, 'r') as file:
            content = file.read()
        project_config = tomlkit.parse(content)
        structure = project_config["dependency_config_structure"]
        value = structure['download_links']
    except Exception as e:
        raise RuntimeError(f"Error processing {dependency_config}: {e}")
    return value


def from_dependency_config_get_command(dependency_config: str) -> data_structures.Command:
    try:
        with open(dependency_config, 'r') as file:
            content = file.read()
        project_config = tomlkit.parse(content)
        structure = project_config["dependency_config_structure"]
        config_command = structure['command']
        command = data_structures.Command(
            config_command['executable'], 
            config_command['executable_args'], 
            config_command.get('execution_method', data_structures.ExecutionMethod.NON_HALTING_WAIT)
        )
    except Exception as e:
        raise RuntimeError(f"Error processing {dependency_config}: {e}")
    return command


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
                log.logger.log_message(success_message)
        else:
            os.makedirs(os.path.dirname(os.path.normpath(config)), exist_ok=True)
            if os.path.isfile(config):
                warning_message = f'This following config already exists, and will not be recreated: "{config}"'
                log.logger.log_message(warning_message)
                raise Warning(warning_message)
            else:
                new_config_path = os.path.normpath(f'{file_io.SCRIPT_DIR}/{config}')
                shutil.copy(template_config, new_config_path)
                success_message = f'This following config was created from the template config: "{new_config_path}"'
                log.logger.log_message(success_message)


def get_config_to_game_names_from_game_configs(game_configs: list[str]) -> dict[str, str]:
    configs_to_game_names = {}
    for game_config_path in game_configs:
        try:
            with open(game_config_path, 'r') as file:
                content = file.read()
            game_config = tomlkit.parse(content)
            structure = game_config["game_config_structure"]
            game_info = structure["game_info"]
            game_display_name = game_info["game_display_name"]
            configs_to_game_names[game_config_path] = game_display_name
        except KeyError as e:
            raise KeyError(f"Missing required key {e} in config: {game_config_path}")
        except Exception as e:
            raise RuntimeError(f"Error processing {game_config_path}: {e}")
    return configs_to_game_names


def get_project_names_from_project_configs(project_configs: list[str]) -> dict[str, str]:
    configs_to_project_names = {}
    for project_config_path in project_configs:
        try:
            with open(project_config_path, 'r') as file:
                content = file.read()
            project_config = tomlkit.parse(content)
            structure = project_config["project_config_structure"]
            project_info = structure["project_info"]
            project_display_name = project_info["display_name"]
            configs_to_project_names[project_config_path] = project_display_name
        except KeyError as e:
            raise KeyError(f"Missing required key {e} in config: {project_config_path}")
        except Exception as e:
            raise RuntimeError(f"Error processing {project_config_path}: {e}")
    return configs_to_project_names


def get_all_configs() -> list[str]:
    return glob.glob(f"{file_io.SCRIPT_DIR}/assets/configs/**/*.toml", recursive=True)


def get_all_dependency_configs() -> list[str]:
    toml_files = []

    search_path = os.path.normpath(f"{file_io.SCRIPT_DIR}/assets/configs/dependencies")

    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith(".toml"):
                toml_files.append(os.path.join(root, file))

    return toml_files


def get_all_game_configs() -> list[str]:
    return glob.glob(f"{file_io.SCRIPT_DIR}/assets/configs/games/**/*.toml", recursive=True)


def get_all_project_configs() -> list[str]:
    return glob.glob(f"{file_io.SCRIPT_DIR}/assets/configs/projects/**/*.toml", recursive=True)


def get_install_tracker_config_path() -> str:
    return os.path.normpath(f'{file_io.SCRIPT_DIR}/assets/configs/install_tracker.toml')


def get_install_tracker_config() -> str:
    tracker_path = get_install_tracker_config_path()
    if not os.path.isfile(tracker_path):
        create_install_tracker_config()
    return tracker_path


def create_install_tracker_config():
    toml_path = get_install_tracker_config_path()

    toml_content = tomlkit.document()
    dependency_config_structure = tomlkit.table()
    dependency_config_structure["config_spec_version"] = get_current_config_spec_version()
    dependency_config_structure["config_version"] = get_current_config_version()

    hashes = tomlkit.table()
    hashes["hashes"] = []
    dependency_config_structure["hashes"] = hashes

    toml_content["dependency_config_structure"] = dependency_config_structure

    with open(toml_path, "w") as toml_file:
        toml_file.write(tomlkit.dumps(toml_content))


def get_config_spec_version() -> float:
    toml_path = get_install_tracker_config()

    with open(toml_path, "r") as toml_file:
        toml_content = tomlkit.parse(toml_file.read())

    dependency_config = toml_content.get("dependency_config_structure")
    return dependency_config.get("config_spec_version")


def get_config_version():
    toml_path = get_install_tracker_config()

    with open(toml_path, "r") as toml_file:
        toml_content = tomlkit.parse(toml_file.read())

    dependency_config = toml_content.get("dependency_config_structure")
    return dependency_config.get("config_version")


def get_hashes() -> list[str]:
    toml_path = get_install_tracker_config()

    with open(toml_path, "r") as toml_file:
        toml_content = tomlkit.parse(toml_file.read())

    dependency_config = toml_content.get("dependency_config_structure")
    hashes = dependency_config.get("hashes")

    return list(hashes)


def get_current_config_spec_version() -> float:
    return 1.0


def get_current_config_version() -> float:
    return 1.0

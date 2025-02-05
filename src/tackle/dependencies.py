from tomlkit import parse

from tackle import configs


def has_dependency_already_been_installed(hash: str) -> bool:
    return hash in configs.get_hashes_of_already_installed()


def get_project_names_to_dependency_hash_lists(project_names: list[str]) -> dict[str, list[str]]:
    project_names_to_dependency_hash_lists = {}
    for config in configs.get_all_dependency_configs():
        try:
            with open(config, 'r') as file:
                content = file.read()
            dependency_config = parse(content)
            structure = dependency_config.get("dependency_config_structure", {})
            
            compatible_projects = structure.get("compatible_projects", [])
            sha_256_hash = structure.get("sha_256_hash", None)
            
            for project in compatible_projects:
                display_name = project.get("display_name")
                if display_name in project_names:
                    if display_name not in project_names_to_dependency_hash_lists:
                        project_names_to_dependency_hash_lists[display_name] = []
                    if sha_256_hash:
                        project_names_to_dependency_hash_lists[display_name].append(sha_256_hash)
        except Exception as e:
            raise RuntimeError(f"Error processing {config}: {e}")
    return project_names_to_dependency_hash_lists


def get_game_names_to_dependency_hash_lists(game_names: list[str]) -> dict[str, list[str]]:
    game_names_to_dependency_hash_lists = {}
    for config in configs.get_all_dependency_configs():
        try:
            with open(config, 'r') as file:
                content = file.read()
            dependency_config = parse(content)
            structure = dependency_config.get("dependency_config_structure", {})
            
            compatible_projects = structure.get("compatible_games", [])
            sha_256_hash = structure.get("sha_256_hash", None)
            
            for project in compatible_projects:
                display_name = project.get("game_display_name")
                if display_name in game_names:
                    if display_name not in game_names_to_dependency_hash_lists:
                        game_names_to_dependency_hash_lists[display_name] = []
                    if sha_256_hash:
                        game_names_to_dependency_hash_lists[display_name].append(sha_256_hash)
        except Exception as e:
            raise RuntimeError(f"Error processing {config}: {e}")
    return game_names_to_dependency_hash_lists


def get_dependency_configs_to_dependency_hashes(dependency_configs: list[str]) -> dict[str, str]:
    dependency_configs_to_dependency_hashes = {}
    for dependency_config_path in dependency_configs:
        try:
            with open(dependency_config_path, 'r') as file:
                content = file.read()
            dependency_configs_to_dependency_hashes[dependency_config_path] = parse(content)["dependency_config_structure"]["sha_256_hash"]
        except Exception as e:
            raise RuntimeError(f"Error processing {dependency_config_path}: {e}")
    return dependency_configs_to_dependency_hashes

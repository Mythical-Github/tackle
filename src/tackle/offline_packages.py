import os
import shutil
import zipfile
import tempfile
import subprocess

from tomlkit import parse, document

from tackle import log, configs, file_io, data_structures, wrappers, settings, installer


# each zip will contain a wrapper, a toml, the provided configs in the configs folder, and a folder of dependencies
# a template bat will be created in the dist directory alongside the zip to install it from an online source
# it will also contain a zip to offline, unzip the zip and install things
# each toml will have the wrapper name in it
# the wrapper name will have the various configs to install info in it
# each bat that unpacks then runs the wrapper must have a hash check for the zip before unzipping it


def copy_configs_over(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str]
):
    dst_project_config_dir = f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/assets/configs/projects'
    os.makedirs(dst_project_config_dir, exist_ok=True)

    for source_project_config in project_configs:
        destination_project_config = os.path.normpath(f'{dst_project_config_dir}/{os.path.basename(source_project_config)}')
        shutil.copy(source_project_config, destination_project_config)


    dst_game_config_dir = f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/assets/configs/games'
    os.makedirs(dst_game_config_dir, exist_ok=True)

    for source_game_config in game_configs:
        destination_game_config = os.path.normpath(f'{dst_game_config_dir}/{os.path.basename(source_game_config)}')
        shutil.copy(source_game_config, destination_game_config)


    dst_dependency_config_dir = f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/assets/configs/dependencies'
    os.makedirs(dst_dependency_config_dir, exist_ok=True)

    flat_dependency_configs = [path for sublist in dependency_configs for path in sublist]

    for source_dependency_config in flat_dependency_configs:
        destination_dependency_config = os.path.normpath(
            os.path.join(dst_dependency_config_dir, os.path.basename(source_dependency_config))
        )
        shutil.copy(source_dependency_config, destination_dependency_config)


def copy_tackle_over():
    if file_io.is_exe():
        src_file = os.path.normpath(f'{file_io.SCRIPT_DIR}/tackle.exe')
        destination_file = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/tackle.exe')
    else:
        # copy the source code over later
        src_file = os.path.normpath(f'{file_io.SCRIPT_DIR}/__main__.py')
        destination_file = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/__main__.py')
    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
    shutil.copy(src_file, destination_file)


def install_dependencies_offline(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    reinstall_dependencies: bool,
    skip_tracking_installs: bool
):
    hashes = []
    for config in dependency_configs:
        hashes.append(configs.from_dependency_config_get_sha_256_hash(config))
    for hash in hashes:
        if not reinstall_dependencies and not hash in configs.get_hashes_of_already_installed():
            installer.install_dependency_from_hash(
                hash=hash, 
                skip_tracking_installs=skip_tracking_installs, 
                offline_install=True
            )


def create_offline_packages(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str],
    wrapper_name: str
):
    new_dependency_configs = list(dependency_configs)
    
    for project_config in project_configs:
        new_dependency_configs.append(configs.from_project_config_get_dependency_configs(project_config))
    
    for game_config in game_configs:
        new_dependency_configs.append(configs.from_game_config_get_dependency_configs(game_config))

    flat_dependency_configs = [path for sublist in new_dependency_configs for path in sublist]

    for dependency_config in flat_dependency_configs:
        command = configs.from_dependency_config_get_command(dependency_config)
        sha_256_hash = configs.from_dependency_config_get_sha_256_hash(dependency_config)
        executable = command.executable
        download_links = configs.from_dependency_config_get_download_links(dependency_config)
        print(len(download_links))
        download_success = file_io.attempt_hash_verified_download_from_download_links(
            executable=executable,
            sha_256_hash=sha_256_hash,
            download_links=download_links,
            output_directory=f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/assets/dependencies'
        )
        if not download_success:
            error_message = f'The following dependency failed to download: "{executable}".'
            raise FileNotFoundError(error_message)
    copy_configs_over(
        project_configs, 
        game_configs, 
        new_dependency_configs
    )
    copy_tackle_over()
    offline_wrapper_path = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/{wrapper_name}_offline_installer')
    wrappers.create_offline_wrapper(new_dependency_configs, offline_wrapper_path)
    create_offline_toml(os.path.normpath(f'{os.path.dirname(offline_wrapper_path)}/offline.toml'), wrapper_name)
    create_offline_zip(wrapper_name)
    output_directory = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist')
    wrappers.create_download_install_wrapper(output_directory=output_directory, wrapper_name=wrapper_name)


def create_offline_toml(output_location: str, wrapper_name: str):
    doc = document()
    doc.add("wrapper_name", wrapper_name)

    with open(output_location, "w") as f:
        f.write(doc.as_string())


def create_offline_zip(wrapper_name: str):
    offline_directory = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer')
    output_zip = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/{wrapper_name}.zip')
    
    file_io.zip_directory(offline_directory, output_zip)

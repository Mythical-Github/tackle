import os
import zipfile
import tempfile
import subprocess
from tackle import log
from tomlkit import parse


def create_offline_packages(
    project_configs: list[str],
    game_configs: list[str],
    dependency_configs: list[str]
):
    log.logger.log_message('test')


def install_offline_packages(
    offline_install_packages: list[str],
    skip_tracking_installs: bool
):
    for offline_install_package in offline_install_packages:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(offline_install_package, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            toml_path = os.path.join(temp_dir, 'offline_installer.toml')
            
            if os.path.exists(toml_path):
                try:
                    with open(toml_path, 'r', encoding='utf-8') as toml_file:
                        toml_data = parse(toml_file.read())
                    
                    wrapper_name = toml_data.get('config_structure', {}).get('wrapper_name', 'wrapper')
                    
                    if wrapper_name:
                        wrapper_path = os.path.join(temp_dir, f'{wrapper_name}.bat')
                        
                        if os.path.exists(wrapper_path):
                            subprocess.run([wrapper_path], check=True)
                        else:
                            log.logger.log_message(f"Wrapper script {wrapper_name} not found in {temp_dir}")
                except Exception as e:
                    log.logger.log_message(f"Error processing {offline_install_package}: {e}")
            else:
                log.logger.log_message(f"offline_installer.toml not found in {offline_install_package}")
    
    log.logger.log_message("Installation process completed.")


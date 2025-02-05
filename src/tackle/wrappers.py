import os
import sys
from tackle import file_io, settings


def get_wrapper_location(wrapper_name: str) -> str:
    return os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/{wrapper_name}.bat')


def generate_wrapper(wrapper_name: str):
    args = sys.argv[:]

    if "--wrapper_name" in args:
        index = args.index("--wrapper_name")
        args.pop(index)
        args.pop(index)

    content = ' '.join(args)

    wrapper_path = get_wrapper_location(wrapper_name)

    os.makedirs(os.path.dirname(wrapper_path), exist_ok=True)

    with open(wrapper_path, 'w') as f:
        f.write(content)


def create_offline_wrapper(dependency_configs: list[list[str]], wrapper_path: str):
    dependencies_config_section = ""
    
    for dependency_group in dependency_configs:
        for dependency in dependency_group:
            absolute_dependency_path = os.path.join(file_io.SCRIPT_DIR, dependency)
            dependency_config_relative_path = os.path.relpath(absolute_dependency_path, start=file_io.SCRIPT_DIR)
            new_chunk = f'--dependencies_configs "%CD%\\{dependency_config_relative_path}"'
            dependencies_config_section += f' {new_chunk}'
    
    command = f""" 
@echo off
set "current_dir=%~dp0"
cd /d "%current_dir%"
"%CD%\\tackle.exe" install_dependencies --offline_install True {dependencies_config_section}
exit /b
"""
    
    with open(f"{wrapper_path}.bat", "w") as f:
        f.write(command + "\n")


def create_download_install_wrapper(output_directory: str, wrapper_name: str):
    bat_file_path = os.path.join(output_directory, f"{wrapper_name}_online_install.bat")
    download_link = 'www.replace_this_download_link.com'

    bat_content = fr"""
@echo off
set OUTPUT_DIR=%~dp0
cd /d "%OUTPUT_DIR%"
set WRAPPER_NAME={wrapper_name}_offline_installer
set DOWNLOAD_LINK={download_link}
set ZIP_PATH="%OUTPUT_DIR%\downloaded_file.zip"
set UNZIPPED_FILES_DIR="%OUTPUT_DIR%\%WRAPPER_NAME%"

:: Download the file
echo Downloading file...
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_LINK%' -OutFile '%ZIP_PATH%'"
if %ERRORLEVEL% neq 0 (
    echo Download failed!
    pause
    exit /b
)

:: Unzip the file
echo Unzipping file...
powershell -Command "Expand-Archive -Path '%ZIP_PATH%' -DestinationPath '%OUTPUT_DIR%'"
if %ERRORLEVEL% neq 0 (
    echo Unzipping failed!
    pause
    exit /b
)

:: Delete the zip file
echo Deleting zip file...
del "%ZIP_PATH%"

"%CD%\\%WRAPPER_NAME%.bat"

pause
"""

    with open(bat_file_path, 'w') as bat_file:
        bat_file.write(bat_content)

    print(f"Batch file created at {bat_file_path}")

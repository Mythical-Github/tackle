import os

from tackle import file_io


def get_tackle_executable_path() -> str:
    if os.name == "nt":
        executable = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/tackle.exe')
    else:
        executable = os.path.normpath(f'{file_io.SCRIPT_DIR}/dist/temp/offline_installer/tackle')
    return executable


def get_tackle_wrapper_extension_with_period() -> str:
    if os.name == "nt":
        wrapper_extension = ".bat"
    else:
        wrapper_extension = ".sh"
    return wrapper_extension

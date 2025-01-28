import os
import sys
from tackle import file_io


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

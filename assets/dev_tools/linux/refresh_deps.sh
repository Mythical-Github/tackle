#!/bin/bash

cd "$(dirname "$0")"

py_project_dev_tools_exe="$(cd .. && pwd)/py_project_dev_tools"

toml="$(cd ../../../ && pwd)/pyproject.toml"

"$py_project_dev_tools_exe" refresh_deps --project_toml_path "$toml"

exit 0

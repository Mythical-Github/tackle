

def install_dependencies(
    project_configs: list[str],
    game_configs: list[str],
    dependencies_configs: list[str],
    offline_install_packages: list[str],
    create_offline_packages: list[str],
    generate_wrappers: bool,
    reinstall_dependencies: bool
):
    print(str(reinstall_dependencies))

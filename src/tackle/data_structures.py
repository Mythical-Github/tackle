from enum import Enum
from platform import platform
from dataclasses import dataclass


class ExecutionMethod(Enum):
    HALTING = 'halting' # akin to subprocess run
    NON_HALTING = 'non_halting' # akin to subprocess Popen
    NON_HALTING_WAIT = 'non_halting_wait' # akin to subprocess Popen with a wait after


@dataclass
class Command:
    executable: str
    executable_args: list[str]
    execution_method: ExecutionMethod


@dataclass
class StoreFrontGameInformation:
    store_display_name: str
    game_purchase_url: str


@dataclass
class Game:
    game_display_name: str
    list[StoreFrontGameInformation]


@dataclass
class DownloadInformation:
    file_display_name: str
    download_urls: list[str]
    os: platform


@dataclass
class Project:
    display_name: str
    home_page: str
    git_repo_urls: list[str]
    community_urls: list[str]
    documentation_urls: list[str]
    downloads_information: list[DownloadInformation]


@dataclass
class DependencyConfigStructure:
    config_spec_version: float
    config_version: float
    display_name: str
    command: Command
    sha_256_hash: str
    download_links: list[str]
    compatible_projects: list[Project]
    compatible_games: list[Game]
    pre_hook_commands: list[Command]
    post_hook_commands: list[Command]


@dataclass
class GameConfigStructure:
    config_spec_version: float
    config_version: float
    game_info: Game


@dataclass
class ProjectConfigStructure:
    config_spec_version: float
    config_version: float
    project_info: Project

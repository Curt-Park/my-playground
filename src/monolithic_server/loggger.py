import os
from importlib import resources
from logging import Logger, config, getLogger


def set_logger_from_config(config_dir_path: str, config_filename: str, log_dir: str, log_filename: str) -> None:
    """Config logger."""
    config_dir_list: list[str] = list(filter(None, config_dir_path.split(os.sep)))
    config_path_with_period: str = ".".join(config_dir_list)

    config_file = resources.files(config_path_with_period).joinpath(config_filename)

    if not config_file.is_file():
        raise FileNotFoundError(f"{config_filename} is not found in {config_dir_path}.")

    os.makedirs(log_dir, exist_ok=True)

    with resources.as_file(config_file) as log_conf:
        config.fileConfig(log_conf, defaults={"log_path": os.path.join(log_dir, log_filename)})

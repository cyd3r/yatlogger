import json
import os
from pathlib import Path

def get_config(current_dir: Path = None, return_path=False):
    if current_dir is None:
        current_dir = Path(os.getcwd())

    config_path = current_dir / ".yatlogger.json"
    if config_path.exists():
        with config_path.open() as config_file:
            config = json.load(config_file)
            if "token" not in config:
                raise KeyError("Key 'token' is missing in config file")

            config["users"] = config.get("users", [])

            if return_path:
                return config, config_path
            return config

    if current_dir.parent == current_dir:
        raise FileNotFoundError("Could not find config")

    return get_config(current_dir.parent, return_path)

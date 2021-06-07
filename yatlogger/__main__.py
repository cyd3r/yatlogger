from pathlib import Path
from argparse import ArgumentParser
from .register import run_register_service

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config")
    args = parser.parse_args()

    config_search_dir = None if args.config is None else Path(args.config)

    run_register_service(config_search_dir)

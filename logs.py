import os
import json
import logging.config


def configure_logging(
        default_path="./config/logging_configuration.json",
        default_level=logging.INFO,
        env_key="LOG_CFG"
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as config_file:
            config = json.load(config_file)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
import yaml
from pathlib import Path

config_file = Path(__file__).parent.parent / "config.yaml"

def load_config():
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)
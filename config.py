import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

_DEFAULTS = {
    "difficulty": "medium",
    "wrap": False,
    "snake_char": "#",
    "food_char": "*",
    "player_name": "",
}

def load_config():
    config = dict(_DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            user_cfg = json.loads(CONFIG_FILE.read_text())
            config.update(user_cfg)
        except (json.JSONDecodeError, IOError):
            pass
    return config

def save_config(config):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

import json
from typing import Dict

def load_config(config_file: str = "config.json") -> Dict:
    """Load and validate configuration from a JSON file."""
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Validate required fields
        required_fields = ["currency", "impact", "save_format", "output_file"]
        for field in required_fields:
            if field not in config:
                print(f"Missing required config field: {field}")
                return {}

        # Validate save_format
        if config["save_format"] not in ["json", "txt"]:
            print(f"Invalid save_format: {config['save_format']}. Must be 'json' or 'txt'.")
            return {}

        return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        return {}
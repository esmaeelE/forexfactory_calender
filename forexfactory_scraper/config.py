import json

def load_config(config_file: str = "config.json") -> dict:
    """Load and validate configuration from a JSON file."""
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        if config.get("save_format") and config["save_format"] not in ("json", "txt"):
            print(f"Invalid save_format: {config['save_format']}. Must be 'json' or 'txt'.")
            return {}

        return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        return {}
import json


def load_config(config_file: str = "config.json") -> dict:
    """Load and validate configuration from a JSON file."""
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        valid_formats = ("json", "txt", "md")
        fmt = config.get("save_format")
        if fmt and fmt not in valid_formats:
            print(f"Invalid save_format: {fmt}. Must be one of {valid_formats}.")
            return {}

        return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        return {}
import json
import os

def load_config(config_path):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Config file not found at {config_path}")
        return {"urls": []}
    except json.JSONDecodeError:
        print(f"Invalid JSON in config file at {config_path}")
        return {"urls": []}

def save_config(config, config_path):
    """Save configuration to JSON file"""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
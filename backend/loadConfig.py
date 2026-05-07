import json
import os
import platform

def get_config_path():
    system = platform.system()
    if system == "Windows":
        appdata = os.getenv("APPDATA")
        return os.path.join(appdata, "com.csrub.warframe", "config.json")
    elif system == "Darwin":  # macOS
        home = os.path.expanduser("~")
        return os.path.join(home, "Library", "Application Support", "com.csrub.warframe", "config.json")
    else:  # Linux
        home = os.path.expanduser("~")
        return os.path.join(home, ".config", "com.csrub.warframe", "config.json")

# Ensure config directory exists
config_path = get_config_path()
os.makedirs(os.path.dirname(config_path), exist_ok=True)

# Create default config if missing
if not os.path.exists(config_path):
    print(f"Config not found at {config_path}, creating default config...", flush=True)
    default_config = {
        "time": 1.0,
        "warframe_link": "",
        "min_plat_price": 0,
        "is_setup_complete": False
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=4)

# Load the config
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

def get_config_val(key):
    return config.get(key)

# Debug prints
print("Time:", get_config_val("time"), flush=True)
print("Warframe Link:", get_config_val("warframe_link"), flush=True)
print("Min Plat Price:", get_config_val("min_plat_price"), flush=True)
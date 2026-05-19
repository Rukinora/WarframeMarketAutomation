import json
import os
import platform

# Returns the config.json file path depending on the operating system.
def get_config_path():
    # Detect current operating system
    system = platform.system() 
    
    # Windows config path
    if system == "Windows":
        # Gets AppData/Roaming directory
        appdata = os.getenv("APPDATA")
        # Returns For Example:
        # C:\Users\YourName\AppData\Roaming\WarframeMarket\config.json
        return os.path.join(
            appdata,
            "WarframeMarket",
            "config.json"
        )
        
    # macOS config path (Untested)
    elif system == "Darwin":
        # Gets current user home directory
        home = os.path.expanduser("~")
        # Returns:
        # ~/Library/Application Support/WarframeMarket/config.json
        return os.path.join(
            home,
            "Library",
            "Application Support",
            "WarframeMarket",
            "config.json"
        )
    # Linux config path (Untested)
    else:
        # Gets current user home directory
        home = os.path.expanduser("~")

        # Returns:
        # ~/.config/WarframeMarket/config.json
        return os.path.join(
            home,
            ".config",
            "WarframeMarket",
            "config.json"
        )



# Stores full config path globally
config_path = get_config_path()

# Debug -> prints exact config location
print("PYTHON CONFIG PATH:", config_path, flush=True)

# Creates the config folder automatically if missing.
# Example:
# C:\Users\User\AppData\Roaming\WarframeMarket
os.makedirs(
    os.path.dirname(config_path),
    exist_ok=True
)



# First-time setup:
# Creates config.json automatically if it doesn't exist yet.
if not os.path.exists(config_path):

    # Debug -> config file missing
    print(
        f"Config not found at {config_path}, "
        f"creating default config...",
        flush=True
    )
    # Default values used for first app launch
    default_config = {
        # Selenium wait delay timing
        "time": 1.0,
        # Default profile URL
        "warframe_link": "https://warframe.market/",
        # Minimum platinum sell price
        "min_plat_price": 20,
        # Tracks if user completed first-time setup
        "is_setup_complete": False
    }
    # Creates config.json file
    with open(config_path, "w", encoding="utf-8") as f:

        # Writes JSON nicely formatted
        json.dump(
            default_config,
            f,
            indent=4
        )



# Loads config.json fresh every time function is called.
# Prevents stale cached values.
def load_config():
    # Debug -> loading config file
    print(
        f"LOADING CONFIG FROM: {config_path}",
        flush=True
    )
    # Opens config.json read-only
    with open(config_path, "r", encoding="utf-8") as f:
        # Returns JSON as Python dictionary
        return json.load(f)



# Returns a specific config value by key name.
# Example:
# get_config_val("time")
# get_config_val("warframe_link")
def get_config_val(key):
    # Loads latest config values
    config = load_config()
    # Returns matching value
    return config.get(key)



# Debug -> prints all currently loaded config values
print("Time:", get_config_val("time"), flush=True)
print("Warframe Link:", get_config_val("warframe_link"), flush=True)
print("Min Plat Price:", get_config_val("min_plat_price"),flush=True)
print("Setup Complete:", get_config_val("is_setup_complete"), flush=True)
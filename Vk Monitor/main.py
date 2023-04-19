import json

config_file_path = "config.json"

def load_config(self, config_file_path):
    with open(config_file_path, "r") as f:
        config = json.load(f)
    self.users = config.get("users", [])
    self.time_span = config.get("time_span", 0)
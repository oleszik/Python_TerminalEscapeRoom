import json
import os

def load_room(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

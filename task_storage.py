import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    # load from json file if it exists
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(list(tasks), f)

    
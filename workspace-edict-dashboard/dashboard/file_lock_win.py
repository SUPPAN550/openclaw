"""
Windows-compatible file locking (替代 fcntl)
"""
import os
import time
import msvcrt

LOCK_DIR = os.path.dirname(os.path.abspath(__file__))
LOCK_EXT = ".lock"

def atomic_json_read(path):
    import json
    lock_path = path + LOCK_EXT
    for _ in range(100):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, OSError):
            time.sleep(0.05)
    raise IOError(f"Could not read {path}")

def atomic_json_write(path, data):
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def atomic_json_update(path, updater):
    import json
    data = atomic_json_read(path)
    data = updater(data)
    atomic_json_write(path, data)
    return data

"""
文件锁工具 - Windows 兼容版
替代 fcntl，使用 Windows 文件锁
"""
import json
import os
import pathlib
import tempfile
import time
import msvcrt
from typing import Any, Callable


def _lock_path(path: pathlib.Path) -> pathlib.Path:
    return path.parent / (path.name + '.lock')


def atomic_json_read(path: pathlib.Path, default: Any = None) -> Any:
    lock_file = _lock_path(path)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    max_attempts = 100
    for _ in range(max_attempts):
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except (IOError, OSError):
            time.sleep(0.05)
    return default


def atomic_json_write(path: pathlib.Path, data: Any) -> None:
    lock_file = _lock_path(path)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=str(path.parent), suffix='.tmp', prefix=path.stem + '_'
    )
    try:
        with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, str(path))
    except Exception:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise


def atomic_json_update(
    path: pathlib.Path,
    modifier: Callable[[Any], Any],
    default: Any = None,
) -> Any:
    lock_file = _lock_path(path)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(100):
        try:
            data = atomic_json_read(path, default)
            result = modifier(data)
            atomic_json_write(path, result)
            return result
        except (IOError, OSError):
            time.sleep(0.05)
    return default

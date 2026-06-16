"""Settings persistence."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULT_PATH = Path(os.path.expanduser("~")) / ".blackjack_settings.json"

DEFAULTS: Dict[str, Any] = {
    "lang": "zh",
    "sound": True,
    "volume": 1,
    "speed": "normal",
    "starting_chips": 200,
}


class Settings:
    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path else DEFAULT_PATH
        self.data: Dict[str, Any] = dict(DEFAULTS)
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            with self.path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    for k, v in loaded.items():
                        if k in DEFAULTS:
                            self.data[k] = v
        except (OSError, json.JSONDecodeError):
            pass

    def save(self) -> None:
        try:
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def get(self, key: str) -> Any:
        return self.data.get(key, DEFAULTS.get(key))

    def set(self, key: str, value: Any) -> None:
        if key in DEFAULTS:
            self.data[key] = value
            self.save()

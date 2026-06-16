"""Persistent score history (JSON in user home)."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

DEFAULT_PATH = Path(os.path.expanduser("~")) / ".blackjack_scores.json"


class ScoreBoard:
    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path else DEFAULT_PATH
        self._records: List[Dict] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self._records = []
            return
        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self._records = [r for r in data if isinstance(r, dict)]
                else:
                    self._records = []
        except (OSError, json.JSONDecodeError):
            self._records = []

    def save(self) -> None:
        try:
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(self._records, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def add(self, name: str, chips: int, rounds: int) -> Dict:
        record = {
            "name": name or "Player",
            "chips": int(chips),
            "rounds": int(rounds),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self._records.append(record)
        self.save()
        return record

    def top(self, n: int = 10) -> List[Dict]:
        return sorted(self._records, key=lambda r: (-r["chips"], -r["rounds"]))[:n]

    @property
    def all(self) -> List[Dict]:
        return list(self._records)

    @property
    def best(self) -> int:
        return max((r["chips"] for r in self._records), default=0)

"""Simple cross-platform sound via terminal bell.

The terminal bell is a portable signal that requires no audio dependencies.
Volume is emulated by the number of bells per event (1..3).
"""
from __future__ import annotations

import sys
import time


SPEED_DELAY = {
    "slow": 0.6,
    "normal": 0.25,
    "fast": 0.08,
    "instant": 0.0,
}


class Sound:
    def __init__(self, enabled: bool = True, volume: int = 1, output=None) -> None:
        self.enabled = enabled
        self.volume = max(0, min(3, volume))
        self._out = output if output is not None else sys.stdout

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled

    def set_volume(self, vol: int) -> None:
        self.volume = max(0, min(3, vol))

    def _emit(self, count: int) -> None:
        if not self.enabled or self.volume == 0:
            return
        n = count * self.volume
        try:
            self._out.write("\a" * n)
            self._out.flush()
        except Exception:
            pass

    def deal(self) -> None:
        self._emit(1)

    def win(self) -> None:
        self._emit(2)

    def lose(self) -> None:
        self._emit(1)

    def blackjack(self) -> None:
        self._emit(3)

    def click(self) -> None:
        self._emit(1)


def speed_delay(name: str) -> float:
    return SPEED_DELAY.get(name, SPEED_DELAY["normal"])


def pause(speed_name: str) -> None:
    d = speed_delay(speed_name)
    if d > 0:
        time.sleep(d)

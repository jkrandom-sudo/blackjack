"""Card and Deck for Blackjack."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    @property
    def value(self) -> int:
        if self.rank in ("J", "Q", "K"):
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

    @property
    def is_ace(self) -> bool:
        return self.rank == "A"


class Deck:
    """Multi-deck shoe with auto-reshuffle."""

    def __init__(self, num_decks: int = 4, rng: random.Random | None = None) -> None:
        if num_decks < 1:
            raise ValueError("num_decks must be >= 1")
        self.num_decks = num_decks
        self._rng = rng or random.Random()
        self._cards: List[Card] = []
        self.reshuffle()

    def reshuffle(self) -> None:
        self._cards = [Card(r, s) for _ in range(self.num_decks) for s in SUITS for r in RANKS]
        self._rng.shuffle(self._cards)

    def __len__(self) -> int:
        return len(self._cards)

    def deal(self) -> Card:
        if len(self._cards) < 15:
            self.reshuffle()
        return self._cards.pop()

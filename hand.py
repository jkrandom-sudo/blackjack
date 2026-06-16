"""Hand value computation for Blackjack."""
from __future__ import annotations

from typing import List

from deck import Card


class Hand:
    def __init__(self, cards: List[Card] | None = None) -> None:
        self.cards: List[Card] = list(cards) if cards else []

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def clear(self) -> None:
        self.cards = []

    @property
    def value(self) -> int:
        """Best hand value (Aces counted as 11 when possible without busting)."""
        total = sum(c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.is_ace)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    @property
    def is_soft(self) -> bool:
        """True if at least one Ace is currently counted as 11."""
        aces = sum(1 for c in self.cards if c.is_ace)
        if aces == 0:
            return False
        low = sum(1 if c.is_ace else c.value for c in self.cards)
        return low + 10 <= 21

    @property
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value == 21

    @property
    def is_bust(self) -> bool:
        return self.value > 21

    def render(self, hide_first: bool = False) -> str:
        if not self.cards:
            return ""
        if hide_first and len(self.cards) >= 1:
            shown = ["[??]"] + [f"[{c}]" for c in self.cards[1:]]
        else:
            shown = [f"[{c}]" for c in self.cards]
        return " ".join(shown)

    def __len__(self) -> int:
        return len(self.cards)

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from deck import Card, Deck, RANKS, SUITS  # noqa: E402


class TestCard(unittest.TestCase):
    def test_face_values(self):
        for rank in ("J", "Q", "K"):
            self.assertEqual(Card(rank, "♠").value, 10)

    def test_number_values(self):
        for n in range(2, 11):
            self.assertEqual(Card(str(n), "♥").value, n)

    def test_ace_default_eleven(self):
        self.assertEqual(Card("A", "♣").value, 11)
        self.assertTrue(Card("A", "♦").is_ace)
        self.assertFalse(Card("K", "♦").is_ace)

    def test_str(self):
        self.assertEqual(str(Card("A", "♠")), "A♠")


class TestDeck(unittest.TestCase):
    def test_size(self):
        d = Deck(num_decks=1)
        self.assertEqual(len(d), 52)
        d4 = Deck(num_decks=4)
        self.assertEqual(len(d4), 208)

    def test_deal_reduces(self):
        d = Deck(num_decks=1)
        before = len(d)
        d.deal()
        self.assertEqual(len(d), before - 1)

    def test_invalid_decks(self):
        with self.assertRaises(ValueError):
            Deck(num_decks=0)

    def test_unique_cards(self):
        d = Deck(num_decks=1)
        # Deck auto-reshuffles below 15 cards, so verify uniqueness
        # within a single fresh shoe by inspecting internal cards.
        seen = set((c.rank, c.suit) for c in d._cards)
        self.assertEqual(len(seen), 52)

    def test_reshuffle_when_low(self):
        d = Deck(num_decks=1, rng=random.Random(0))
        # Force the internal pile below the reshuffle threshold.
        d._cards = d._cards[:5]
        self.assertEqual(len(d), 5)
        # Next deal triggers reshuffle and refills with a full shoe (52 - 1 dealt).
        d.deal()
        self.assertEqual(len(d), 51)

    def test_deterministic_shuffle(self):
        d1 = Deck(num_decks=1, rng=random.Random(42))
        d2 = Deck(num_decks=1, rng=random.Random(42))
        seq1 = [str(d1.deal()) for _ in range(10)]
        seq2 = [str(d2.deal()) for _ in range(10)]
        self.assertEqual(seq1, seq2)

    def test_ranks_suits_constants(self):
        self.assertEqual(len(RANKS), 13)
        self.assertEqual(len(SUITS), 4)


if __name__ == "__main__":
    unittest.main()

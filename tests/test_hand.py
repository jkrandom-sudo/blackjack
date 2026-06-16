import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from deck import Card  # noqa: E402
from hand import Hand  # noqa: E402


class TestHand(unittest.TestCase):
    def test_empty(self):
        h = Hand()
        self.assertEqual(h.value, 0)
        self.assertFalse(h.is_blackjack)
        self.assertFalse(h.is_bust)
        self.assertFalse(h.is_soft)

    def test_basic_value(self):
        h = Hand([Card("5", "♠"), Card("7", "♥")])
        self.assertEqual(h.value, 12)

    def test_blackjack(self):
        h = Hand([Card("A", "♠"), Card("K", "♥")])
        self.assertTrue(h.is_blackjack)
        self.assertEqual(h.value, 21)

    def test_not_blackjack_with_three_cards(self):
        h = Hand([Card("7", "♠"), Card("7", "♥"), Card("7", "♣")])
        self.assertEqual(h.value, 21)
        self.assertFalse(h.is_blackjack)

    def test_ace_demotion(self):
        h = Hand([Card("A", "♠"), Card("9", "♥"), Card("5", "♣")])
        self.assertEqual(h.value, 15)  # A=1
        self.assertFalse(h.is_soft)

    def test_soft_seventeen(self):
        h = Hand([Card("A", "♠"), Card("6", "♥")])
        self.assertEqual(h.value, 17)
        self.assertTrue(h.is_soft)

    def test_two_aces(self):
        h = Hand([Card("A", "♠"), Card("A", "♥")])
        self.assertEqual(h.value, 12)
        self.assertTrue(h.is_soft)

    def test_two_aces_with_face(self):
        h = Hand([Card("A", "♠"), Card("A", "♥"), Card("9", "♣")])
        self.assertEqual(h.value, 21)

    def test_bust(self):
        h = Hand([Card("K", "♠"), Card("Q", "♥"), Card("5", "♣")])
        self.assertTrue(h.is_bust)
        self.assertEqual(h.value, 25)

    def test_render_hidden(self):
        h = Hand([Card("A", "♠"), Card("K", "♥")])
        rendered = h.render(hide_first=True)
        self.assertIn("[??]", rendered)
        self.assertIn("K", rendered)
        self.assertNotIn("A♠", rendered)

    def test_render_visible(self):
        h = Hand([Card("A", "♠"), Card("K", "♥")])
        rendered = h.render(hide_first=False)
        self.assertIn("A", rendered)
        self.assertIn("K", rendered)

    def test_clear(self):
        h = Hand([Card("A", "♠")])
        h.clear()
        self.assertEqual(len(h), 0)


if __name__ == "__main__":
    unittest.main()

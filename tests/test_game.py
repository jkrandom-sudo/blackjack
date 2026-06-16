"""Game flow integration tests using stubbed input/output and a fixed deck."""
import io
import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from deck import Card, Deck  # noqa: E402
from game import BlackjackGame  # noqa: E402
from i18n import I18N  # noqa: E402
from score import ScoreBoard  # noqa: E402
from settings import Settings  # noqa: E402
from sound import Sound  # noqa: E402


class StackedDeck(Deck):
    """Deck where deal() returns cards from a fixed list (last item dealt first)."""

    def __init__(self, cards):
        # Avoid parent shuffle behavior
        self._cards = list(cards)
        self.num_decks = 1

    def reshuffle(self):
        # No-op for tests — extend with a fresh standard deck if drained
        if not self._cards:
            self._cards = [Card(r, "♠") for r in ("2", "3", "4", "5", "6", "7", "8", "9", "10")]


def make_game(input_seq, deck_cards, *, speed="instant"):
    inputs = iter(input_seq)
    out = io.StringIO()

    def fake_input(prompt=""):
        try:
            return next(inputs)
        except StopIteration:
            raise EOFError()

    s_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    s_tmp.close()
    Path(s_tmp.name).unlink()
    sb_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    sb_tmp.close()
    Path(sb_tmp.name).unlink()

    settings = Settings(s_tmp.name)
    settings.set("speed", speed)
    settings.set("starting_chips", 100)
    sb = ScoreBoard(sb_tmp.name)
    sound = Sound(enabled=False, output=io.StringIO())
    g = BlackjackGame(
        settings=settings,
        scoreboard=sb,
        i18n=I18N("en"),
        sound=sound,
        input_func=fake_input,
        output=out,
    )
    g.deck = StackedDeck(deck_cards)
    return g, out


def cards_in_deal_order(seq):
    """Cards listed in deal order — convert to deck push order (last dealt = top)."""
    return list(reversed(seq))


class TestPlayRound(unittest.TestCase):
    def test_player_blackjack_pays_3_to_2(self):
        # Deal order: P1, D1, P2, D2 → player gets A, K (BJ), dealer gets 9,7
        deal = [Card("A", "♠"), Card("9", "♥"), Card("K", "♣"), Card("7", "♦")]
        g, _ = make_game(input_seq=[], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "blackjack")
        self.assertEqual(g.chips, 100 + 15)  # 1.5x payout

    def test_dealer_blackjack(self):
        deal = [Card("9", "♠"), Card("A", "♥"), Card("8", "♣"), Card("K", "♦")]
        g, _ = make_game(input_seq=[], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "dealer_blackjack")
        self.assertEqual(g.chips, 90)

    def test_push_on_double_blackjack(self):
        deal = [Card("A", "♠"), Card("A", "♥"), Card("K", "♣"), Card("K", "♦")]
        g, _ = make_game(input_seq=[], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "push")
        self.assertEqual(g.chips, 100)

    def test_player_stands_and_wins(self):
        # Player: 10, K (=20). Dealer: 9, 8 (=17, stands). Player wins.
        deal = [Card("10", "♠"), Card("9", "♥"), Card("K", "♣"), Card("8", "♦")]
        g, _ = make_game(input_seq=["s"], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "win")
        self.assertEqual(g.chips, 110)

    def test_player_busts(self):
        # Player: 10, K, then hits → 10 → bust
        deal = [Card("10", "♠"), Card("9", "♥"), Card("K", "♣"), Card("8", "♦"), Card("10", "♥")]
        g, _ = make_game(input_seq=["h"], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "bust")
        self.assertEqual(g.chips, 90)

    def test_dealer_busts(self):
        # Player: 10, 9 (=19). Dealer: 6, 9 (=15) hits → 10 → bust 25
        deal = [
            Card("10", "♠"), Card("6", "♥"),
            Card("9", "♣"), Card("9", "♦"),
            Card("10", "♥"),
        ]
        g, _ = make_game(input_seq=["s"], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "win")
        self.assertEqual(g.chips, 110)

    def test_player_loses(self):
        # Player: 10, 7 (=17). Dealer: 10, 9 (=19). Player stands → loses.
        deal = [Card("10", "♠"), Card("10", "♥"), Card("7", "♣"), Card("9", "♦")]
        g, _ = make_game(input_seq=["s"], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "lose")
        self.assertEqual(g.chips, 90)

    def test_double_down_win(self):
        # Player: 5, 6 (=11). Double → 10 (=21). Dealer: 10, 8 (=18). Player wins doubled.
        deal = [Card("5", "♠"), Card("10", "♥"), Card("6", "♣"), Card("8", "♦"), Card("10", "♣")]
        g, _ = make_game(input_seq=["d"], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "win")
        self.assertEqual(g.chips, 100 + 20)

    def test_invalid_then_stand(self):
        deal = [Card("10", "♠"), Card("9", "♥"), Card("K", "♣"), Card("8", "♦")]
        g, _ = make_game(input_seq=["x", "?", "s"], deck_cards=cards_in_deal_order(deal))
        result = g.play_round(bet=10)
        self.assertEqual(result, "win")


class TestAskBet(unittest.TestCase):
    def test_invalid_then_valid(self):
        g, _ = make_game(input_seq=["abc", "-5", "0", "999", "10"], deck_cards=[])
        bet = g.ask_bet()
        self.assertEqual(bet, 10)

    def test_quit(self):
        g, _ = make_game(input_seq=["q"], deck_cards=[])
        self.assertIsNone(g.ask_bet())


if __name__ == "__main__":
    unittest.main()

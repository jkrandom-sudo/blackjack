"""Blackjack — console game with i18n, sound, settings, scoreboard."""
from __future__ import annotations

import os
import sys
from typing import Optional

from deck import Deck
from hand import Hand
from i18n import I18N, STRINGS
from score import ScoreBoard
from settings import Settings
from sound import Sound, pause


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


class QuitGame(Exception):
    pass


class BlackjackGame:
    DEALER_STAND = 17

    def __init__(
        self,
        settings: Optional[Settings] = None,
        scoreboard: Optional[ScoreBoard] = None,
        i18n: Optional[I18N] = None,
        sound: Optional[Sound] = None,
        input_func=input,
        output=sys.stdout,
    ) -> None:
        self.settings = settings or Settings()
        self.scoreboard = scoreboard or ScoreBoard()
        self.i18n = i18n or I18N(self.settings.get("lang"))
        self.sound = sound or Sound(
            enabled=self.settings.get("sound"),
            volume=self.settings.get("volume"),
        )
        self._input = input_func
        self._out = output
        self.deck = Deck()
        self.player = Hand()
        self.dealer = Hand()
        self.chips = int(self.settings.get("starting_chips"))
        self.rounds = 0
        self.player_name = ""

    # ---------- IO helpers ----------
    def _print(self, msg: str = "") -> None:
        self._out.write(str(msg) + "\n")
        self._out.flush()

    def _ask(self, prompt: str) -> str:
        try:
            return self._input(prompt).strip()
        except EOFError:
            raise QuitGame()

    def t(self, key: str, **kw) -> str:
        return self.i18n.t(key, **kw)

    # ---------- Menus ----------
    def main_menu(self) -> None:
        while True:
            clear_screen()
            self._print("=" * 42)
            self._print(self.t("title").center(42))
            self._print("=" * 42)
            self._print(self.t("menu_new"))
            self._print(self.t("menu_settings"))
            self._print(self.t("menu_scores"))
            self._print(self.t("menu_help"))
            self._print(self.t("menu_quit"))
            self._print("")
            choice = self._ask(self.t("prompt_choice")).lower()
            if choice in ("n", "新", "1"):
                self.run_session()
            elif choice in ("s", "设置", "2"):
                self.settings_menu()
            elif choice in ("l", "排", "3"):
                self.show_scores()
            elif choice in ("h", "帮", "4", "?"):
                self.show_help()
            elif choice in ("q", "退", "5", "exit"):
                self._print(self.t("goodbye"))
                return
            else:
                self._print(self.t("unknown_input"))
                self._ask(self.t("press_enter"))

    def settings_menu(self) -> None:
        while True:
            clear_screen()
            self._print(self.t("settings_title"))
            self._print("-" * 30)
            self._print(self.t("set_lang", value=STRINGS[self.i18n.lang]["lang_name"]))
            self._print(self.t(
                "set_sound",
                value=self.t("on") if self.sound.enabled else self.t("off"),
            ))
            self._print(self.t("set_volume", value=str(self.sound.volume)))
            self._print(self.t("set_speed", value=self.t(f"speed_{self.settings.get('speed')}")))
            self._print(self.t("set_back"))
            choice = self._ask(self.t("prompt_choice")).lower()
            if choice == "1":
                new_lang = "en" if self.i18n.lang == "zh" else "zh"
                self.i18n.set(new_lang)
                self.settings.set("lang", new_lang)
            elif choice == "2":
                self.sound.set_enabled(not self.sound.enabled)
                self.settings.set("sound", self.sound.enabled)
            elif choice == "3":
                self.sound.set_volume((self.sound.volume + 1) % 4)
                self.settings.set("volume", self.sound.volume)
                self.sound.click()
            elif choice == "4":
                order = ["slow", "normal", "fast", "instant"]
                idx = order.index(self.settings.get("speed")) if self.settings.get("speed") in order else 1
                self.settings.set("speed", order[(idx + 1) % len(order)])
            elif choice in ("b", "返", "back", "0"):
                return

    def show_scores(self) -> None:
        clear_screen()
        self._print(self.t("scores_title"))
        self._print("-" * 60)
        top = self.scoreboard.top(10)
        if not top:
            self._print(self.t("scores_empty"))
        else:
            self._print(self.t("scores_header"))
            for i, r in enumerate(top, 1):
                name = (r.get("name") or "")[:16]
                self._print(f"{i:<6} {name:<18} {r['chips']:<8} {r['rounds']:<8} {r['date']}")
        self._print("")
        self._ask(self.t("press_enter"))

    def show_help(self) -> None:
        clear_screen()
        self._print(self.t("help_title"))
        self._print("-" * 42)
        self._print(self.t("help_body"))
        self._ask(self.t("press_enter"))

    # ---------- Session ----------
    def run_session(self) -> None:
        name = self._ask(self.t("enter_name")) or self.t("name_default")
        self.player_name = name
        self.chips = int(self.settings.get("starting_chips"))
        self.rounds = 0
        self._print(self.t("starting_chips", chips=self.chips))
        try:
            while self.chips > 0:
                self.rounds += 1
                self._print("")
                self._print(self.t("round_no", n=self.rounds))
                bet = self.ask_bet()
                if bet is None:
                    break
                self.play_round(bet)
                cont = self._ask(self.t("press_enter"))
                if cont.lower() in ("q", "quit", "退"):
                    break
            if self.chips <= 0:
                self._print(self.t("out_of_chips"))
        except QuitGame:
            pass

        # Save score
        ans = self._ask(self.t("save_score_q", yes_no=self.t("yes_no"))).lower()
        if ans in ("y", "yes", "是"):
            self.scoreboard.add(self.player_name, self.chips, self.rounds)
            self._print(self.t("score_saved"))
            self._ask(self.t("press_enter"))

    def ask_bet(self) -> Optional[int]:
        while True:
            raw = self._ask(self.t("bet_prompt") + f"[{self.t('chips_label')}: {self.chips}] ").lower()
            if raw in ("q", "quit"):
                return None
            if raw == "p":
                self.handle_pause()
                continue
            try:
                bet = int(raw)
            except ValueError:
                self._print(self.t("invalid_bet"))
                continue
            if bet <= 0:
                self._print(self.t("invalid_bet"))
                continue
            if bet > self.chips:
                self._print(self.t("not_enough_chips"))
                continue
            return bet

    def handle_pause(self) -> None:
        ans = self._ask(self.t("paused"))
        if ans.lower() in ("q", "quit", "退"):
            raise QuitGame()

    # ---------- Round ----------
    def play_round(self, bet: int) -> str:
        self.player = Hand()
        self.dealer = Hand()
        speed = self.settings.get("speed")

        # Initial deal
        for _ in range(2):
            self.player.add(self.deck.deal())
            self.sound.deal()
            pause(speed)
            self.dealer.add(self.deck.deal())
            self.sound.deal()
            pause(speed)

        self.render(hide_dealer=True)

        # Naturals
        if self.player.is_blackjack and self.dealer.is_blackjack:
            self.render(hide_dealer=False)
            self._print(self.t("push"))
            return "push"
        if self.player.is_blackjack:
            payout = int(bet * 1.5)
            self.chips += payout
            self.render(hide_dealer=False)
            self._print(self.t("blackjack"))
            self.sound.blackjack()
            self._print(self.t("round_summary", result=f"+{payout}", chips=self.chips))
            return "blackjack"
        if self.dealer.is_blackjack:
            self.chips -= bet
            self.render(hide_dealer=False)
            self._print(self.t("dealer_blackjack"))
            self.sound.lose()
            self._print(self.t("round_summary", result=f"-{bet}", chips=self.chips))
            return "dealer_blackjack"

        # Player turn
        doubled = False
        while True:
            action = self._ask(self.t("your_action")).lower()
            if action in ("h", "hit", "要"):
                self.player.add(self.deck.deal())
                self.sound.deal()
                pause(speed)
                self.render(hide_dealer=True)
                if self.player.is_bust:
                    self.chips -= bet
                    self._print(self.t("bust"))
                    self.sound.lose()
                    self._print(self.t("round_summary", result=f"-{bet}", chips=self.chips))
                    return "bust"
            elif action in ("s", "stand", "停"):
                break
            elif action in ("d", "double", "加"):
                if len(self.player) != 2:
                    self._print(self.t("double_not_allowed"))
                    continue
                if self.chips < bet * 2:
                    self._print(self.t("not_enough_chips"))
                    continue
                bet *= 2
                doubled = True
                self.player.add(self.deck.deal())
                self.sound.deal()
                pause(speed)
                self.render(hide_dealer=True)
                if self.player.is_bust:
                    self.chips -= bet
                    self._print(self.t("bust"))
                    self.sound.lose()
                    self._print(self.t("round_summary", result=f"-{bet}", chips=self.chips))
                    return "bust"
                break
            elif action in ("p", "pause", "暂"):
                self.handle_pause()
            elif action in ("q", "quit", "退"):
                raise QuitGame()
            else:
                self._print(self.t("unknown_input"))

        # Dealer turn
        self.render(hide_dealer=False)
        while self.dealer.value < self.DEALER_STAND:
            self.dealer.add(self.deck.deal())
            self.sound.deal()
            pause(speed)
            self.render(hide_dealer=False)

        # Resolve
        if self.dealer.is_bust:
            self.chips += bet
            self._print(self.t("dealer_bust"))
            self.sound.win()
            self._print(self.t("round_summary", result=f"+{bet}", chips=self.chips))
            return "win"
        if self.player.value > self.dealer.value:
            self.chips += bet
            self._print(self.t("win"))
            self.sound.win()
            self._print(self.t("round_summary", result=f"+{bet}", chips=self.chips))
            return "win"
        if self.player.value < self.dealer.value:
            self.chips -= bet
            self._print(self.t("lose"))
            self.sound.lose()
            self._print(self.t("round_summary", result=f"-{bet}", chips=self.chips))
            return "lose"
        self._print(self.t("push"))
        self._print(self.t("round_summary", result="0", chips=self.chips))
        return "push"

    def render(self, hide_dealer: bool) -> None:
        clear_screen()
        self._print("=" * 42)
        self._print(self.t("round_no", n=self.rounds) + f"   {self.t('chips_label')}: {self.chips}")
        self._print("=" * 42)
        self._print(f"{self.t('dealer'):<8}: {self.dealer.render(hide_first=hide_dealer)}")
        if not hide_dealer:
            self._print(f"{'':<8}  = {self.dealer.value}")
        self._print(f"{self.t('you'):<8}: {self.player.render()}")
        self._print(f"{'':<8}  = {self.player.value}{' (soft)' if self.player.is_soft else ''}")
        self._print("")


def main() -> None:
    game = BlackjackGame()
    try:
        game.main_menu()
    except (KeyboardInterrupt, QuitGame):
        print()
        print(game.t("goodbye"))


if __name__ == "__main__":
    main()

# Blackjack / 21 点

A console Blackjack game written in pure Python (stdlib only) with bilingual UI, persistent scores, configurable sound, and game-speed control.

一个用纯 Python 标准库编写的控制台 21 点游戏,支持中英文界面、分数持久化、可配置音效与游戏速度。

---

## Features / 功能

- **Multi-deck shoe**: 4 decks with auto-reshuffle when running low.
- **Standard rules**: hit / stand / double down, dealer stands on 17, Blackjack pays 3:2.
- **Bilingual UI** (中文 / English) — switch in Settings.
- **Sound effects** via terminal bell — toggle on/off, volume 0–3.
- **Game speed** — slow / normal / fast / instant deal animation.
- **Pause / resume** — `P` at any prompt.
- **Persistent settings & scores** — saved to `~/.blackjack_settings.json` and `~/.blackjack_scores.json`.
- **Top-10 leaderboard** by chips.
- **Comprehensive test suite** — 51 unit + integration tests.

## Requirements / 环境

- Python 3.9 or newer
- A terminal with UTF-8 support (recommended for card suit symbols)
- No third-party packages

## Quick Start / 快速开始

```bash
git clone https://github.com/<your-user>/blackjack.git
cd blackjack
python3 game.py
```

From the main menu:

| Key | Action / 操作 |
|-----|-----|
| `N` | New game / 开始新游戏 |
| `S` | Settings / 设置 |
| `L` | Leaderboard / 排行榜 |
| `H` | Help / 帮助 |
| `Q` | Quit / 退出 |

In-round controls:

| Key | Action |
|-----|-----|
| `H` | Hit (要牌) |
| `S` | Stand (停牌) |
| `D` | Double down (加倍 — only on first 2 cards, requires chips ≥ 2× bet) |
| `P` | Pause (暂停) |
| `Q` | Quit round (退出当前局) |

## Project Layout / 项目结构

```
blackjack/
├── game.py              # main game loop and menus
├── deck.py              # Card / Deck classes
├── hand.py              # Hand value computation (with Ace logic)
├── i18n.py              # Bilingual string table
├── sound.py             # Terminal-bell sound + speed delays
├── score.py             # Persistent leaderboard
├── settings.py          # Persistent user settings
├── tests/
│   ├── test_deck.py
│   ├── test_hand.py
│   ├── test_modules.py  # i18n / sound / score / settings
│   ├── test_game.py     # round-flow integration tests with stubbed deck
│   └── run_tests.py
├── README.md
└── .gitignore
```

## Running the Tests / 运行测试

```bash
python3 -m unittest discover tests/
# or
python3 tests/run_tests.py
```

Expected: `Ran 51 tests in <1s`, all passing.

## Settings File Locations

- Settings: `~/.blackjack_settings.json`
- Scores:   `~/.blackjack_scores.json`

Delete those files to reset.

## Game Rules / 游戏规则

- Aces count as 1 or 11 (whichever helps without busting).
- 2–10 score face value; J / Q / K = 10.
- The dealer hits on 16 or below and stands on 17 or above.
- A natural Blackjack (Ace + 10-value as the first two cards) pays **1.5×**.
- A push (tie) returns the bet.
- "Double down" doubles the bet, deals exactly one more card, and stands.

## License

MIT — see LICENSE file (or use freely).

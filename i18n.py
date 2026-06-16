"""Bilingual (Chinese/English) text resources."""
from __future__ import annotations

STRINGS = {
    "en": {
        "title": "BLACKJACK / 21",
        "menu_new": "[N] New game",
        "menu_settings": "[S] Settings",
        "menu_scores": "[L] Leaderboard",
        "menu_help": "[H] Help",
        "menu_quit": "[Q] Quit",
        "prompt_choice": "Choose: ",
        "enter_name": "Enter your name: ",
        "name_default": "Player",
        "chips_label": "Chips",
        "bet_prompt": "Place bet (or 'q' to quit, 'p' to pause): ",
        "invalid_bet": "Invalid bet. Try again.",
        "not_enough_chips": "Not enough chips.",
        "dealer": "Dealer",
        "you": "You",
        "your_action": "[H]it / [S]tand / [D]ouble / [P]ause / [Q]uit: ",
        "blackjack": "Blackjack!",
        "bust": "Bust!",
        "win": "You win!",
        "lose": "You lose.",
        "push": "Push (tie).",
        "dealer_blackjack": "Dealer has Blackjack.",
        "dealer_bust": "Dealer busts!",
        "round_summary": "Round result: {result} | Chips: {chips}",
        "press_enter": "Press Enter to continue...",
        "paused": "PAUSED. Press Enter to resume, Q+Enter to quit.",
        "settings_title": "Settings",
        "set_lang": "[1] Language: {value}",
        "set_sound": "[2] Sound: {value}",
        "set_volume": "[3] Volume: {value}",
        "set_speed": "[4] Speed: {value}",
        "set_back": "[B] Back",
        "on": "ON",
        "off": "OFF",
        "speed_slow": "slow",
        "speed_normal": "normal",
        "speed_fast": "fast",
        "speed_instant": "instant",
        "scores_title": "Leaderboard (Top 10 by chips)",
        "scores_empty": "(no records yet)",
        "scores_header": "Rank   Name              Chips    Rounds   Date",
        "score_saved": "Score saved.",
        "help_title": "Help",
        "help_body": (
            "Goal: get closer to 21 than the dealer without going over.\n"
            "A = 1 or 11. J/Q/K = 10. 2..10 = face value.\n"
            "Hit (H): take a card.\n"
            "Stand (S): stop drawing.\n"
            "Double (D): double bet, take exactly one card, then stand.\n"
            "Dealer hits to 16, stands on soft 17 or higher.\n"
            "Blackjack pays 3:2.\n"
            "Pause (P) any time. Sound and language can be changed in Settings.\n"
        ),
        "goodbye": "Thanks for playing!",
        "out_of_chips": "You're out of chips. Game over.",
        "starting_chips": "Starting chips: {chips}",
        "round_no": "Round {n}",
        "lang_name": "English",
        "yes_no": "(y/n)",
        "save_score_q": "Save score? (y/n): ",
        "unknown_input": "Unknown input.",
    },
    "zh": {
        "title": "21 点 / Blackjack",
        "menu_new": "[N] 开始新游戏",
        "menu_settings": "[S] 设置",
        "menu_scores": "[L] 排行榜",
        "menu_help": "[H] 帮助",
        "menu_quit": "[Q] 退出",
        "prompt_choice": "请选择: ",
        "enter_name": "请输入玩家名: ",
        "name_default": "玩家",
        "chips_label": "筹码",
        "bet_prompt": "请下注 (q 退出, p 暂停): ",
        "invalid_bet": "下注无效,请重新输入。",
        "not_enough_chips": "筹码不足。",
        "dealer": "庄家",
        "you": "你",
        "your_action": "[H]要牌 / [S]停牌 / [D]加倍 / [P]暂停 / [Q]退出: ",
        "blackjack": "Blackjack!天牌!",
        "bust": "爆牌!",
        "win": "你赢了!",
        "lose": "你输了。",
        "push": "平局。",
        "dealer_blackjack": "庄家是 Blackjack。",
        "dealer_bust": "庄家爆牌!",
        "round_summary": "本轮结果: {result} | 筹码: {chips}",
        "press_enter": "按回车继续...",
        "paused": "已暂停,回车继续,输入 Q 回车退出。",
        "settings_title": "设置",
        "set_lang": "[1] 语言: {value}",
        "set_sound": "[2] 音效: {value}",
        "set_volume": "[3] 音量: {value}",
        "set_speed": "[4] 速度: {value}",
        "set_back": "[B] 返回",
        "on": "开",
        "off": "关",
        "speed_slow": "慢速",
        "speed_normal": "正常",
        "speed_fast": "快速",
        "speed_instant": "即时",
        "scores_title": "排行榜 (按筹码 Top 10)",
        "scores_empty": "(暂无记录)",
        "scores_header": "名次   玩家              筹码     局数     日期",
        "score_saved": "成绩已保存。",
        "help_title": "帮助",
        "help_body": (
            "目标:在不超过 21 点的前提下比庄家更接近 21。\n"
            "A 可作 1 或 11;J/Q/K 计 10 点;2-10 按面值。\n"
            "要牌 (H): 再发一张。\n"
            "停牌 (S): 不再要牌。\n"
            "加倍 (D): 下注翻倍,只再发一张然后停牌。\n"
            "庄家在 16 点及以下必须要牌,17 及以上停牌。\n"
            "Blackjack 赔率 3:2。\n"
            "随时按 P 暂停。音效与语言可在设置中调整。\n"
        ),
        "goodbye": "感谢游玩!",
        "out_of_chips": "筹码用尽,游戏结束。",
        "starting_chips": "起始筹码: {chips}",
        "round_no": "第 {n} 局",
        "lang_name": "中文",
        "yes_no": "(y/n)",
        "save_score_q": "保存本次成绩?(y/n): ",
        "unknown_input": "无效输入。",
    },
}


class I18N:
    def __init__(self, lang: str = "zh") -> None:
        self.lang = lang if lang in STRINGS else "en"

    def set(self, lang: str) -> None:
        if lang in STRINGS:
            self.lang = lang

    def t(self, key: str, **kwargs) -> str:
        text = STRINGS[self.lang].get(key) or STRINGS["en"].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

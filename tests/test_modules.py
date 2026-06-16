import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from i18n import I18N, STRINGS  # noqa: E402
from score import ScoreBoard  # noqa: E402
from settings import Settings, DEFAULTS  # noqa: E402
from sound import Sound, SPEED_DELAY, speed_delay  # noqa: E402


class TestI18N(unittest.TestCase):
    def test_default_zh(self):
        i = I18N("zh")
        self.assertEqual(i.lang, "zh")
        self.assertIn("21", i.t("title"))

    def test_switch(self):
        i = I18N("zh")
        i.set("en")
        self.assertEqual(i.lang, "en")
        self.assertIn("BLACKJACK", i.t("title"))

    def test_invalid_lang_falls_back(self):
        i = I18N("xx")
        self.assertEqual(i.lang, "en")

    def test_format(self):
        i = I18N("en")
        self.assertIn("5", i.t("starting_chips", chips=5))

    def test_all_keys_present_both_langs(self):
        en_keys = set(STRINGS["en"].keys())
        zh_keys = set(STRINGS["zh"].keys())
        self.assertEqual(en_keys, zh_keys, f"Mismatch: {en_keys ^ zh_keys}")


class TestScoreBoard(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        Path(self.tmp.name).unlink()

    def tearDown(self):
        p = Path(self.tmp.name)
        if p.exists():
            p.unlink()

    def test_empty(self):
        sb = ScoreBoard(self.tmp.name)
        self.assertEqual(sb.top(), [])
        self.assertEqual(sb.best, 0)

    def test_add_and_persist(self):
        sb = ScoreBoard(self.tmp.name)
        sb.add("Alice", 500, 10)
        sb.add("Bob", 300, 5)
        sb2 = ScoreBoard(self.tmp.name)
        self.assertEqual(len(sb2.all), 2)
        self.assertEqual(sb2.best, 500)

    def test_top_sort(self):
        sb = ScoreBoard(self.tmp.name)
        sb.add("A", 100, 5)
        sb.add("B", 300, 3)
        sb.add("C", 200, 10)
        top = sb.top(2)
        self.assertEqual([r["name"] for r in top], ["B", "C"])

    def test_top_limit(self):
        sb = ScoreBoard(self.tmp.name)
        for i in range(15):
            sb.add(f"P{i}", i * 10, i)
        self.assertEqual(len(sb.top(10)), 10)


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        Path(self.tmp.name).unlink()

    def tearDown(self):
        p = Path(self.tmp.name)
        if p.exists():
            p.unlink()

    def test_defaults(self):
        s = Settings(self.tmp.name)
        for k, v in DEFAULTS.items():
            self.assertEqual(s.get(k), v)

    def test_set_and_persist(self):
        s = Settings(self.tmp.name)
        s.set("lang", "en")
        s.set("sound", False)
        s2 = Settings(self.tmp.name)
        self.assertEqual(s2.get("lang"), "en")
        self.assertFalse(s2.get("sound"))

    def test_unknown_key_ignored(self):
        s = Settings(self.tmp.name)
        s.set("nonexistent", "x")
        self.assertNotIn("nonexistent", s.data)


class TestSound(unittest.TestCase):
    def test_disabled(self):
        import io
        buf = io.StringIO()
        s = Sound(enabled=False, volume=2, output=buf)
        s.deal()
        s.win()
        self.assertEqual(buf.getvalue(), "")

    def test_enabled_writes(self):
        import io
        buf = io.StringIO()
        s = Sound(enabled=True, volume=1, output=buf)
        s.deal()
        self.assertEqual(buf.getvalue(), "\a")

    def test_volume_zero_silent(self):
        import io
        buf = io.StringIO()
        s = Sound(enabled=True, volume=0, output=buf)
        s.deal()
        s.win()
        self.assertEqual(buf.getvalue(), "")

    def test_volume_clamp(self):
        s = Sound(volume=99)
        self.assertEqual(s.volume, 3)
        s.set_volume(-5)
        self.assertEqual(s.volume, 0)

    def test_speed_delay(self):
        for k in ("slow", "normal", "fast", "instant"):
            self.assertIn(k, SPEED_DELAY)
        self.assertEqual(speed_delay("instant"), 0.0)
        self.assertEqual(speed_delay("unknown"), SPEED_DELAY["normal"])


if __name__ == "__main__":
    unittest.main()

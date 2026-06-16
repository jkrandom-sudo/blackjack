"""Run all tests."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(str(Path(__file__).resolve().parent), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

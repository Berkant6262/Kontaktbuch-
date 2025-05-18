import unittest
from datenbank_funktion import main

class TestMain(unittest.TestCase):
    def test_main_runs(self):
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised an Exception: {e}")

if __name__ == "__main__":
    unittest.main()

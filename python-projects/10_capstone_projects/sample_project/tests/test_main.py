"""Tests for the expense tracker."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
import os

# Allow import from parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        """Use a temp file instead of the real expenses.json."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        # Patch DATA_FILE to use temp path
        self.patcher = patch.object(main, "DATA_FILE", Path(self.tmp.name))
        self.patcher.start()
        # Initialize with empty list
        with open(self.tmp.name, "w") as f:
            json.dump([], f)

    def tearDown(self):
        self.patcher.stop()
        os.unlink(self.tmp.name)

    def _add(self, amount, category, note=""):
        """Helper: add an expense via argparse namespace."""
        import types
        args = types.SimpleNamespace(amount=amount, category=category, note=note)
        main.cmd_add(args)

    def test_add_and_load(self):
        self._add(12.50, "food", "lunch")
        expenses = main.load_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["amount"], 12.50)
        self.assertEqual(expenses[0]["category"], "food")

    def test_add_normalizes_category(self):
        self._add(5.0, "Food")  # uppercase input
        expenses = main.load_expenses()
        self.assertEqual(expenses[0]["category"], "food")  # stored lowercase

    def test_multiple_expenses(self):
        self._add(10.0, "food")
        self._add(20.0, "transport")
        self._add(5.0, "food")
        expenses = main.load_expenses()
        self.assertEqual(len(expenses), 3)
        food_total = sum(e["amount"] for e in expenses if e["category"] == "food")
        self.assertEqual(food_total, 15.0)

    def test_ids_are_sequential(self):
        for i in range(3):
            self._add(float(i + 1), "misc")
        expenses = main.load_expenses()
        ids = [e["id"] for e in expenses]
        self.assertEqual(ids, [1, 2, 3])

    def test_export_csv(self):
        self._add(25.0, "utilities", "electricity")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_path = f.name
        try:
            import types
            args = types.SimpleNamespace(file=csv_path)
            main.cmd_export(args)
            with open(csv_path) as f:
                content = f.read()
            self.assertIn("utilities", content)
            self.assertIn("25.0", content)
        finally:
            os.unlink(csv_path)

    def test_empty_list(self, capsys=None):
        """List with no expenses doesn't crash."""
        import types, io
        from unittest.mock import patch as _patch
        args = types.SimpleNamespace(category=None)
        with _patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            main.cmd_list(args)
        self.assertIn("No expenses", mock_out.getvalue())


if __name__ == "__main__":
    unittest.main()

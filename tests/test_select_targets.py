"""select_targets.py exists to keep a 155 KB registry out of the conversation. These tests pin that."""
import contextlib
import io
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins" / "founder-pipeline" / "skills" / "web-listings"
sys.path.insert(0, str(SKILL / "scripts"))
import select_targets as st  # noqa: E402

TARGETS = json.loads((SKILL / "config" / "targets.json").read_text())["targets"]


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = st.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class SelectTargets(unittest.TestCase):
    def test_class_filter_returns_only_rows_that_apply(self):
        rows = st.select(TARGETS, brand_class="community")
        self.assertTrue(rows)
        self.assertTrue(all("community" in t["applies_to"] for t in rows))
        self.assertLess(len(rows), len(TARGETS))

    def test_list_output_is_compact_and_carries_no_notes(self):
        code, out, _ = run("--class", "community", "--priority", "1")
        self.assertEqual(code, 0)
        whole = (SKILL / "config" / "targets.json").stat().st_size
        self.assertLess(len(out), whole / 10, "a filtered list must be a small fraction of the file")
        self.assertNotIn(TARGETS[0]["notes"][:60], out)
        self.assertIn(TARGETS[0]["id"], out)  # DIR-0001 is a priority-1 community target

    def test_one_id_returns_the_full_row_with_notes(self):
        code, out, _ = run("--id", TARGETS[0]["id"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["notes"], TARGETS[0]["notes"])

    def test_unassigned_lists_exactly_the_rows_with_no_class(self):
        self.assertEqual({t["id"] for t in st.select(TARGETS, unassigned=True)},
                         {t["id"] for t in TARGETS if not t.get("applies_to")})

    def test_refuses_to_dump_everything(self):
        with self.assertRaises(SystemExit):
            run()

    def test_unknown_id_is_an_error(self):
        code, _, err = run("--id", "DIR-NOPE")
        self.assertEqual(code, 1)
        self.assertIn("no target", err)


if __name__ == "__main__":
    unittest.main()

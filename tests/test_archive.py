"""Local checks for the first-pass X archive. No network."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_tools"))

from validate_archive import HANDLES, validate  # noqa: E402


class ArchiveValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = validate(ROOT)

    def test_archive_valid(self):
        self.assertTrue(self.report["ok"], "\n".join(self.report["errors"]))

    def test_counts(self):
        summary = self.report["summary"]
        self.assertEqual(summary["total_posts"], 1232)
        self.assertEqual(summary["handles"]["alexandr_wang"]["posts"], 512)
        self.assertEqual(summary["handles"]["iiiinvest"]["posts"], 366)
        self.assertEqual(summary["handles"]["silverfang88"]["posts"], 354)
        self.assertEqual(summary["handles"]["alexandr_wang"]["profile_post_count"], 3762)
        self.assertEqual(summary["handles"]["iiiinvest"]["profile_post_count"], 4858)
        self.assertEqual(summary["handles"]["silverfang88"]["profile_post_count"], 19982)
        self.assertFalse(summary["completeness_claim"])
        self.assertFalse(summary["pagination_verified_complete"])

    def test_string_ids_and_order_are_in_the_validator(self):
        # The shared validator is the check. This asserts it actually ran all handles.
        self.assertEqual(set(self.report["summary"]["handles"]), set(HANDLES))

    def test_manifests_deny_completeness(self):
        for handle in HANDLES:
            manifest = json.loads((ROOT / handle / "coverage_manifest.json").read_text(encoding="utf-8"))
            self.assertIs(manifest["claim_of_completeness"], False)
            self.assertEqual(manifest["ids_stored_as"], "strings")

    def test_known_bad_citation_removed_from_analysis(self):
        text = (ROOT / "alexandr_wang" / "analysis.md").read_text(encoding="utf-8")
        self.assertNotIn("809675263590961152", text)
        self.assertIn("809663723006611456", text)

    def test_readme_states_partial_archive(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("not a complete", readme.lower())
        self.assertIn("1,232", readme)
        self.assertIn("alexandr_wang/", readme)
        self.assertIn("iiiinvest/", readme)
        self.assertIn("silverfang88/", readme)


if __name__ == "__main__":
    unittest.main()

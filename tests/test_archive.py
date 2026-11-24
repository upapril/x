"""Local checks for the expanded X archive. No network."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_tools"))

from validate_archive import HANDLES, validate  # noqa: E402

PRIOR_COMMITS = (
    "7c43efc9646ebe174a1e5d43c669865d982909ba",
    "5e939e92cad74c649388927b7d19770641b03240",
)


class ArchiveValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = validate(ROOT)

    def test_archive_valid(self):
        self.assertTrue(self.report["ok"], "\n".join(self.report["errors"]))

    def test_counts(self):
        summary = self.report["summary"]
        self.assertEqual(summary["total_posts"], 15370)
        self.assertEqual(summary["handles"]["alexandr_wang"]["posts"], 1873)
        self.assertEqual(summary["handles"]["iiiinvest"]["posts"], 3856)
        self.assertEqual(summary["handles"]["silverfang88"]["posts"], 9239)
        self.assertEqual(summary["handles"]["taresky"]["posts"], 224)
        self.assertEqual(summary["handles"]["thankUcrypto"]["posts"], 178)
        self.assertGreater(summary["handles"]["taresky"]["pending_windows"], 0)
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
            self.assertIs(manifest["claim_all_tweets"], False)
            self.assertGreater(manifest["expand_job_status_counts"].get("pending", 0), 0)

    def test_known_bad_citation_is_not_linked(self):
        text = (ROOT / "alexandr_wang" / "analysis.md").read_text(encoding="utf-8")
        self.assertNotIn("status/809675263590961152", text)
        self.assertIn("absent", text)
        self.assertIn("809663723006611456", text)

    def test_readme_states_partial_archive(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        lowered = readme.lower()
        self.assertIn("incomplete", lowered)
        self.assertIn("9,239", readme)
        self.assertIn("1,873", readme)
        self.assertIn("3,856", readme)
        self.assertIn("taresky/", readme)
        self.assertIn("thankUcrypto/", readme)
        self.assertIn("INSIGHTS.md", readme)
        self.assertIn("FINANCE_SKILLS_COMPARISON.md", readme)
        self.assertIn("pending", lowered)

    def test_expanded_store_keeps_first_pass_ids(self):
        prior_handles = ("alexandr_wang", "iiiinvest", "silverfang88")
        for commit in PRIOR_COMMITS:
            for handle in prior_handles:
                old = subprocess.check_output(
                    ["git", "show", f"{commit}:{handle}/normalized/posts.jsonl"],
                    cwd=ROOT,
                ).decode("utf-8")
                old_ids = {json.loads(line)["id"] for line in old.splitlines() if line.strip()}
                new_ids = set()
                for line in (ROOT / handle / "normalized" / "posts.jsonl").read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        new_ids.add(json.loads(line)["id"])
                missing = old_ids - new_ids
                self.assertFalse(missing, f"{handle} at {commit[:7]} dropped {len(missing)} ids")


if __name__ == "__main__":
    unittest.main()

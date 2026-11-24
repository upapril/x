"""Checks the vendored finance-skills tree against its provenance manifest.

Does not execute upstream skills, scripts, or package installs.
"""
from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "finance-skills"
PROVENANCE = ROOT / "vendor" / "finance-skills.PROVENANCE.md"
UPSTREAM_SHA = "a0850786e72aa23b92862f9f1635b0de506fe206"


def manifest_hashes(text: str) -> dict[str, str]:
    start = text.index("## sha256")
    fenced = text.index("```\n", start) + 4
    end = text.index("\n```", fenced)
    rows = {}
    for line in text[fenced:end].splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        rows[rel] = digest
    return rows


class VendorFinanceSkillsTest(unittest.TestCase):
    def test_provenance_records_upstream_commit(self):
        text = PROVENANCE.read_text(encoding="utf-8")
        self.assertIn("https://github.com/himself65/finance-skills", text)
        self.assertIn(UPSTREAM_SHA, text)
        self.assertIn("Copyright (c) 2025 Alex Yang", text)
        self.assertIn("git archive", text)
        self.assertIn("2026-11-24", text)

    def test_license_is_the_upstream_mit_notice(self):
        license_text = (VENDOR / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2025 Alex Yang", license_text)
        self.assertIn("Permission is hereby granted, free of charge", license_text)
        digest = hashlib.sha256((VENDOR / "LICENSE").read_bytes()).hexdigest()
        self.assertEqual(
            digest,
            "afb4751be1f58107f1daf07472d16f7eb6ec6df09996b5758e8ef6cc6d5a0a30",
        )

    def test_tree_matches_import_manifest(self):
        expected = manifest_hashes(PROVENANCE.read_text(encoding="utf-8"))
        self.assertEqual(len(expected), 180)
        actual = {}
        for path in VENDOR.rglob("*"):
            if path.is_file():
                rel = path.relative_to(VENDOR).as_posix()
                actual[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(actual, expected)

    def test_no_git_metadata_or_dependency_install(self):
        self.assertFalse((VENDOR / ".git").exists())
        self.assertFalse((VENDOR / "node_modules").exists())
        names = {p.name for p in VENDOR.rglob("*")}
        self.assertNotIn(".git", names)
        self.assertNotIn("node_modules", names)

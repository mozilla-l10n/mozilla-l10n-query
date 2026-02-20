#!/usr/bin/env python3
"""Unit tests for generate_static.py."""

import sys
import unittest
from pathlib import Path

# Make the generator importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app" / "scripts"))

from generate_static import (
    generate_all_repos,
    generate_single_repo,
    generate_type_repos,
    generate_bugzilla,
    generate_tool,
)

TESTFILES = Path(__file__).parent.parent / "testfiles"


class TestAllRepos(unittest.TestCase):
    def test_all_repos(self):
        result = generate_all_repos(TESTFILES)
        self.assertIsInstance(result, list)
        for item in result:
            for key in ("id", "display_order", "name", "locales", "type", "enabled"):
                self.assertIn(key, item)
            self.assertEqual(item["locales"], sorted(item["locales"]))

    def test_single_repo_beta(self):
        result = generate_single_repo(TESTFILES, "beta")
        self.assertIsNotNone(result)
        for key in ("id", "name", "display_order", "locales", "type", "enabled"):
            self.assertIn(key, result)
        self.assertEqual(result["id"], "beta")
        self.assertEqual(result["locales"], sorted(result["locales"]))

    def test_unknown_repo_returns_none(self):
        result = generate_single_repo(TESTFILES, "nonexistent")
        self.assertIsNone(result)


class TestTypeRepos(unittest.TestCase):
    def test_type_product(self):
        result = generate_type_repos(TESTFILES, "product")
        self.assertIsInstance(result, list)
        for item in result:
            self.assertEqual(item["type"], "product")

    def test_type_web(self):
        result = generate_type_repos(TESTFILES, "web")
        self.assertIsInstance(result, list)
        for item in result:
            self.assertEqual(item["type"], "web")


class TestBugzilla(unittest.TestCase):
    def test_bugzilla_www(self):
        result = generate_bugzilla(TESTFILES, "www")
        self.assertIsInstance(result, dict)
        for locale, full_name in result.items():
            self.assertIsInstance(locale, str)
            self.assertIsInstance(full_name, str)

    def test_bugzilla_product(self):
        result = generate_bugzilla(TESTFILES, "product")
        self.assertIsInstance(result, dict)
        for locale, full_name in result.items():
            self.assertIsInstance(locale, str)
            self.assertIsInstance(full_name, str)


class TestTools(unittest.TestCase):
    def test_tool_pontoon(self):
        result = generate_tool(TESTFILES, "pontoon")
        self.assertIsInstance(result, list)
        self.assertEqual(result, sorted(result))

    def test_tool_all(self):
        result = generate_tool(TESTFILES, "all")
        self.assertIsInstance(result, dict)
        self.assertIn("pontoon", result)
        self.assertIn("pontoon-mozorg", result)


if __name__ == "__main__":
    unittest.main()

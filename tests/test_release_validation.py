import unittest

from scripts.validate_release import extract_release_notes


class ReleaseValidationTests(unittest.TestCase):
    def setUp(self):
        self.changelog = """# Changelog

## [Unreleased]

Pending.

## [1.2.3] - 2026-09-29

### Added
- A dated release note.

## [1.2.2] - 2026-09-01

- An older note.
"""

    def test_extracts_only_the_matching_dated_section(self):
        notes = extract_release_notes("v1.2.3", self.changelog)
        self.assertIn("## [1.2.3] - 2026-09-29", notes)
        self.assertIn("A dated release note", notes)
        self.assertNotIn("An older note", notes)

    def test_rejects_non_stable_tag_syntax(self):
        with self.assertRaisesRegex(ValueError, "stable vMAJOR.MINOR.PATCH"):
            extract_release_notes("v1.2.3-rc.1", self.changelog)

    def test_requires_a_matching_changelog_section(self):
        with self.assertRaisesRegex(ValueError, "CHANGELOG.md must contain"):
            extract_release_notes("v1.2.4", self.changelog)

    def test_rejects_invalid_release_date(self):
        invalid = "## [1.2.3] - 2026-99-99\n- A note.\n"
        with self.assertRaisesRegex(ValueError, "valid YYYY-MM-DD"):
            extract_release_notes("v1.2.3", invalid)

    def test_rejects_empty_release_notes(self):
        empty = "## [1.2.3] - 2026-09-29\n\n### Added\n"
        with self.assertRaisesRegex(ValueError, "at least one release-note bullet"):
            extract_release_notes("v1.2.3", empty)


if __name__ == "__main__":
    unittest.main()

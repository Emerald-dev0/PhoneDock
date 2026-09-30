#!/usr/bin/env python3
"""Validate a stable release tag and extract its dated changelog section."""

from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path

SEMVER_TAG = re.compile(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")


def extract_release_notes(tag: str, changelog: str) -> str:
    if not SEMVER_TAG.fullmatch(tag):
        raise ValueError("Release tags must use stable vMAJOR.MINOR.PATCH syntax.")

    version = tag[1:]
    lines = changelog.splitlines()
    heading_pattern = re.compile(rf"^## \[{re.escape(version)}\] - ([0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}})$")
    start = next(
        ((index, heading_pattern.fullmatch(line)) for index, line in enumerate(lines) if heading_pattern.fullmatch(line)),
        None,
    )
    if start is None:
        raise ValueError(f"CHANGELOG.md must contain a dated '## [{version}] - YYYY-MM-DD' section.")

    start_index, heading_match = start
    try:
        date.fromisoformat(heading_match.group(1))
    except ValueError as error:
        raise ValueError("The changelog release date must be a valid YYYY-MM-DD date.") from error

    end_index = next(
        (index for index in range(start_index + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    section = lines[start_index:end_index]
    if not any(line.strip().startswith("-") for line in section[1:]):
        raise ValueError("The dated changelog section must contain at least one release-note bullet.")
    return "\n".join(section).strip() + "\n"


def main() -> int:
    tag = os.environ.get("RELEASE_TAG", "")
    runner_temp = os.environ.get("RUNNER_TEMP")
    if not runner_temp:
        print("RUNNER_TEMP is required to write release notes.", file=sys.stderr)
        return 1

    try:
        notes = extract_release_notes(tag, Path("CHANGELOG.md").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    output = Path(runner_temp) / "release-notes.md"
    output.write_text(notes, encoding="utf-8")
    print(f"Validated {tag}; release notes written for draft review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run dependency-free repository, documentation-link, and XML checks."""

from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "docs/PROJECT_AUDIT.md",
    "docs/PRODUCT_SPEC.md",
    "docs/ROADMAP.md",
    "docs/ARCHITECTURE.md",
    "docs/PLATFORM_SUPPORT.md",
    "docs/PROTOCOL.md",
    "docs/SECURITY.md",
    "docs/TESTING.md",
    "docs/DESIGN_SYSTEM.md",
    "docs/FEATURE_STATUS.md",
    "docs/decisions/README.md",
    ".github/pull_request_template.md",
    "scripts/check_repository.py",
    "scripts/smoke_desktop.py",
    "scripts/validate_release.py",
    "tests/test_release_validation.py",
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FENCED_BLOCK = re.compile(r"(?ms)^\s*(```|~~~).*?^\s*\1\s*$")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
INLINE_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
NON_SLUG = re.compile(r"[^\w\-\s]", re.UNICODE)


def markdown_files() -> list[Path]:
    paths = [ROOT / name for name in ("README.md", "CONTRIBUTING.md", "CHANGELOG.md")]
    paths.extend((ROOT / "docs").rglob("*.md"))
    paths.extend((ROOT / ".github").rglob("*.md"))
    return sorted(path for path in paths if path.is_file())


def heading_anchors(path: Path) -> set[str]:
    content = path.read_text(encoding="utf-8")
    counts: defaultdict[str, int] = defaultdict(int)
    anchors: set[str] = set()
    for line in content.splitlines():
        match = HEADING.match(line)
        if not match:
            continue
        text = INLINE_LINK.sub(r"\1", match.group(1))
        text = HTML_TAG.sub("", text).replace("`", "").lower()
        text = NON_SLUG.sub("", text).strip()
        base = re.sub(r"\s+", "-", text)
        count = counts[base]
        counts[base] += 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def check_markdown_links(paths: list[Path]) -> tuple[int, list[str]]:
    errors: list[str] = []
    checked = 0
    anchors_by_path = {path.resolve(): heading_anchors(path) for path in paths}

    for source in paths:
        content = FENCED_BLOCK.sub("", source.read_text(encoding="utf-8"))
        for match in MARKDOWN_LINK.finditer(content):
            destination = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc:
                continue

            target_text = unquote(parsed.path)
            target = (source.parent / target_text).resolve() if target_text else source.resolve()
            checked += 1
            if not target.exists():
                errors.append(f"{source.relative_to(ROOT)}: broken link target {destination!r}")
                continue

            fragment = unquote(parsed.fragment)
            if fragment and target.is_file() and target.suffix.lower() == ".md":
                target_anchors = anchors_by_path.get(target)
                if target_anchors is None:
                    target_anchors = heading_anchors(target)
                if fragment.lower() not in {anchor.lower() for anchor in target_anchors}:
                    errors.append(
                        f"{source.relative_to(ROOT)}: missing Markdown anchor "
                        f"{fragment!r} in {target.relative_to(ROOT)}"
                    )
    return checked, errors


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"required file is missing: {relative}")

    markdown = markdown_files()
    link_count, link_errors = check_markdown_links(markdown)
    errors.extend(link_errors)

    xml_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and (path.suffix.lower() == ".xml" or path.suffix.lower() == ".vcxproj")
        and ".git" not in path.parts
        and ".venv" not in path.parts
        and "build" not in path.parts
    ]
    for path in sorted(xml_files):
        try:
            import xml.etree.ElementTree as ET

            ET.parse(path)
        except (ET.ParseError, OSError) as error:
            errors.append(f"{path.relative_to(ROOT)}: invalid XML: {error}")

    version_catalog = ROOT / "android/gradle/libs.versions.toml"
    if version_catalog.is_file():
        try:
            tomllib.loads(version_catalog.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError) as error:
            errors.append(f"{version_catalog.relative_to(ROOT)}: invalid TOML: {error}")

    tracked_local_properties = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "android/local.properties"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if tracked_local_properties.returncode == 0:
        errors.append("android/local.properties is tracked; keep local SDK paths ignored")

    if errors:
        print("Repository checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Repository checks passed: "
        f"{len(markdown)} Markdown files, {link_count} local links, "
        f"{len(xml_files)} XML project/resource files, Android version catalog."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

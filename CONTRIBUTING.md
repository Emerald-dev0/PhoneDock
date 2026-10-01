# Contributing to PhoneDock

Thanks for helping improve PhoneDock. The repository is in a recovery/foundation stage: Android, Linux and Windows contain prototypes, while iOS, macOS and web projects are not present. Read [the audit](docs/PROJECT_AUDIT.md), [product specification](docs/PRODUCT_SPEC.md), [platform matrix](docs/PLATFORM_SUPPORT.md) and [roadmap](docs/ROADMAP.md) before assuming a capability exists.

## Before starting

- Keep work focused on a documented issue or acceptance criterion; discuss protocol, identity, security, platform, dependency or repository-wide architecture changes before implementing them.
- Inspect existing code and preserve useful platform-specific work. Do not move/rewrite an app to match a proposed directory tree without a migration reason.
- Do not start a new app/shared package or claim a platform feature until its responsibility and build/test path are defined.
- For security-sensitive changes, review [SECURITY.md](docs/SECURITY.md) and [PROTOCOL.md](docs/PROTOCOL.md) first. Do not put vulnerability details, tokens, certificates or private keys in public issues or source.
- Do not change the license without explicit maintainer authorization. The checked-in license attribution still contains template text; maintainers should resolve it before redistribution claims are made.

## Branches and pull requests

Create a focused branch from the repository's current development branch. Suggested prefixes are `feat/`, `fix/`, `docs/`, `build/` and `test/`; follow any repository/automation constraints that apply to your environment. Open one coherent PR targeting the current development branch. Keep generated files and local SDK/IDE configuration out of commits.

A PR should:

- explain the problem, change and user/platform impact;
- link an issue/requirement or add/update one when needed;
- state which platforms are affected and which are not;
- include tests, docs and migration/configuration updates appropriate to the change;
- describe security/privacy/permission and compatibility impact;
- complete the PR template's verification and status checklist;
- identify blockers and remaining acceptance criteria instead of overstating completion.

Do not include signing credentials, local.properties, build outputs, personal data, or unrelated formatting changes.

## Development setup and checks

Follow application-specific setup in [README.md](README.md) and commands in [TESTING.md](docs/TESTING.md). In brief:

- Android requires a compatible JDK and Android SDK.
- Linux desktop uses the existing Python/PySide6/PyAV/Zeroconf application and `desktop/requirements.txt`.
- Windows C++ builds require Visual Studio C++ tools and the Windows SDK.
- iOS/macOS/web have no source projects or local build commands yet.

Before submitting, run the checks relevant to your change where available:

```bash
python3 scripts/check_repository.py
python3 -m compileall -q desktop
bash -n desktop/run_desktop.sh desktop/build_deb.sh
```

For Android run Gradle unit-test, lint and build tasks; for Linux install dependencies and exercise the changed runtime; for Windows build the application project. Add targeted tests for new behavior. If the required OS, SDK, hardware, credential or network is unavailable, report the exact blocker and do not describe the test as passed. See [TESTING.md](docs/TESTING.md) for the full matrix.

## Coding and documentation conventions

- Follow `.editorconfig`, the existing platform language conventions and project-local style. Kotlin follows the configured official style; Python uses four-space indentation; avoid broad reformatting of unrelated files.
- Prefer small, reviewable changes and explicit resource/lifecycle ownership. Validate peer-controlled data and use safe error handling. Avoid adding dependencies unless they have a clear, maintained purpose.
- Keep build files, workflows, scripts, docs and actual app behavior consistent. Do not add speculative API/protocol behavior or claim a product capability from UI/source presence alone.
- Update `docs/PROJECT_AUDIT.md` when repository facts materially change, `docs/PLATFORM_SUPPORT.md` when platform evidence changes, and `docs/ROADMAP.md` when phase scope/completion changes.
- Record a consequential accepted architectural decision in `docs/decisions/` as an ADR. Proposals remain proposals until review.
- Preserve version and changelog accuracy. There is no verified past release history in this checkout; follow `CHANGELOG.md` for future entries.

## Defect and security reports

Use the GitHub issue templates for reproducible non-sensitive defects and feature proposals. Include platform/OS, app revision, steps, expected/actual result, relevant non-sensitive logs and verification performed. Do not attach personal files, notification/clipboard content, authentication material, or private keys.

For a suspected security issue, do not publish exploitable details in a public issue. Use GitHub's private vulnerability reporting if enabled for the repository; if no private channel is available, ask a repository maintainer to establish one before disclosure. No private security contact is asserted by this document.

## Honest completion reports

Separate implementation state from verification evidence. State the exact commands and results; identify checks that failed, were not run, or were blocked; name hardware/OS tested; and list remaining acceptance criteria. A build is not a runtime test, a mock is not an integration, and local workflow syntax parsing is not a successful GitHub Actions run. Use the vocabulary in [FEATURE_STATUS.md](docs/FEATURE_STATUS.md).

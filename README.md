# PhoneDock

**One connected workspace for the devices you use.**

PhoneDock is a local-first cross-platform device integration project. Its goal is to help compatible phones and computers discover, trust and work with one another—without requiring a cloud account or relay for core workflows that can run directly over a local connection.

> **Repository status (2026-09-29):** this is a revival-stage project, not a production-ready release. Kotlin/Compose Android, Python/PySide6 Linux and C++ Windows prototypes are present. Their networking/video behavior has not been verified end-to-end on real devices. iOS, macOS and web application source was not found. Pairing/authentication, file transfer, clipboard synchronization, notification forwarding and a working second-display implementation are not present. See the [repository audit](docs/PROJECT_AUDIT.md) for evidence and build limitations.

## Table of contents

- [Product vision](#product-vision)
- [Local-first and privacy](#local-first-and-privacy)
- [Application targets](#application-targets)
- [Intended capabilities](#intended-capabilities)
- [Current implementation status](#current-implementation-status)
- [Architecture direction](#architecture-direction)
- [Repository layout](#repository-layout)
- [Development setup](#development-setup)
- [Build, test and CI](#build-test-and-ci)
- [Releases and updates](#releases-and-updates)
- [Roadmap](#roadmap)
- [Limitations and open decisions](#limitations-and-open-decisions)
- [Engineering and contribution](#engineering-and-contribution)
- [License status](#license-status)
- [Project documentation](#project-documentation)

## Product vision

PhoneDock aims to connect physical devices into one coherent workspace. A user should be able to find a compatible device, decide whether to trust it, connect securely, see what it can do, and move between supported workflows without guessing whether a control is real.

It is broader than screen mirroring. The intended experience combines device discovery and management, supported Android screen viewing/control, file and content handoff, optional clipboard sharing, supported notification/media integration, diagnostics and—in a separately researched path—using Android as an additional display.

Product intent is not implementation evidence. Every feature and platform claim must be backed by source, automated tests, and platform/hardware evidence appropriate to that claim. The [feature-status guide](docs/FEATURE_STATUS.md) defines the vocabulary used throughout the project.

## Local-first and privacy

Direct local operation is the default for local-device workflows. Pairing, local screen sessions and transfers should not silently depend on an account, cloud storage or relay when both devices can communicate directly. Any future optional cloud service must be explicitly disclosed and must not become an undisclosed requirement for a local feature.

“Local” does not mean “secure.” A shared Wi-Fi network, discovery announcement or IP address does not establish trust. The current Android prototype accepts a plain TCP connection without a defined authenticated or encrypted session. Do not use it for confidential data or expose it to an untrusted network. See [Security](docs/SECURITY.md) and [Protocol](docs/PROTOCOL.md).

## Application targets

PhoneDock is intended to have six application targets. They will not have identical capabilities: each should feel native and report its actual OS/device support.

| Target | Intended experience | Repository evidence today |
|---|---|---|
| **Android** | Native mobile companion; the initial phone-side target for user-consented screen capture and supported integrations. | Kotlin/Jetpack Compose app, onboarding/dashboard, NSD/TCP service and MediaProjection/MediaCodec source. Build/runtime/hardware behavior remains unverified; key session and UI wiring is incomplete. |
| **iOS** | Native SwiftUI companion using Apple's platform conventions and materials. Capabilities must follow iOS APIs and policy; do not promise Android-equivalent capture, background operation or remote input. | No iOS source, Xcode project or assets found. |
| **Linux desktop** | Desktop device discovery/management and, when implemented, Android viewing/control, transfer and diagnostics. | Python/PySide6 UI, `zeroconf` discovery, TCP receiver and PyAV decoder code exist. They are prototype/unverified and have no product test suite. |
| **Windows desktop** | Native-feeling Windows workspace and supported Android receiver/control workflows. | C++ project explores DNS-SD, Winsock, Media Foundation and Direct3D 11. Decoder/render methods are unfinished; the separate display-driver project has no implementation source. |
| **macOS desktop** | First-class Mac application that respects macOS permissions, security and distribution conventions. | No macOS source, Xcode project or assets found. Technology choice remains open. |
| **Web app and product website** | Responsive product, documentation and release information, plus only those browser utilities that are secure and supported. | No web application or website source/configuration found. A browser is not assumed to replace native device or driver APIs. |

The detailed per-platform capability matrix and test prerequisites are in [PLATFORM_SUPPORT.md](docs/PLATFORM_SUPPORT.md).

## Intended capabilities

The following describes the target product scope, not a promise that these features are already available. Requirements and acceptance criteria are in [PRODUCT_SPEC.md](docs/PRODUCT_SPEC.md).

### Connect and manage devices

- Automatic discovery on supported local networks and manual connection where supported.
- Local Wi-Fi and platform/device-specific USB connectivity.
- Explicit trusted-device pairing, authenticated sessions, capability negotiation and revocation.
- Accurate device status, connection type, cancellation, disconnection and bounded reconnection.
- Useful diagnostics for permissions, discovery, transport and session failures.

Discovery is not authentication. A device name, IP address or service announcement must not grant access.

### View and control Android

- User-consented Android screen capture and streaming to supported desktop applications.
- Correct aspect ratio, lifecycle/rotation behavior, configurable quality and measurable performance where implemented.
- Supported mouse, keyboard or touch input only where Android APIs, permissions and device configuration allow it. Additional Accessibility/ADB/developer prerequisites must be explicit, not implied.
- iOS is a separate capability target; PhoneDock will not promise arbitrary iPhone screen capture or system-wide input injection without a supported API path.

### Move content and stay in sync

- Selected-file transfer, a shared transfer inbox, queues/progress/cancellation, integrity checking and transfer history.
- Explicit handoff of links, text, images and other supported content.
- Optional clipboard synchronization with per-direction controls, loop prevention, clear status and privacy safeguards.
- Notification forwarding and media controls only on platforms that expose the required APIs and permissions.

### Manage privacy and performance

- User-visible capture/session state, stop and revoke controls, trusted-device management, permission explanations and privacy preferences.
- Connection diagnostics and performance monitoring based on real measurements—not placeholder values.
- Android-as-an-additional-display mode only if a safe, maintainable host implementation is proven for the named operating systems and devices.

## Current implementation status

| Area | Evidence-based status |
|---|---|
| Android UI | Onboarding and dashboard prototype; dashboard state is not bound to the connection service, and settings is a TODO. |
| Android discovery/session | NSD registration, ephemeral TCP listener and client acceptance are implemented in source but not verified. No pairing, authentication, session negotiation or input reader is present. |
| Android capture | MediaProjection/AVC capture and frame callbacks exist, but the encoder/service lifecycle and receiver path have not been verified on hardware. |
| Linux client | PySide6 onboarding/discovery screens, Zeroconf browser, TCP parser, PyAV decoder and mouse-message sender exist. Integration is unverified; the Android side does not consume those input messages. |
| Windows client | DNS-SD, TCP receive and decoder/renderer scaffolding exist; decode/render contains TODOs and no runtime build/result is available yet. |
| Shared protocol | Similar length-prefixed frame code exists independently in Android, Linux and Windows. The Windows header has unused PDP version/port constants. There is no finalized protocol or compatibility claim. |
| Other product features | USB, pairing/trusted identity, files, clipboard, notification forwarding, media controls, transfer history, diagnostics and working second-display support were not found. |
| iOS/macOS/web | No application/site implementation was found. |

The full source-by-source classification, security findings, version/configuration details and verification limits are in [PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md). No release tags were present in the checked-out history; Android/Linux `1.1.0` strings are not proof of a published release.

## Architecture direction

Keep each app's UI and OS integration native to its platform. Separate presentation, platform adapters, device identity/capabilities, session/security, transport, media and data workflows. A shared protocol or portable core may be useful later, but should be introduced only after its boundary, language and ownership are justified; Phase 0 does not add a fake shared package or monorepo build system.

The observed prototype path is Android MediaProjection/MediaCodec → TCP → Linux PyAV or Windows Media Foundation/Direct3D scaffolding. Its frame prefix is undocumented and unauthenticated; source similarity is not proof of interoperability. Discovery, pairing, session lifecycle, error propagation, protocol versioning and video/data pipelines are described with observed/proposed distinctions in [ARCHITECTURE.md](docs/ARCHITECTURE.md) and [PROTOCOL.md](docs/PROTOCOL.md).

## Repository layout

### Existing application layout

```text
android/                Kotlin/Compose Android Gradle app
  app/src/main/         activity, capture, connectivity, UI and resources
desktop/                Python/PySide6 Linux prototype, scripts and requirements
windows/                C++ desktop prototype, common Windows header and driver scaffold
```

### Engineering foundation added in this phase

```text
.github/workflows/      pull-request/main CI and tagged draft-release workflow
.github/ISSUE_TEMPLATE/  issue forms in Markdown form
docs/                   audit, product, roadmap, architecture, security, tests, design
  decisions/            ADR process; no decisions pre-approved
scripts/                repository, smoke and release-validation checks
tests/                  standard-library tests for release validation policy
```

Future `ios/`, `macos/`, `web/`, shared packages, design assets and cross-platform tests should be added only when they have real source and defined responsibilities. Existing applications are not being moved merely to match a template. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the proposed organization and migration policy.

## Development setup

### Android

Prerequisites: JDK 17 (used by CI), Android SDK/platform/build tools for API 35, and a compatible Gradle environment. The checked-in Gradle wrapper is in `android/`.

```bash
cd android
./gradlew --no-daemon testDebugUnitTest lintDebug assembleDebug
```

Set `ANDROID_HOME` or `ANDROID_SDK_ROOT` locally, or create an ignored `android/local.properties` with your own SDK path. Do not commit machine-specific paths. This repository currently has no Android unit/instrumentation test source; the command builds/lints and runs empty test tasks until tests are added.

### Linux desktop

Prerequisites: Python 3 and the packages in `desktop/requirements.txt`; a display session and suitable network are needed to run the interactive client.

```bash
cd desktop
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -m compileall -q .
./run_desktop.sh
```

The launcher expects the `desktop/venv` directory. Debian packaging uses the existing `build_deb.sh` prototype and additionally needs PyInstaller and `dpkg-deb`; its package metadata/launcher integration has not been validated for distribution.

### Windows desktop

Prerequisites: Windows, Visual Studio C++ tools/toolset v143, the Windows SDK, and Media Foundation/Direct3D headers and libraries. From a Developer PowerShell:

```powershell
msbuild windows\PhoneDock.App\PhoneDock.App.vcxproj /m /p:Configuration=Release /p:Platform=x64 /p:AppxPackage=false
```

The driver project is not buildable as a product: it has no implementation source and needs WDK/signing/platform research.

### iOS, macOS and web

No source project, dependency file, build script or test command exists yet. iOS/macOS work will require an appropriate macOS/Xcode environment; web prerequisites should be selected when a real web project is approved.

## Build, test and CI

Run repository checks from the root:

```bash
python3 scripts/check_repository.py
python3 -m compileall -q desktop
bash -n desktop/run_desktop.sh desktop/build_deb.sh
```

GitHub Actions is configured for pull requests and pushes to `main`. It runs documentation/repository and source checks, the Linux Python dependency/import job, Android Gradle unit-test/lint/debug build tasks, and a Windows C++ application build attempt. Jobs use read-only repository permissions, pinned action commit SHAs, timeouts and cancellation for superseded CI. The driver, Apple apps and web app are not claimed as built because their required implementation/configuration is missing.

A locally parsed workflow file is not a successful GitHub Actions run. Local Python dependency installation, `pip check`, top-level package imports (`PySide6`, PyAV and Zeroconf), source compilation and shell syntax pass; importing Qt widgets/running the offscreen UI smoke could not run here because system `libGL.so.1` is absent. The Android build could not start locally because Java/Android SDK were unavailable, and Windows could not be built on this Linux environment. No hardware or end-to-end test is claimed. Read [TESTING.md](docs/TESTING.md) for verification levels and test cases.

## Releases and updates

The repository has no verified release/tag history. The convention proposed for future releases is `vMAJOR.MINOR.PATCH`, subject to project versioning approval. Before tagging, add a dated matching section to [CHANGELOG.md](CHANGELOG.md).

A tag-triggered workflow waits for CI and creates a **draft source-only GitHub Release** for maintainer review. It does not build/sign/notarize or attach application binaries: current Android release output is not configured for production signing, Linux packaging is prototype-grade, and Windows/driver work is incomplete. No release is created by this documentation change. A maintainer must verify any genuine platform artifacts and checksums before publishing.

A GitHub Release does not update an installed application. Automatic update delivery, rollback, store distribution and platform signing/notarization remain separate work. See [CHANGELOG.md](CHANGELOG.md) and [ROADMAP.md](docs/ROADMAP.md).

## Roadmap

1. **Phase 0 — Repository recovery and engineering foundation:** audit existing code, establish accurate product docs, conventions and CI.
2. **Phase 1 — Product, design, architecture and threat model:** review requirements, prototype visual direction and record actual decisions.
3. **Phase 2 — Protocol and cross-platform engineering foundation:** specify version/security/capability boundaries and test vectors.
4. **Phase 3 — Trusted local discovery and session lifecycle:** pairing, authentication, state, cancellation and reconnection.
5. **Phase 4 — Android capture and desktop viewing:** complete a tested end-to-end screen path.
6. **Phase 5 — Supported remote control and USB:** implement only reviewed, platform-supported paths.
7. **Phase 6 — File transfer and content handoff:** reliable, integrity-checked transfer and inbox.
8. **Phase 7 — Clipboard, notifications, media and device management:** opt-in platform-specific integrations.
9. **Phase 8 — iOS companion.**
10. **Phase 9 — Web application and product website.**
11. **Phase 10 — Android second-display feasibility and implementation.**
12. **Phase 11 — Production hardening and versioned releases.**

Each phase has platform owners/dependencies, tests and exit criteria in [ROADMAP.md](docs/ROADMAP.md). Phase status is evidence-based; a folder, mockup or PR description cannot complete a phase.

## Limitations and open decisions

- No authenticated/encrypted protocol or trusted-device pairing exists; do not use the prototypes for sensitive content.
- No product-wide supported OS/device matrix, Linux distribution baseline, performance target or hardware validation has been established. The current x86_64 PySide6 wheel requires glibc 2.34 or newer; other Linux architectures/distributions are not verified.
- Discovery implementations and frame parsing are duplicated across Android/Linux/Windows; their behavior is not declared interoperable.
- Windows video rendering and driver implementation are incomplete; iOS, macOS and web source is absent.
- The current UI/illustrations use an older “Harvst” palette; the Android launcher icon is a template icon. A premium indigo/ice-blue/porcelain/deep-ink design direction is proposed, not finalized. See [DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md).
- The `LICENSE` file contains MIT license text but its copyright line still includes template wording. This project overview does not make a legal conclusion; maintainers should confirm attribution before making licensing/distribution claims. No license change was made.

## Engineering and contribution

Use the actual platform stack, preserve working code, add targeted tests, keep sensitive data out of logs, and update docs when source or compatibility changes. Do not implement a new protocol/framework or create mock packages without a reviewed need. Report exactly what built, what tests ran, what hardware was exercised, what remains blocked, and which acceptance criteria remain.

Read [CONTRIBUTING.md](CONTRIBUTING.md), use the [pull-request template](.github/pull_request_template.md), and follow the issue templates in `.github/ISSUE_TEMPLATE/`.

## License status

A root `LICENSE` file is present and contains MIT terms, but its copyright line includes the template text `NACOS OAU (or your name)`. The project has not changed that file or resolved the attribution in this phase. Do not rely on this README as legal confirmation; request maintainer review.

## Project documentation

- [Repository audit](docs/PROJECT_AUDIT.md) — evidence-based baseline, technology and risks.
- [Product specification](docs/PRODUCT_SPEC.md) — requirements, boundaries and acceptance criteria.
- [Roadmap](docs/ROADMAP.md) — phases, dependencies, owners and completion gates.
- [Architecture](docs/ARCHITECTURE.md) — observed structure and proposed boundaries.
- [Platform support](docs/PLATFORM_SUPPORT.md) — capability/build/test matrix.
- [Protocol](docs/PROTOCOL.md) — current wire-code findings and unresolved design.
- [Security](docs/SECURITY.md) — local-first assumptions, threat model and review gates.
- [Testing](docs/TESTING.md) — test levels, commands and honest reporting.
- [Design system](docs/DESIGN_SYSTEM.md) — existing assets and proposed visual direction.
- [Feature-status method](docs/FEATURE_STATUS.md) — status/evidence discipline.
- [Contributing](CONTRIBUTING.md) and [changelog policy](CHANGELOG.md).

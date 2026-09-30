# PhoneDock repository audit

- **Audit date:** 2026-09-29
- **Baseline revision:** `4d8c51f9e11def19df59aa90c156c362e34046e2`
- **Scope:** tracked application source, build files, assets, scripts, README, Git history available in this checkout, and local tool availability. The checked-out history is shallow/grafted and exposes only the baseline commit; conclusions about earlier development history are therefore limited.

This audit records repository evidence, not product intent. Product requirements are in [PRODUCT_SPEC.md](PRODUCT_SPEC.md); the platform status vocabulary is in [FEATURE_STATUS.md](FEATURE_STATUS.md).

## Executive summary

PhoneDock is a small collection of platform-specific experiments, not yet a complete cross-platform product. The repository contains:

- A native Kotlin/Jetpack Compose Android application with onboarding/dashboard UI, Android Network Service Discovery (NSD), a TCP listener, and a MediaProjection/MediaCodec AVC capture path.
- A Python/PySide6 Linux desktop prototype with Zeroconf browsing, a TCP frame receiver, a PyAV H.264 decoder, and a custom video widget.
- A C++ Windows console/application prototype with DNS-SD browsing, Winsock receiving, Media Foundation decoder scaffolding, and Direct3D 11 renderer scaffolding. A separate driver project file and a shared Windows header exist, but no driver implementation source was found.

The Android and Linux source contain real networking and video-related code, but no build, automated test, end-to-end, or hardware results establish that those pieces work together. The Windows code is also unverified and visibly incomplete. There is no iOS, macOS, or web application source, no cross-platform shared library, no finalized protocol, no pairing/authentication implementation, no file-transfer or clipboard implementation, and no existing CI workflow or test suite.

The previous root README described a broad intended product and future architecture. It was not evidence that those capabilities existed. This phase adds a documented specification and a CI foundation while preserving the existing applications and their assets.

## Repository map

### Baseline contents

```text
.
├── .gitignore
├── LICENSE
├── README.md
├── android/
│   ├── app/
│   │   ├── build.gradle.kts
│   │   └── src/main/                 # Compose screens, service, capture, resources
│   ├── build.gradle.kts
│   ├── gradle/                       # version catalog and wrapper
│   ├── gradlew / gradlew.bat
│   ├── settings.gradle.kts
│   └── local.properties              # removed by this phase; machine-specific path
├── desktop/                          # Python/PySide6 Linux prototype and scripts
└── windows/
    ├── PhoneDock.App/                # C++ console/client prototype
    ├── PhoneDock.Common/             # Windows-only declarations
    └── PhoneDock.Driver/             # project configuration; no driver sources found
```

### Phase 0 additions

```text
.
├── .editorconfig
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/                   # CI and draft source-release automation
│   ├── dependabot.yml
│   └── pull_request_template.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/
│   ├── decisions/                    # ADR process; no product decision is pre-approved
│   ├── ARCHITECTURE.md
│   ├── DESIGN_SYSTEM.md
│   ├── FEATURE_STATUS.md
│   ├── PLATFORM_SUPPORT.md
│   ├── PRODUCT_SPEC.md
│   ├── PROJECT_AUDIT.md
│   ├── PROTOCOL.md
│   ├── ROADMAP.md
│   ├── SECURITY.md
│   └── TESTING.md
├── scripts/
│   ├── check_repository.py
│   ├── smoke_desktop.py
│   └── validate_release.py
├── tests/test_release_validation.py
└── desktop/requirements.txt
```

No application was moved and no empty future application/package directory was added.

## Applications and components discovered

| Component | Actual technology/configuration | Evidence and status |
|---|---|---|
| Android app | Kotlin, Android Gradle Plugin 8.7.2, Kotlin 2.0.21, Jetpack Compose/Material 3, Gradle 8.9 wrapper; one `:app` module | `android/settings.gradle.kts`, `android/app/build.gradle.kts`, `android/gradle/libs.versions.toml`; project and source exist, build not verified in this environment |
| Android UI | Compose onboarding pager, dashboard, custom Canvas illustrations, Material theme | `ui/onboarding/*`, `ui/dashboard/*`, `ui/theme/*`; UI is present, but dashboard state is local placeholder state and controls are not connected to the service |
| Android capture/connection | `MediaProjection`, `MediaCodec` AVC encoder, `VirtualDisplay`, foreground `ConnectionService`, `ServerSocket`, NSD registration | `capture/ScreenStreamer.kt`, `connectivity/ConnectionService.kt`, `connectivity/NsdHelper.kt`; implementation is partial and unverified; no hardware or end-to-end test |
| Linux desktop | Python 3, PySide6, PyAV, `zeroconf`; Bash launcher and Debian packaging script | `desktop/*.py`, `desktop/run_desktop.sh`, `desktop/build_deb.sh`; project has no pre-existing dependency manifest (a direct-dependency manifest is added in this phase), automated tests, or successful runtime/package result |
| Windows desktop prototype | C++20, Visual Studio `.vcxproj`, Win32/Windows DNS APIs, Winsock, Media Foundation, Direct3D 11, C++/WinRT header | `windows/PhoneDock.App/*`; console entry point and several partial components; no Visual Studio solution, package manifest, successful build, GUI shell, or runtime verification |
| Windows driver prototype | UMDF-related `.vcxproj`; Windows-only declarations in `PhoneDock.Common/Public.h` | `windows/PhoneDock.Driver/PhoneDock.Driver.vcxproj`, `windows/PhoneDock.Common/Public.h`; project file has no implementation source. The configured project GUID also contains non-hexadecimal characters and needs repair before it is treated as a buildable project |
| iOS app | None found | No Swift/SwiftUI source, Xcode project/workspace, package manifest, or iOS assets |
| macOS app | None found | No Swift/SwiftUI source, Xcode project/workspace, package manifest, or macOS assets |
| Web application/site | None found | No HTML/CSS/JS/TS application, package manifest, framework configuration, or website source |
| Shared components | No cross-platform protocol/core package | `windows/PhoneDock.Common/Public.h` is Windows-only; Android, Linux, and Windows networking implementations are separate |
| Tests and CI | No pre-existing test source, test directory, workflow, PR template, or dependency automation found | Android declares JUnit/Espresso dependencies but has no test source and no product behavior test suite exists. Phase 0 adds repository checks and standard-library tests for release-tag/changelog validation; an actual GitHub Actions pass is distinct from local YAML parsing |

## Feature inventory

Statuses below describe repository evidence, not product aspirations. “Verified” means the relevant behavior was actually exercised; merely finding source code is not verification.

| Feature/component | Status | Evidence / limitation |
|---|---|---|
| Android app entry point and Compose UI | **Prototype or mockup** | `MainActivity.kt`, onboarding and dashboard screens are real UI code. Onboarding copy advertises capabilities not implemented. The dashboard uses default values such as “Unknown” and “No PC Detected”; settings is a TODO. |
| Android project/build configuration | **Implemented but not verified** | Gradle wrapper, app module, version catalog and manifest exist. This sandbox lacks Java and an Android SDK, so no Gradle build completed. This phase adds missing direct Compose icon/ViewModel dependencies and previously referenced onboarding palette values, but cannot claim build success. |
| Android screen capture and AVC encoding | **Partially implemented** | `ScreenStreamer.kt` configures a MediaProjection virtual display and AVC encoder and calls a frame callback. `ConnectionService.kt` sends encoded buffers when a client is present. No Android device, codec, lifecycle, rotation, or receiver test was available; output-format/configuration and lifecycle handling need review. |
| Android discovery and TCP listener | **Implemented but not verified** | `NsdHelper.kt` registers `_phonedock._tcp`; `ConnectionService.kt` binds an ephemeral `ServerSocket` and accepts connections. The listener accepts clients without pairing/authentication and does not implement a protocol handshake. |
| Linux onboarding/discovery interface | **Prototype or mockup** | `desktop/onboarding_view.py` and `main.py` create real widgets but include nonfunctional/aspirational copy and placeholder states. |
| Linux mDNS/DNS-SD discovery | **Implemented but not verified** | `desktop/discovery.py` browses `_phonedock._tcp.local.` with `zeroconf` and emits addresses. No network/hardware test was performed; IPv4 is selected and update handling is empty. |
| Linux TCP receive and H.264 rendering path | **Partially implemented** | `desktop/connection.py` parses a length/type prefix; `desktop/video_view.py` uses PyAV and a Qt image widget. There is no integration test. The `QThread` subclass does not override `run`, so its decoder slot/thread affinity should be reviewed before calling decoding asynchronous. |
| Linux input/remote-control path | **Partially implemented** | `VideoView` emits normalized mouse events and `main.py` serializes them; `ConnectionManager.send_input` sends type 2. The Android service never reads input messages and no input injection implementation exists. |
| Windows DNS-SD/client receive | **Implemented but not verified** | `Discovery.cpp` browses services and `SessionClient.cpp` opens a TCP socket and receives a length/flag/payload shape. There is no Windows build or runtime result; socket reads assume full header reads and sizes are not bounded. |
| Windows H.264 decode/render | **Prototype or mockup** | `VideoDecoder.cpp::Decode` and `Renderer.cpp::Present` are TODOs. No complete media pipeline or display window exists. |
| Windows display driver / Android second display | **Prototype or mockup** | `PhoneDock.Common/Public.h` contains GUID/IOCTL declarations and the driver project file exists, but no driver source or working display extension was found. Android onboarding only illustrates/promises the goal. |
| Clipboard, file transfer, transfer inbox/history, links/content handoff, notification forwarding, media controls, trusted-device management, diagnostics/performance telemetry | **Planned but not found** | No implementation or tests found. A foreground-service status notification is not notification forwarding. |
| USB connectivity, manual host/IP connection, automatic reconnection, authenticated pairing/trust | **Planned but not found** | Existing prototypes use local DNS-SD discovery and a TCP connection only; no USB adapter, manual connection UI, pairing, authentication, persistent identity, or reconnect state machine was found. |
| iOS, macOS, and web product experiences | **Planned but not found** | No project source or platform configuration exists. |

## Existing protocol and architecture evidence

- Android advertises the `_phonedock._tcp` DNS-SD type and selects a dynamic TCP port (`NsdHelper.kt`, `ConnectionService.kt`).
- Linux browses `_phonedock._tcp.local.` (`desktop/discovery.py`). Windows browses `_phonedock._tcp.local` (`windows/PhoneDock.App/Discovery.cpp`). These are signs of an emerging convention, not proof of tested interoperability.
- Android writes a four-byte big-endian length followed by one key-frame flag and payload (`ConnectionService.sendFrame`). Windows reads a four-byte network-order length plus one flag; Linux parses a four-byte network-order length plus a one-byte type. The field meanings, payload caps, codec-configuration handling, and version negotiation are not specified.
- Linux sends a type-2 input message, but Android's client handler does not read from the socket. Windows has no input sender/receiver.
- `windows/PhoneDock.Common/Public.h` defines `PDP_VERSION_MAJOR 0`, `PDP_VERSION_MINOR 1` and a default port `45124`; those constants are not used by the Android dynamic-port service and are not a negotiated protocol.
- No versioned wire specification, pairing flow, key exchange, encryption, error frame, heartbeat, capability negotiation, shared identity model, or cross-platform common library was found.

These observations are documented without choosing a final protocol in [PROTOCOL.md](PROTOCOL.md).

## Build and test commands

Commands below are based on the checked-in configuration. A command being documented is not evidence that it has succeeded.

### Android

```bash
cd android
./gradlew --no-daemon testDebugUnitTest lintDebug assembleDebug
```

Requires a JDK compatible with AGP 8.7 (JDK 17 is the CI choice) and Android SDK platform/build tools for the configured API level 35. `android/local.properties` previously contained a developer-specific absolute SDK path; it was removed and is now ignored. Set `ANDROID_HOME`/`ANDROID_SDK_ROOT` or a local ignored `local.properties` for a local SDK. No Android unit or instrumentation test source was found.

**Observed local result:** `./gradlew --no-daemon tasks --all` stopped before Gradle started because no `java` executable/`JAVA_HOME` is available. The Android SDK is also absent. No Android build result is claimed.

### Linux desktop

```bash
cd desktop
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -m compileall -q .
./run_desktop.sh
```

The runtime dependencies are directly pinned in `desktop/requirements.txt`; transitive dependencies are not yet represented in a resolver-generated lockfile. A desktop session and working display/network environment are required for an interactive/hardware check. The launcher expects `desktop/venv` specifically.

The existing Debian packaging script is a prototype. It expects PyInstaller installed in that `venv`, `dpkg-deb`, and execution from `desktop/`; its package metadata/version and launcher/icon integration need maintenance before a release artifact is treated as product-ready.

**Observed local result:** `python -m pip install -r desktop/requirements.txt`, `python -m pip check`, top-level dependency imports, Python compilation, and shell syntax checks pass in the ignored sandbox virtual environment. Importing Qt widgets/starting the offscreen UI is blocked because the host is missing `libGL.so.1`; an attempt to install the OS library could not reach the Debian package mirrors. The GitHub Linux runner job includes a short offscreen UI smoke check, but its result must be read from Actions. No physical-device/network workflow or existing Python unit test was verified.

### Windows

From a Visual Studio Developer PowerShell with the C++ workload, Windows SDK, and Media Foundation headers/libraries:

```powershell
msbuild windows\PhoneDock.App\PhoneDock.App.vcxproj /m /p:Configuration=Release /p:Platform=x64 /p:AppxPackage=false
```

The Windows runner in CI attempts this application project. The separate driver project is excluded because it has no source implementation and requires the Windows Driver Kit (WDK). Neither project has been built locally; this audit environment is Linux and has no MSBuild/Windows SDK.

### iOS, macOS, and web

No build/test command exists because those applications and build configurations were not found. Xcode and Apple SDK availability are later prerequisites, not evidence of an existing app.

### Repository checks added by Phase 0

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q desktop scripts tests
bash -n desktop/run_desktop.sh desktop/build_deb.sh
```

The repository checker validates required documentation, local Markdown links/anchors, and parseability of checked-in XML project/resource files. It does not replace platform builds, runtime tests, a Markdown style linter, or a security scanner.

## Build failures and environment limitations

- **Android:** Gradle wrapper could not start: Java/JAVA_HOME missing. Android SDK path from the tracked baseline (`/home/emerald/Android/Sdk`) was not present; that local-only file is removed in this phase. Full Gradle build/lint/unit test remains pending on CI or a configured Android environment.
- **Linux runtime:** PySide6, PyAV, and Zeroconf were absent from the base interpreter. This phase pins direct dependencies; installation, `pip check`, top-level dependency imports, Python compilation, and shell syntax checks pass in an ignored virtual environment. Importing Qt widgets/offscreen startup is blocked by missing host `libGL.so.1`; the attempted OS-package install could not reach Debian mirrors. No device/network peer or Debian package was available for a runtime test.
- **Windows:** no Windows host, MSBuild, Visual Studio, Windows SDK, Media Foundation runtime, or WDK is available locally. CI is configured to try the application project; driver build remains blocked by missing source/WDK.
- **Apple/web:** no source to build; Xcode is unavailable on this Linux environment; no web project exists.
- **Tests:** no application unit/integration/hardware test source existed at baseline. Android build dependencies declare JUnit/Espresso but no tests were found. Phase 0 adds standard-library unit tests for the tag/changelog validation helper only; those are repository-policy tests, not PhoneDock product-feature tests.
- **CI workflow results:** all added workflow/Dependabot YAML parses locally with PyYAML 6.0.3. `actionlint` could not be downloaded because this environment cannot reach GitHub release assets. Initial PR run [36648554925](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36648554925) passed repository/documentation/source checks and the separate GitGuardian check, but failed the Linux desktop dependency-import, Android Gradle, and Windows C++ jobs. GitHub's Actions log archive downloads returned EOF from this sandbox, so the exact Android/Windows build diagnostics could not be inspected. Follow-up changes add the Linux Qt runtime libraries found missing by local `ldd` inspection, correct Windows DNS-SD IPv4 conversion and declare its SDK/link dependencies, and upgrade pinned Actions to Node 24 releases. The Android/Windows job summaries now retain failure tails. The follow-up CI run is pending; these fixes are not yet build-verified. YAML parsing is not semantic workflow validation or a successful Actions run.

## Important technical debt and risks

1. **Unauthenticated network listener.** Android accepts clients on a TCP listener and streams screen data without an authenticated handshake or transport encryption. Treat this prototype as unsafe on untrusted networks; do not expose it beyond a trusted development network.
2. **No documented protocol.** Similar frame prefixes have independently evolved in Android, Linux, and Windows, while message behavior differs. A future protocol must bound lengths, define byte order/fields, negotiate capabilities and versions, and specify authentication/error handling before adding features.
3. **No message-size limits.** Desktop/Windows receivers accept peer-supplied lengths without a documented cap. Android schedules frame writes asynchronously; backpressure and lifetime behavior need review.
4. **Incomplete/unstable service lifecycle.** Android projection, encoder, foreground service, sockets, NSD, and UI state are not coherently bound; `ConnectionService` tracks one `activeClient` while continuing to accept sockets and schedules a coroutine for each encoded frame without an explicit bounded backpressure policy. Stream buffers, codec configuration/offset handling, MediaProjection callbacks, rotation and cleanup need testing.
5. **Misleading UI copy and mock state.** Android and Linux onboarding mention control, clipboard, transfers, and second-display behavior that is not implemented. Dashboard state is not sourced from `ConnectionService`.
6. **Duplicate platform implementations.** Discovery and transport framing are separately implemented with no shared tests or spec. Do not create a shared package until a suitable portable boundary and language are selected.
7. **Windows scaffolding is incomplete.** `Decode`/`Present` are TODOs, the entry point is a console program, the driver project has no source and a malformed GUID, and receive logic has reliability concerns.
8. **Linux dependency/packaging maintenance.** A direct dependency manifest was added; a complete lock, product test suite, and corrected packaging metadata are still absent. `desktop/main.py` repeats imports and defines `on_mouse_event`/`closeEvent` twice; the later definitions shadow the earlier ones. The synchronous connect call runs from the UI path, and the decoder thread/slot affinity needs correction or proof before claiming background decoding.
9. **Environment-specific configuration.** A tracked absolute Android SDK path was removed. Local SDK configuration must remain ignored.
10. **Asset/identity inconsistency.** Android and Linux prototypes use an older cream/coral/dark-green “Harvst” palette; Android launcher resources are the default Android template icon. No approved PhoneDock logo/design tokens were found.
11. **Version/release ambiguity.** Android and Linux source contain `1.1.0` strings and the Windows header contains PDP `0.1`; no Git tags or release history were present. These are not evidence of a published product release.
12. **License attribution requires maintainer review.** `LICENSE` contains MIT license text but the copyright line still includes template wording (`NACOS OAU (or your name)`). This phase does not alter the file or make a legal determination; resolve attribution before making public licensing claims.

### Dependency, generated-file and configuration review

- Android pins AGP 8.7.2, Kotlin 2.0.21, Gradle 8.9, and Compose BOM 2024.11.00. These pins warrant a support/security review against the current Android toolchain; no upgrade or advisory audit was attempted because this environment cannot run Gradle. The repository has no Gradle dependency lock and the wrapper properties contain no distribution checksum. The app Gradle file also references `proguard-rules.pro`, which was not found in the app tree; verify release configuration even though minification is currently disabled.
- This phase adds direct Python runtime pins (`PySide6` 6.11.2, PyAV 18.1.0, `zeroconf` 0.151.5) after inspecting the app imports. The PySide6 x86_64 wheel selected during the sandbox check requires glibc 2.34 or newer; other architectures/distros are unverified. Pip resolves transitive dependencies but no full resolver lockfile is committed; create/review one before relying on reproducible production packaging.
- GitHub Actions are pinned to immutable commit SHAs for checkout/setup actions and Dependabot is configured for GitHub Actions, Gradle and pip updates. No automated secret-scanning workflow or repository-level secret-scanning result is asserted; local pattern checks are limited.
- No compiled app/package artifact was tracked at baseline. Android launcher WebP/vector files are app resources; the Gradle wrapper JAR is a build-tool wrapper component. Local `__pycache__` files created by checks are ignored and not tracked.
- The baseline tracked `android/local.properties` contained a machine-specific absolute SDK path, not a credential; it is removed and the filename is ignored. No credential/private-key pattern was found by the limited scan described below; this does not validate full history or GitHub settings.

## Duplicate or conflicting architecture

- Android uses platform NSD and Java TCP sockets; Linux uses Python `zeroconf` and Python sockets; Windows uses DNS API and Winsock. No shared core or test vectors exist.
- Android/Linux/Windows contain similar but undocumented length-prefixed stream framing, with a flag/type byte. The Windows-only header separately advertises PDP v0.1 and port 45124 while Android binds a dynamic port.
- Android UI has one theme palette while parts of the onboarding use a different legacy palette; the onboarding claims Windows-specific capabilities despite the Android app's broader target.
- The README product vision and onboarding copy describe planned features; source evidence does not support treating those as implemented.

## Security review items

- Define a threat model and pairing/authentication flow before allowing remote sessions.
- Require authenticated, encrypted sessions and robust replay/session handling; select vetted platform/library primitives rather than designing cryptography.
- Bound frame/message sizes and queues; handle partial reads, timeouts, reconnects, and resource exhaustion.
- Review wildcard socket binding, firewall/network exposure, NSD metadata, permission prompts, foreground-service lifecycle, and Android backup policy.
- Confirm Android screen capture remains explicitly user-consented and revocable; do not add input injection or notification access without explicit UX/permission boundaries.
- Keep clipboard text, notification content, files, tokens, private keys, and pairing material out of logs.
- Add transfer path/overwrite protections and integrity checks before implementing file transfer.
- No credential/private-key pattern was found in the tracked source during the limited local scan; this is not a substitute for GitHub secret scanning or a full history scan. The shallow history limits historical scanning.

See [SECURITY.md](SECURITY.md) for the security baseline and open items.

## Documentation, compatibility, and support gaps

At baseline there was no developer setup guide, audit, product requirements document, architecture description, protocol specification, platform support matrix, testing policy, design system, roadmap, contribution guide, release/changelog policy, issue templates, PR checklist, CI, or dependency-update configuration. The root README was the only detailed documentation and mixed future requirements with current repository state.

Compatibility is not verified on any physical Android device or supported Linux distribution. Android declares `minSdk 26`, `targetSdk 35`, `compileSdk 35`, Java 11 bytecode, AGP 8.7.2/Kotlin 2.0.21; there is no device/OS test matrix. Windows targets x64 in the app project and references VS toolset v143/Windows APIs, but no build or supported Windows version has been verified. No Apple/browser compatibility matrix can be asserted without implementations.

## Phase 0 changes and follow-up

This phase preserves the Android, Linux, and Windows source and existing Android image/vector assets. It adds repository-aware product/engineering docs, an explicit feature-status vocabulary, local documentation/XML checks, platform-appropriate CI attempts, a source-only draft release workflow, dependency/update and contribution templates, direct Linux runtime dependencies, and `.editorconfig`/ignore hygiene. It removes only the developer-specific tracked `android/local.properties` path and makes the missing Android palette/dependency declarations explicit; it also adds Windows header self-sufficiency/include-order fixes as preparation for the Windows CI build.

Recommended next steps:

1. Resolve Phase 0 CI results on GitHub; fix any regression before merging.
2. Confirm the license attribution and decide whether the existing license text/holder is intentional.
3. Run Android build/lint on CI and test projection, NSD, lifecycle, and screen capture on supported hardware.
4. Run the Windows application build; separately decide whether the display-driver project is viable before repairing/building it.
5. Build a repeatable Linux development environment and replace misleading packaging metadata before any artifact is distributed.
6. Select the protocol and security design through explicit ADRs, after comparing the existing frame code and actual platform constraints.
7. Design pairing/device identity and testable session states before expanding connection features.
8. Only then implement additional features/platform projects; keep iOS, macOS, web, and shared-core choices evidence-led.

The detailed sequence and completion criteria are in [ROADMAP.md](ROADMAP.md).

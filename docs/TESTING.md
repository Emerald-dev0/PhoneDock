# Testing and verification

PhoneDock is not considered reliable because it compiles or because a UI looks plausible. Tests must be appropriate to the claim: unit behavior, protocol interoperability, platform lifecycle, and real-device performance are different kinds of evidence. Status rules are in [FEATURE_STATUS.md](FEATURE_STATUS.md); current platform gaps are in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md).

## Baseline

At the audited baseline no application test source or cross-platform test suite was found. Android declares JUnit and Espresso dependencies but has no test files. Linux has no product-feature test suite. Windows has no test project. Phase 0 adds standard-library unit tests for the release-tag/changelog validator plus repository/documentation validation and CI build/test commands; those policy tests do not validate PhoneDock app behavior. A Gradle test task with zero tests is not evidence of behavior.

## Test levels

1. **Static/repository checks:** documentation links and required files, XML project/resource parseability, Python syntax, shell syntax, formatting/lint only where configured. These catch source/repository defects but do not execute the app.
2. **Unit tests:** pure state transitions, parsers, capability filtering, file-name/size validation, clipboard loop prevention, metrics and view-model behavior. Keep OS APIs behind testable boundaries.
3. **Protocol/component integration:** language-independent vectors for version/envelope parsing; bounded input and malformed-message tests; discovery/transport/session integration with fake peers; transfer checksums and cancellation.
4. **Platform tests:** Android permission/service lifecycle and Compose UI; Linux Qt behavior and package checks on declared distributions; Windows build and Media Foundation/render path; native iOS XCTest/XCUITest on macOS and the official iOS Simulator when the Phase 4 app exists; web browser/accessibility tests when source exists.
5. **Hardware/network tests:** named real Android devices and host hardware, real Wi-Fi/USB, codec and display behavior, network interruption, sleep/resume, thermal/battery and sustained-use behavior. Record exact OS, device, network, build and result.

Mocks can isolate dependencies in unit tests but must not be presented as evidence that the real feature is integrated.

## Current local commands

From the repository root:

```bash
python3 scripts/check_repository.py
python3 -m compileall -q desktop
bash -n desktop/run_desktop.sh desktop/build_deb.sh
```

Android (JDK 17 and Android SDK platform/build tools API 35 required):

```bash
cd android
./gradlew --no-daemon testDebugUnitTest lintDebug assembleDebug
```

Linux desktop (Python 3 and a display/network environment for interactive use):

```bash
cd desktop
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -m pip check
venv/bin/python -m compileall -q .
./run_desktop.sh
```

Windows application (Visual Studio Developer PowerShell, C++ workload, Windows SDK):

```powershell
msbuild windows\PhoneDock.App\PhoneDock.App.vcxproj /m /p:Configuration=Release /p:Platform=x64 /p:AppxPackage=false
```

No iOS, macOS desktop, or web build command exists today because those projects are absent. The developer's Linux Mint laptop can handle source/design/protocol work, repository checks, and portable test fixtures. Pure Swift packages can be tested on Linux only if a compatible Swift toolchain is available and the package avoids Apple-only frameworks; Linux Swift is not Xcode and cannot build SwiftUI/iOS targets or run the official iOS Simulator. Phase 4 plans official Simulator CI on a hosted macOS runner after a real iOS project and repeatable test command exist. Phase 9 is a separate macOS product target. No custom iOS emulator will be built. The Windows driver project is not in the build command: it has no implementation source and needs a WDK-equipped, signed test plan.

## Continuous integration

`.github/workflows/ci.yml` runs on pull requests, pushes to `main`, manual dispatch, and reusable workflow calls. It uses least-privilege read permissions, bounded job timeouts, cancellation for superseded CI, and immutable pinned action commits. Current checks are:

- documentation/repository checker, standard-library release-policy unit tests, Python syntax, and shell syntax on Linux;
- Python/Linux dependency installation, Qt/PyAV/Zeroconf imports, source syntax, and a short offscreen UI smoke check;
- Android unit-test task, lint, and debug assembly on Linux with JDK 17 and the runner's Android SDK;
- Windows application C++ build on a Windows runner.

There is no iOS/macOS-app CI job yet because no Apple app project/scheme exists; no web job because no web project exists; and no driver job because implementation sources/WDK configuration are absent. Phase 4 will add iOS Simulator CI only with a real Xcode app/test target and repeatable command; Phase 9's macOS product needs its own target and test evidence. The macOS runner used by iOS CI does not implement/test a macOS PhoneDock app by itself. Expand other matrix entries only when a real project and repeatable command exist. CI YAML/static parsing locally is not an Actions run; report the run/check state separately.

The Android JUnit/Espresso tasks currently have no test source. CI therefore verifies build/lint and task configuration but does not validate feature behavior. The Linux job verifies dependency resolution/imports, syntax, and a short offscreen UI construction/event-loop smoke; it does not verify interactive GUI behavior, mDNS reachability, H.264 hardware behavior, or packaging. The Windows job validates only the app project build, not video output, network behavior, or the driver.

## Planned iOS verification — Phase 4 (not configured or run)

There is no iOS app, Xcode project/scheme, macOS iOS-CI job, Simulator result, or physical-device result. This is a plan, not an assertion that any Apple check exists or has passed. The canonical phase dependencies, API/policy matrix, signing boundary, and not-started borrowed-iPhone checklist are in [ROADMAP.md](ROADMAP.md) and [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md).

**Verified toolchain snapshot (2026-10-01; recheck at Phase 4 kickoff):** the public repository can use GitHub's standard hosted `macos-26` runner (Apple silicon; `macos-26-intel` is also listed). The current `macos-26` runner-image readme lists stable Xcode 26.6, the iOS 26.5 SDK/Simulator runtime, and installed iPhone Simulator devices. Apple's Xcode requirements list the Swift 6.3 compiler with Xcode 26.6. Xcode 27 is a public preview and iOS 27 APIs are beta at this snapshot, so they are not the required CI baseline. Candidate baseline: `macos-26`, explicitly select Xcode 26.6, and test an installed stable iOS 26.5 Simulator destination; update this only after checking GitHub's current image and Apple's compatibility matrix.

When the real Swift/SwiftUI project begins:

- Use a least-privilege macOS Actions job (`contents: read`, bounded timeout, pinned actions, checkout without persisted credentials). Avoid `macos-latest`; the image label is mutable, so log its image version and explicitly select/assert the stable Xcode path.
- Log `xcodebuild -version`, `swift --version`, `xcodebuild -showsdks`, `xcrun simctl list runtimes`, and the available iOS simulator destinations. Fail clearly if the selected stable runtime is missing. Keep these logs and the actual test command with the result.
- Run XCTest for state transitions, validation, capability negotiation, protocol fixtures, and security/error paths. Use XCUITest for practical launch, navigation, accessibility identifiers, settings, empty/error states, and permission-denial/recovery behavior that the simulator exposes. Keep discovery/protocol/state boundaries injectable for deterministic unit tests.
- A future command template for the reviewed snapshot (not runnable until the project/scheme exists) is:

  ```bash
  set -o pipefail
  RESULT_DIR="$(mktemp -d "${RUNNER_TEMP:-${TMPDIR:-/tmp}}/phonedock.XXXXXX")"
  xcodebuild \
    -project ios/PhoneDock.xcodeproj \
    -scheme PhoneDock \
    -destination 'platform=iOS Simulator,name=iPhone 17,OS=26.5' \
    -resultBundlePath "$RESULT_DIR/PhoneDock.xcresult" \
    CODE_SIGNING_ALLOWED=NO \
    test 2>&1 | tee "$RESULT_DIR/xcodebuild.log"
  ```

  Recheck project/scheme/destination names against the selected image at implementation time. Use the same documented command locally on macOS and CI.
- In the workflow, upload the `xcodebuild` log and `.xcresult` bundle on failure using a separately pinned artifact action/step that still runs after the test command fails; apply short retention and do not include secrets or user data. Simulator builds should not need a distribution certificate or App Store Connect credentials; never expose any signing secret to untrusted PR code.
- Label results **macOS/iOS Simulator CI**, never physical-device verified. Simulator can verify compilation, app/unit/state tests, protocol fixtures, navigation/layout, and practical UI automation on that runtime. It cannot establish real Wi-Fi/Bonjour/multicast, device permission prompts across hardware, peer interoperability, cable/accessory behavior, sustained background execution, screen-capture quality, battery, or thermal performance.
- A physical-device test also needs an authorized iPhone, a compatible peer, and a legitimate signed install path. A hosted macOS runner is not a USB-connected iPhone lab. Until the borrowed-device checklist is actually performed, iPhone evidence remains **Not started**.

No Apple CI job is added by this documentation-only change because no real Xcode project, scheme, or repeatable test command exists. The official iOS Simulator runs on macOS; it does not run on Linux and PhoneDock will not build a custom emulator.

## Required failure and resilience coverage before features ship

### Pairing, protocol and network

- Unknown peer, invalid identity, expired/replayed pairing proof, revoked peer and version mismatch.
- Malformed/short headers, partial TCP reads/writes, oversized lengths, unsupported message type, invalid capability and timeout.
- Two peers on multiple interfaces; IPv4/IPv6 decisions; service found/removed/renamed; address change; multicast blocked; manual entry failure.
- Disconnect during authentication, streaming and transfer; cancellation; reconnect after sleep/resume; no reconnect after revocation.
- Backpressure and bounded queues under slow receivers; process/service cleanup and concurrent client policy.

### Capture, permissions and lifecycle

- User denies/ends MediaProjection, permission revoked, app process killed, service restarted, display rotation/resolution change, screen locked and device sleeps.
- Unsupported encoder/codec configuration, codec format change, network loss, missing key frame, decode failure, renderer/device loss and resource cleanup.
- Remote-control permission/setup absent, user stops sharing, invalid coordinates/rates and input cancellation.

### Transfer and privacy

- Small, empty and large files; exact checksum; duplicate names; destination permissions; unsafe paths; disk full; cancellation, disconnect, retry/resume policy and partial-file cleanup.
- Clipboard direction toggles, duplicate/loop prevention, limits, unsupported types, permission/lifecycle behavior and content never appearing in standard logs.
- Notification filtering/permission revocation and media availability; private content absent from logs/diagnostic export.

### UI, accessibility and release

- Loading, empty, permission-denied, connecting, failed, reconnecting and disconnected states reflect real service state.
- Keyboard and screen-reader operation, large text, contrast in light/dark themes and reduced motion.
- Clean build in a fresh environment; dependency/license/security review; signed artifact verification only where signing is configured; checksum and provenance for published binaries.

## Reporting test results honestly

Every completion report lists command, environment, outcome and scope. Distinguish:

- **passed:** command ran and relevant assertions/build succeeded;
- **failed:** command ran and reported failure, including baseline versus regression where known;
- **blocked:** did not run because a named SDK, credential, hardware, OS or service was unavailable;
- **not applicable:** no project/feature exists yet.

Do not call syntax checks a test suite, local YAML parsing a GitHub Actions success, a compile a runtime test, a mock a hardware test, or source presence a supported platform. Attach a CI run/check and real-device evidence for claims that require them.

## Phase 0 verification record

In the audit sandbox, `python3 scripts/check_repository.py` passed (required files, local Markdown links/anchors, XML project/resource files and Android TOML catalog); Python compilation, shell syntax, installation of the pinned Linux direct dependencies, `pip check`, and top-level dependency imports passed. A Qt offscreen UI smoke attempt was blocked by missing system `libGL.so.1`; the Debian mirror was unreachable from this environment. All workflow/Dependabot YAML files parsed with PyYAML 6.0.3; `actionlint` could not be downloaded from GitHub release assets. These are local syntax/static checks, not a GitHub Actions result.

The audit environment has no Java/Android SDK or Windows/MSBuild toolchain, so Android/Windows builds were not run locally. No physical devices were available and there was no baseline unit/integration test suite.

Initial PR CI runs [36648554925](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36648554925), [36649242392](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36649242392), [36649688990](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36649688990), and [36650248646](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36650248646) exposed failures in Qt imports/UI construction, Windows DNS-SD compilation, and Android lint. The code and CI setup were corrected; run [36650681493](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36650681493) passed the configured jobs at that point. The latest verified PR run, [36652649534](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36652649534), also passes the existing repository/source checks, Linux dependency imports and offscreen UI smoke, Android lint/debug assembly, and Windows x64 Release build; GitGuardian passes. The Android test task contains no app test sources; the Windows result is compile-only; the Linux smoke does not exercise a real session/network/device. Local Android/Windows builds remain blocked by absent toolchains and local Qt offscreen startup by missing `libGL.so.1`. `actionlint` could not be downloaded, but all workflows and Dependabot YAML parsed with PyYAML and GitHub accepted/executed the workflows. No iOS, macOS-app, or real-device result is claimed.

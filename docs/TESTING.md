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

No iOS, macOS desktop, or web build command exists today because those projects are absent. Phase 4 plans to add the iOS app and simulator CI on macOS/Xcode; no iOS Simulator runs on Linux and no custom emulator will be built. The Windows driver project is not in the build command: it has no implementation source and needs a WDK-equipped, signed test plan.

## Continuous integration

`.github/workflows/ci.yml` runs on pull requests, pushes to `main`, manual dispatch, and reusable workflow calls. It uses least-privilege read permissions, bounded job timeouts, cancellation for superseded CI, and immutable pinned action commits. Current checks are:

- documentation/repository checker, standard-library release-policy unit tests, Python syntax, and shell syntax on Linux;
- Python/Linux dependency installation, Qt/PyAV/Zeroconf imports, source syntax, and a short offscreen UI smoke check;
- Android unit-test task, lint, and debug assembly on Linux with JDK 17 and the runner's Android SDK;
- Windows application C++ build on a Windows runner.

There is no iOS/macOS CI job yet because no Apple app project exists; no web job because no web project exists; and no driver job because implementation sources/WDK configuration are absent. Phase 4 will add the iOS job with a real Xcode project and repeatable simulator command. Expand other matrix entries only when a real project and repeatable command exist. CI YAML/static parsing locally is not an Actions run; report the run/check state separately.

The Android JUnit/Espresso tasks currently have no test source. CI therefore verifies build/lint and task configuration but does not validate feature behavior. The Linux job verifies dependency resolution/imports, syntax, and a short offscreen UI construction/event-loop smoke; it does not verify interactive GUI behavior, mDNS reachability, H.264 hardware behavior, or packaging. The Windows job validates only the app project build, not video output, network behavior, or the driver.

## Planned iOS verification — Phase 4 (not configured or run)

There is currently no iOS app, Xcode project/scheme, macOS CI job, simulator test result, or physical-device result. The following is a plan, not a claim that these checks exist or have passed. The detailed app scope, API/policy investigation, signing prerequisites and canonical borrowed-iPhone checklist live in [ROADMAP.md](ROADMAP.md).

When the real Swift/SwiftUI project begins:

- Add a least-privilege GitHub Actions job on an available macOS runner with its installed Xcode/iOS SDK and official iOS Simulator. At phase kickoff, verify the runner image, Xcode version, simulator runtime and destination; record those versions so results are reproducible.
- Run Xcode build and XCTest on a simulator destination. Add XCUITest smoke coverage for app launch, device-list and pairing/session navigation, settings, accessibility identifiers, and practical permission-denied/recovery states. Keep protocol, discovery and state logic injectable so unit tests can use deterministic fakes.
- Simulator CI can check Swift compilation, unit/state logic, view integration, navigation, layout and basic UI automation without a personal Mac or iPhone. Label the result **macOS/iOS Simulator CI**, never physical-device verified.
- Use simulator builds that do not require distribution credentials where the selected Xcode setup allows it. Never expose Apple signing secrets to untrusted pull-request code. Confirm the current signing/provisioning requirements separately before installing on a borrowed iPhone or distributing an app.
- Do not infer real Wi-Fi/Bonjour/multicast reliability, device privacy-prompt behavior, inter-device interoperability, sustained background execution, capture/mirroring, battery or thermal performance from a simulator run. Those require the borrowed-iPhone checklist in the roadmap and a compatible peer.

The official iOS Simulator is supplied by Xcode on macOS. It does not run on this Linux environment; PhoneDock will not build a custom emulator. No Apple runner, Xcode project, simulator command, or iOS test suite is added by this documentation-only change.

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

Initial PR CI runs [36648554925](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36648554925), [36649242392](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36649242392), [36649688990](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36649688990), and [36650248646](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36650248646) exposed failures in Qt imports/UI construction, Windows DNS-SD compilation, and Android lint. The code and CI setup were corrected; run [36650681493](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36650681493) passes all configured jobs: repository/source checks, Linux dependency imports and offscreen UI smoke, Android lint/debug assembly, and Windows x64 Release build. GitGuardian also passes. The Android test task contains no app test sources; the Windows result is compile-only; the Linux smoke does not exercise a real session/network/device. Local Android/Windows builds remain blocked by absent toolchains and local Qt offscreen startup by missing `libGL.so.1`. `actionlint` could not be downloaded, but all workflows and Dependabot YAML parsed with PyYAML and GitHub accepted/executed the workflows. No real-device result is claimed.

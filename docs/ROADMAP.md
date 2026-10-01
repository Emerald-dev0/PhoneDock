# PhoneDock roadmap

This is PhoneDock's authoritative phase-by-phase plan—not a calendar promise. A phase is complete only when its deliverables and verification evidence exist. Status rules are in [FEATURE_STATUS.md](FEATURE_STATUS.md); current implementation evidence is in [PROJECT_AUDIT.md](PROJECT_AUDIT.md) and [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md); product acceptance criteria are in [PRODUCT_SPEC.md](PRODUCT_SPEC.md).

**Baseline as of 2026-10-01:** Phase 0 repository/CI foundation is complete for its stated scope, with PR review and merge still pending. Phases 1–3 have **not** delivered a finalized product architecture, interoperable protocol, pairing/authentication, or trusted session foundation. The Android, Linux, and Windows projects remain prototypes. There is no iOS or macOS app project, no web app/site source, and no iOS/macOS-specific CI job. A plan or API-feasibility label below is not implementation or verification evidence.

## Phase overview

| Phase | Objective | Depends on | Completion evidence |
|---|---|---|---|
| **0 — Repository recovery and engineering foundation** | Audit and preserve existing work; distinguish current from intended product; establish docs, contribution/status conventions, practical CI, and safe repository defaults. | None | Repository audit matches source; docs links/checks pass; existing CI jobs pass or are precisely documented as blocked; no unresolved regression is introduced. |
| **1 — Product, design, architecture and threat-model decisions** | Review requirements, visual direction, product boundaries, architecture options, privacy model, and threat model; approve only evidence-backed decisions. | Phase 0 | Reviewed product acceptance criteria; accessibility-reviewed design direction; threat model; ADRs for actual decisions; unresolved items explicitly listed. |
| **2 — Protocol and cross-platform engineering foundation** | Specify versioned discovery/session boundaries, stable device identity, capability negotiation, message limits, error model, fixtures, and maintainable platform interfaces. | Phase 1 security/architecture decisions | Reviewed protocol and executable conformance fixtures; malformed/oversized input is rejected; version mismatch is safe; no app advertises unimplemented compatibility. |
| **3 — Trusted local discovery and connection lifecycle** | Replace unauthenticated prototype sessions with explicit pairing, authentication, capability negotiation, status, cancellation, revocation, disconnect, and reconnect behavior. | Phase 2 protocol/security | End-to-end tests for existing Android/Linux targets and any desktop target that builds; real LAN discovery/pairing/revocation evidence on named versions; unknown peers cannot access sessions. |
| **4 — Native iOS companion** | Implement a real Swift/SwiftUI iPhone app for the iOS-supported subset, beginning with discovery, pairing/trust, session status, and settings. | Phases 1–3; an official macOS/Xcode build-and-test environment. **No personal Mac is required for simulator CI.** A borrowed iPhone is required only for physical-device evidence, not for starting source/design work. | Meaningful Xcode app and test targets; reviewed API/policy decisions; repeatable macOS CI build, XCTest, and practical XCUITest on official Simulator; physical-device claims gated on the not-started checklist below. |
| **5 — Android capture and desktop screen viewing** | Complete Android user-consented capture/AVC and at least one supported desktop receiver/render path; handle permission, lifecycle, orientation, backpressure, and recovery. | Phase 3 authenticated session | Real-device Android capture and named desktop receiver; permission/start/stop/rotation/background/network-loss tests; measured latency/resource behavior. |
| **6 — Supported remote control and USB** | Add capability-gated Android input and only those platform/device-specific USB or manual-connection flows proven feasible. | Phases 2–3 and 5; per-platform API/policy review | Setup/permission documentation; input mapping/cancellation tests; cable, permission, and recovery tests for every declared host/device combination. iOS input is not implied. |
| **7 — File transfer and content handoff** | Deliver user-selected file transfer, inbox, queue/progress/history, integrity checks, and explicit link/text/image handoff. | Phase 3 security/session; Phase 2 framing | Integrity and resilience suite for interruption, cancellation, large/empty files, duplicate names, and low storage; safe destination UX; no traversal/overwrite vulnerability. |
| **8 — Clipboard, notifications, media and device management** | Add opt-in clipboard sync, supported notification/media integration, persistent trusted-device management, transfer history, and diagnostics. | Phase 3 identity; relevant platform permission/API decisions; Phase 7 transfer metadata | Per-platform permission/revocation and privacy tests; persistent-state/multi-device tests; meaningful measured metrics. iOS support remains feature-by-feature and policy-gated. |
| **9 — Native macOS desktop app** | Build a distinct native Mac product; do not confuse the macOS runner used for iOS CI with a macOS PhoneDock app. | Phases 1–3; Phase 5 if the first Mac release includes Android screen viewing; Phases 7–8 only for features included in its scope. | Real macOS app target and user workflow; macOS-specific permissions, UI, security and lifecycle tests; physical-Mac evidence for any support claim. A successful iOS Simulator job alone does not satisfy this phase. |
| **10 — Web app and product website** | Publish maintained product/docs/release information and add only browser workflows supported by a reviewed security/permission model. | Phase 1 content/design; Phases 2–3 only if a browser client is approved. | Reproducible web build, accessibility and browser tests, and local-network/security review; no unsupported native-capability claims. |
| **11 — Android second-display mode** | Research and, only if justified, implement Android-as-display for named host operating systems. | Phases 1, 2, and 5; separate platform/driver research | Supported OS/device matrix; install/uninstall/recovery/security tests; real hardware evidence; maintainer decision that ongoing driver cost is justified. |
| **12 — Production hardening and releases** | Review security/privacy, accessibility, performance, dependency health, packaging, signing, crash handling, support, rollback, and distribution for each claimed app. | The relevant feature phases and approved launch scope | Release gate passes separately for every claimed platform; signed/notarized/store artifacts only with valid credentials; checksums/provenance and support/update behavior documented; no unresolved critical/high security issue. |

## Platform sequencing and responsibilities

- **Android:** the only phone-side implementation today. Stabilize permission handling, foreground-service/capture lifecycle, identity, transport, and capability reporting before input or other integrations. Use emulators plus named physical Android devices.
- **Linux desktop:** preserve the existing PySide6/PyAV prototype. Establish receiver tests, supported distribution packaging, and OS-specific networking; do not replace the framework without a reviewed migration case.
- **Windows desktop:** preserve the existing C++ project while determining whether it can become a viable desktop receiver/application. Keep the empty second-display driver scaffold separate; it is not an implemented driver.
- **iOS:** Phase 4 is a real native-app implementation phase immediately after shared protocol, trust, authentication, and session foundations. It does not wait for later Android-only capture, input, transfer, or clipboard phases. No Xcode project, iOS code, or iOS CI exists yet.
- **macOS desktop:** a separate native product phase (Phase 9), distinct from running iOS builds/tests on macOS. SwiftUI/AppKit or another native stack must be selected with a reviewed ADR before implementation; no Mac target exists today.
- **Web:** Phase 10 begins with useful accessible product/documentation/release pages. A browser-to-device client is a separate security and browser-capability decision, not a guaranteed port of native behavior.
- **macOS as build infrastructure:** official Xcode and iOS Simulator require macOS. The hosted runner is a practical CI route for a developer working from Linux; that runner, its simulator, and its build result are not an iPhone test or a macOS PhoneDock product.
- **Shared components:** none is established. Introduce portable code only after Phase 2 proves a stable boundary and language/toolchain fit. Protocol fixtures and reviewed interfaces can be shared without forcing identical native UI or platform APIs.
- **Design assets/tokens:** Phase 1 should reconcile prototype palettes and the default Android launcher icon with the proposed identity. Do not create unused token packages or replace existing assets without design review.

## Phase 4 — Native iOS companion

**Status: planned; implementation not started.** There is no iOS source, Xcode project/scheme, iOS CI job, simulator result, or iPhone test. Do not create an empty iOS placeholder before Phase 4. At kickoff, establish a real buildable application and test structure together with the first implemented workflows.

### Dependencies and first useful release

Phase 4 depends on actual Phase 1–3 deliverables—not just the existence of those headings:

1. Phase 1 must accept the iOS requirements, native interaction/accessibility design, threat model, and explicit product exclusions.
2. Phase 2 must provide a reviewed protocol/version/capability contract, test vectors, parser limits, and interoperable error behavior.
3. Phase 3 must implement a reviewed pairing ceremony, stable identity, authenticated/encrypted session lifecycle, capability negotiation, revocation, and safe connection-state semantics that the iOS adapter can consume.

These foundations are **not present today**. The iOS app must not invent a separate wire protocol or claim its own pairing/authentication is complete before the shared foundations exist. Phase 4 may develop UI concepts, Swift source that is independent of Apple frameworks, protocol fixtures, and tests with injected fakes while the foundations are being completed, but the integrated iOS workflow must wait for them.

The first useful iOS slice is a genuine app for a compatible peer: device list/discovery; readable peer identity; explicit approve/reject/revoke; truthful connecting/connected/disconnected/error status; user-controlled cancel/disconnect; supported privacy/connection settings; permission help; and privacy-safe diagnostics. Manual connection is included only if Phases 2–3 approve its protocol and security behavior. Transfer, clipboard, notification, media, capture, mirroring, input, USB, and background behavior are separate capability gates, not first-release assumptions.

### Implementation milestones

| Milestone | Work | Exit evidence |
|---|---|---|
| **4A — Entry gate and project** | Reconfirm Phases 1–3 artifacts and current Apple API/policy sources. Create the Xcode project, real app target/scheme, resource setup, XCTest target, and only the UI-automation/test structure needed by actual workflows. | A meaningful SwiftUI app—not an empty shell—builds and launches in the selected official simulator; project is reproducible from a clean checkout. |
| **4B — Native design and state model** | Implement accessible native navigation, app states, permission explanations, capability/unavailable states, and testable service boundaries. Keep connection state out of decorative/mock UI. | XCTest covers state transitions, validation, capability filtering, and failures; XCUITest covers launch/navigation and empty/error/settings states. |
| **4C — Integrated local workflow** | Connect the approved Phase 2–3 protocol/session adapter; request local-network access at the point of use; browse only the approved service type; present candidates as untrusted; complete explicit trust/session status and disconnect/revoke flows. | Deterministic protocol tests plus Simulator UI tests; end-to-end network evidence on a named physical iPhone and compatible desktop is still separately required for device-support claims. |
| **4D — Optional platform features** | Add a feature only when the feasibility matrix in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md) has a reviewed decision, exact minimum OS, required user consent/declarations, security review, and a test plan. Add capture extensions/targets only if the current API and distribution policy justify them. | Per-feature acceptance evidence and explicit fallback/exclusion; no Android-parity assertion. |
| **4E — Device validation and support decision** | Use the borrowed-iPhone checklist below only after there is a signed installable build and a compatible peer. Record exact models/OS/network and observed limits. | Physical checks are recorded as passed/failed/not run; only reviewed device/OS combinations become support claims. This milestone is **not started**. |

### Swift, native design, and Xcode structure

- Use **Swift and SwiftUI** for the native iOS presentation and Apple networking/security APIs selected during protocol implementation. Prefer native navigation, controls, typography, focus/accessibility behavior, and system appearance; do not transplant the Android layout.
- Use Apple-native **Liquid Glass-inspired** materials only on OS versions and controls that support them. Favor native system styling; use custom glass selectively, maintain legible content/control separation, respect increased contrast and reduced-transparency settings, and provide a clear opaque/standard-material fallback on older or accessibility-constrained configurations. The effect is not a brand substitute or a feature prerequisite.
- At Phase 4 kickoff, create a real `.xcodeproj` (or a reviewed workspace if dependencies require one), app target, scheme, source/resources, unit-test target, and UI-test target. Organize only code that exists—e.g. `App`, `Devices`, `Pairing`, `Session`, `Settings`, platform/network adapters, domain state, `PhoneDockTests`, and `PhoneDockUITests`. Add a ReplayKit/ScreenCaptureKit extension target only after its feature gate is approved.
- Keep platform-specific code behind testable boundaries. Fakes may make unit/UI tests deterministic, but a fake peer is not protocol interoperability evidence. Avoid a speculative shared package merely to mirror this folder outline.

### API and policy gate

The complete iOS per-feature classification, Apple references, current evidence, and boundaries are in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md). Recheck that matrix at Phase 4 kickoff and before every capability claim. Important current findings from the 2026-10-01 research snapshot:

- Apple documents local-network privacy controls for local TCP and Bonjour workflows. The app must explain access, declare the Bonjour service it browses/advertises, handle denial/revocation, and never equate discovery with identity.
- Apple documents CryptoKit and Keychain/Security APIs; their existence does **not** choose PhoneDock's protocol, pairing ceremony, key lifecycle, or secure storage policy. Those remain Phase 2–3 decisions.
- Apple documentation currently shows **ScreenCaptureKit for iOS 27** with a system content-sharing picker, but the iOS 27/Xcode 27 SDK line is beta at this snapshot. The current ReplayKit reference marks major recording/broadcast APIs deprecated in iOS 27. Treat screen capture as a user-mediated, version-gated investigation; do not base required support or CI on beta APIs. Reassess when the SDK and hosted image reach a stable supported release.
- Apple's current External Accessory reference material describes MFi-compatible accessories; it is not evidence of a general-purpose iPhone-to-PC USB socket. Do not promise generic USB.
- Do not promise software-injected system-wide remote input or access to notifications from arbitrary iOS apps through ordinary public APIs. Treat PhoneDock's own notifications and app-owned media separately.

### Development from Linux Mint without a Mac or iPhone

The developer's available computer is a Linux Mint HP EliteBook 840 G1, with no Mac or iPhone. Phase 4 is planned to remain viable in that environment:

- Linux can be used for product/API research, Swift source editing, UX/design work, protocol/interface design, language-independent fixtures, repository checks, and review of CI logs/results. A compatible open-source Swift Linux toolchain can also run tests for a deliberately platform-independent Swift package, subject to the actual Mint/Ubuntu base and toolchain support; see [Swift platform support](https://www.swift.org/platform-support/).
- Linux Swift is **not Xcode**. It cannot build the iOS app target against Apple's SDKs/SwiftUI, use `xcodebuild`, or run Apple's iOS Simulator. Do not build a custom emulator.
- Official Xcode/macOS CI performs the Apple-SDK build, XCTest, and Simulator UI tests once there is a real project and repeatable command. This does not require the developer to own a Mac.
- Simulator and mocks do not replace an iPhone. A physical validation later needs a borrowed/authorized iPhone **and** a feasible, appropriately signed installation path (for example, access to a Mac with supported Xcode or a separately reviewed distribution/test setup). A GitHub-hosted macOS runner is not a USB-connected iPhone lab.

### macOS CI and official iOS Simulator plan

**Verified runner/toolchain snapshot (2026-10-01; revalidate at Phase 4 kickoff):** this repository is public. GitHub's hosted-runner inventory lists the standard `macos-26` Apple-silicon runner and `macos-26-intel`; the current `macos-26` runner-image documentation lists stable Xcode **26.6** as the default, the iOS **26.5 SDK and Simulator runtime**, and installed iPhone simulator devices. Apple's Xcode system-requirements table lists Xcode 26.6's supported macOS range, iOS 26.5 SDK, and **Swift 6.3** compiler. GitHub labels Xcode 27 as public preview and Apple's iOS 27 SDK/API set is beta at this snapshot. Therefore, the initial required-CI candidate is a pinned `macos-26` label with an explicitly selected stable Xcode 26.6/iOS 26.5 simulator—not `macos-latest`, Xcode 27 beta, or an assumed future image. Exact runner/tool versions can change; confirm availability and costs for the repository at kickoff.

Official references: [GitHub-hosted runner inventory](https://docs.github.com/en/actions/reference/runners/github-hosted-runners), [macOS 26 runner-image software list](https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md), [Apple Xcode SDK/system requirements](https://developer.apple.com/xcode/system-requirements/), and [Apple iOS Simulator documentation](https://developer.apple.com/documentation/xcode/testing-your-app-in-simulator-or-on-a-device).

Once the real project, scheme, and repeatable test command exist, add a least-privilege macOS job to the existing CI without changing existing Android/Linux/Windows checks:

1. Use the stable `macos-26` label (or a newly verified stable replacement), `contents: read`, bounded job timeout, pinned actions, and checkout without persisted credentials. Record the GitHub runner image version from the setup log.
2. Select/assert the intended installed Xcode path. Log `xcodebuild -version`, `swift --version`, `xcodebuild -showsdks`, `xcrun simctl list runtimes`, and the available iOS simulator destinations; fail clearly if the required stable SDK/runtime is absent. Revalidate version compatibility using Apple's system-requirements page.
3. Run XCTest for pure state, validation, capability negotiation, protocol fixtures, and security/error paths. Use XCUITest for practical launch, navigation, accessibility identifiers, settings, empty/error states, and permission denial/recovery where the simulator can exercise it. Keep device/network dependencies injectable.
4. Run the same documented command locally on macOS and CI. A command template (not runnable until the project exists) for the verified snapshot is:

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

   At implementation time, confirm the project/scheme and simulator destination from the selected image; update the example rather than assuming those names persist.
5. Preserve `xcodebuild` logs and the `.xcresult` bundle on failure through a separately pinned artifact step that still runs after a test failure; use limited retention and no user data/secrets. Report image/Xcode/SDK/runtime versions and the exact command. CI establishes the reported Simulator scope only.
6. Add no iOS job to this documentation-only phase: there is no iOS project, scheme, or repeatable Apple test command yet. Do not add a fake job that only echoes tool versions or runs Linux-only Swift source.

**Simulator-testable:** app launch/build, Swift unit and state tests, protocol fixtures, UI navigation/layout, accessibility identifiers, and deterministic permission/capability branches. Simulator automation can test only the system behaviors it actually exposes; mocks are labeled as mocks.

**Requires a physical iPhone and a compatible peer:** real Wi-Fi/Bonjour/multicast behavior, Local Network prompts and Settings changes across devices, authentication/interoperability with desktop peers, cable/accessory behavior, sustained screen capture, app suspension/lock behavior, battery/thermal cost, and device-specific codecs/radios. Simulator tests and source presence are not physical-device evidence.

### Signing, provisioning, and secrets boundary

- Prefer Simulator CI that needs **no distribution certificate, provisioning profile, Apple account secret, or App Store Connect key**; use `CODE_SIGNING_ALLOWED=NO` where the selected Xcode scheme supports it. If the actual project requires signing for a specific test, document why and scope credentials to trusted jobs only.
- Never expose signing/provisioning credentials to pull-request code, forks, untrusted branches, or ordinary test artifacts. Keep PR permissions read-only; use protected environments and short-lived/minimum-scope secrets only for a later trusted device or release workflow.
- Confirm current Apple signing/provisioning rules before installing on a borrowed iPhone. Device development signing, beta distribution, App Store distribution, and public release are separate decisions. Do not create a release/archive-signing path in Phase 4 merely to make Simulator CI pass.
- Signing, provisioning, store enrollment, App Review, and release credentials are not configured or implied by the existence of hosted macOS runners.

### Borrowed-iPhone physical verification checklist

**Status: NOT STARTED — no iPhone, iOS app, Simulator run, or physical install has been tested for PhoneDock.** Do not check an item until it has actually been performed. For every result record device model, iOS version, app commit/build, Xcode version, date, network/peer, steps, observed result, and limits. Mark unimplemented or unapproved features `Not applicable / not in scope`, not `Passed`.

- [ ] Confirm an authorized borrowed iPhone and a legitimate signed installation path; install and launch the build; record first-launch, update, and reinstall behavior.
- [ ] Pair with a compatible desktop peer using the reviewed protocol; verify peer identity, approve/reject, persistence, authentication, revocation, and that revoked trust blocks reconnect.
- [ ] Exercise Local Network permission: first prompt and rationale, grant, deny, Settings change/revoke, and retry; verify unrelated app screens remain usable after denial.
- [ ] Test Bonjour discovery on a real supported Wi-Fi network; verify duplicate/lost candidates, address changes, reconnect, manual entry if approved, and unsupported network/interface cases.
- [ ] If and only if file transfer is implemented and approved, select real files, verify destination and checksum, cancel/interruption behavior, duplicate-name policy, and cleanup.
- [ ] If and only if USB is approved for a documented accessory/host pair, test cable/accessory permission, unplug/replug, and recovery. Otherwise record generic USB as unsupported/not included.
- [ ] Exercise connection loss/recovery, Wi-Fi changes, foreground/background, screen lock/unlock, app suspension/termination/relaunch, cancel/disconnect, and bounded retry. Record what the OS suspends rather than assuming an always-on session.
- [ ] If and only if a capture API is approved, use the current system picker/consent flow, start/stop/interruption handling, and any disclosed microphone/camera/background permissions. Test only APIs supported by the tested OS.
- [ ] Exercise every permission denial/revocation used by implemented features; verify privacy-safe diagnostics do not contain keys, tokens, clipboard/file/notification content, or private addresses by default.
- [ ] Measure sustained-session reliability, transfer/capture latency where applicable, battery and thermal behavior; record device/OS/network variation instead of generalizing from one phone.
- [ ] Review VoiceOver, Dynamic Type, light/dark appearance, increased contrast, reduced transparency/motion, touch targets, and any Liquid Glass fallback on the claimed OS range.
- [ ] Record device-specific feature limits and failures; remove unsupported model/OS combinations from claims. Physical evidence applies only to the tested configurations.

Until performed, physical iPhone validation remains an external prerequisite for hardware-supported claims, not a reason to invent emulator evidence or a fake test result.

### Optional Hackintosh investigation — not a dependency

A local Hackintosh is **not recommended or required** for PhoneDock. It is not the project foundation, and no installation instructions or compatibility guarantee are provided. The developer must not erase, replace, or repartition Linux Mint to try one.

**Licensing gate first:** the current [macOS Tahoe 26 Software License Agreement](https://www.apple.com/legal/sla/docs/macOSTahoe.pdf) is expressly “For use on Apple-branded Systems”; the [Xcode and Apple SDKs Agreement](https://www.apple.com/legal/sla/docs/xcode.pdf) says Apple software is authorized for execution only on an Apple-branded product running macOS. On that wording, treat installing/running macOS or Xcode on the non-Apple HP as **not an approved development path absent explicit Apple authorization/current legal review**. This is a project-risk note, not legal advice; re-read the then-current terms before any consideration. If the license gate is not cleared, stop this route and use hosted macOS CI and, when possible, borrowed Apple hardware.

If authorization/terms ever permit a technical feasibility study, first identify the exact HP product number and inventory its actual components; “EliteBook 840 G1” alone does not identify the configuration. Review the [HP support manuals/UEFI documentation](https://support.hp.com/us-en/product/hp-elitebook-840-g1-notebook-pc/5405360/manuals) and determine:

- Exact CPU/firmware/board, instruction-set and graphics device; whether that exact combination supports hardware acceleration required by a then-current Apple-supported macOS/Xcode and iOS Simulator.
- Exact Wi-Fi/Bluetooth, Ethernet, USB controller, audio, camera, display, touchpad/keyboard and storage devices; whether each has stable drivers without unsupported patches.
- BIOS/UEFI version/settings, boot/security features, ACPI/power management, sleep/wake, battery behavior, storage headroom, and any firmware update/recovery risks.
- Whether a macOS version supported by Apple on the hardware could also run the required **stable** Xcode, iOS SDK, and simulator runtime; verify against Apple's current [Xcode system requirements](https://developer.apple.com/xcode/system-requirements/), rather than choosing an obsolete Xcode merely to boot.
- Update/security reliability: OS/Xcode updates, graphics acceleration, Wi-Fi, USB, sleep/resume, virtualization, recovery, and whether critical build/tests fail after updates. Unsupported patches are not a repeatable release environment.

No exact unit inventory or compatible supported macOS/Xcode configuration has been established. The project must continue on Linux Mint plus official hosted macOS CI if the experiment fails, is unreliable, or is not licensed. Keep Mint installed and usable throughout; do not treat Hackintosh as a prerequisite, acceptance criterion, or substitute for an iPhone.

## Phase 9 — Native macOS desktop app

**Status: planned; no macOS application source/project exists.** The iOS CI host does not count as this product. Phase 9 should build a separate native Mac app with macOS-specific navigation/window behavior, device discovery/trust, connection status, settings, permissions, and only the workflows that Phases 2–8 actually support. SwiftUI/AppKit is a candidate, subject to a Phase 1/Phase 9 ADR; do not infer that iOS UI or every iOS API can be reused as a macOS app.

Respect macOS Local Network privacy, sandbox/file access, system appearance/accessibility, and signing/notarization requirements. Use a macOS target and macOS-specific tests/destinations; physical-Mac validation is separate from iOS Simulator testing. An existing stable macOS runner may later run both iOS and macOS schemes, but each product needs a real target, repeatable command, and separate evidence. Do not create the `macos/` scaffold before this phase begins.

## Required phase gate

For every feature/phase, the pull request or release record must include:

1. Requirement and acceptance criteria.
2. Platforms included and excluded, with reasons.
3. Source/configuration changed.
4. Commands, tests, CI run IDs/results, and any real-device evidence.
5. Permission, threat-model, and privacy impact.
6. Known limitations, blockers, and residual work.

A compile-only result does not complete an end-user feature. Missing hardware, signing credentials, Apple/Windows SDKs, or required services must be stated as blockers rather than replaced by an unverified claim.

## Phase 0 status

Phase 0 is **complete for the repository/CI foundation scope; PR review and merge remain pending**. Hosted run [36652649534](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36652649534) passes the existing repository/source, Linux desktop dependency/import/UI-smoke, Android lint/debug-assembly, and Windows x64 Release-build jobs; GitGuardian passes. Android's unit-test task has no product test sources; the Windows result is compile-only; and the Linux smoke does not establish real session/network/device behavior. This run does **not** test an iOS/macOS app, Xcode, or iPhone. Local Android/Windows builds remain blocked by missing Java/Android SDK and MSBuild/Windows SDK; local Qt offscreen startup is blocked by missing `libGL.so.1`. Physical Android/Windows device tests remain outside this repository-only gate and are not claimed as complete.

## Known risks and external prerequisites

- Pairing, authenticated encryption, message framing, device identity, and cross-platform capability negotiation are not finalized or implemented.
- Android APIs/permission behavior and encoder support vary across OS versions/hardware; Linux distributions/display sessions and Windows codec/runtime behavior also need declared test matrices.
- iOS Phase 4 is planned but has no project, source, CI job, signing setup, Simulator result, or iPhone evidence. Phases 1–3 are real prerequisites; current iOS 27 capture APIs are beta and not a release commitment.
- macOS is both a planned native product (Phase 9) and the official iOS build/test environment; no Mac app currently exists.
- Web is planned in Phase 10; there is no site/client source or browser security decision.
- The Windows second-display concept requires driver source, WDK, code signing, supported OS policy, hardware, and recovery testing.
- Signing/notarization, iOS provisioning/distribution, Android distribution/store credentials, and release updates are not configured. Never store signing credentials in workflow source or expose them to pull-request builds.
- No project release/tag history is present; embedded application version strings do not establish a release convention.
- License attribution in the checked-in `LICENSE` is template-like and needs maintainer confirmation before distribution claims.

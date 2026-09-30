# PhoneDock roadmap

This is the authoritative, dependency-aware development plan—not a calendar promise. Each phase is complete only when its deliverables and verification evidence exist. Status rules are in [FEATURE_STATUS.md](FEATURE_STATUS.md); current platform evidence is in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md). Product scope is sourced from [PRODUCT_SPEC.md](PRODUCT_SPEC.md).

## Phase overview

| Phase | Objective | Depends on | Completion evidence |
|---|---|---|---|
| **0 — Repository recovery and engineering foundation** | Audit and preserve existing work; state current versus intended product; establish docs, contribution/status conventions, practical CI, and safe repository defaults. | None | Repository audit matches source; docs links/checks pass; relevant CI jobs pass or are precisely documented as blocked; no new regression is unresolved. |
| **1 — Product, design, architecture and threat-model decisions** | Review requirements, visual direction, product boundaries, architecture options, privacy model and threat model; approve only decisions supported by evidence. | Phase 0 | Reviewed product acceptance criteria; accessibility-reviewed design prototype; threat model; ADRs for actual decisions; unresolved items explicitly listed. |
| **2 — Protocol and cross-platform engineering foundation** | Specify versioned discovery/session boundaries, device identity and capability negotiation; define test vectors, portable interfaces, error model, logging policy and CI matrix. | Phase 1 security/architecture decisions | Protocol review and conformance tests; cross-platform parsers reject malformed/oversized input; version mismatch is safe; no app advertises compatibility it has not implemented. |
| **3 — Trusted local discovery and connection lifecycle** | Replace unauthenticated prototype sessions with explicit pairing, authentication, capability negotiation, status, cancellation, disconnection and reconnect behavior. | Phase 2 protocol/security | End-to-end tests for Android/Linux and whichever desktop target passes its build; real LAN discovery/pairing and revocation tests on named OS/device versions; unknown peers cannot access sessions. |
| **4 — Native iOS companion** | Build a real Swift/SwiftUI iPhone companion for the iOS-supported subset of discovery, pairing, session status and settings. Establish the Xcode project and app/test structure when this phase starts; investigate and exclude unsupported capabilities rather than promising parity. | Phases 1–3; macOS/Xcode access; reviewed protocol, trust and capability contracts. Does **not** wait for later Android-specific feature phases. | Real Xcode app project; documented Apple API/policy capability decisions; macOS CI build plus practical XCTest/XCUITest simulator coverage; borrowed-iPhone checklist recorded before any physical-device/support claim. |
| **5 — Android capture and desktop screen viewing** | Complete Android user-consented capture/AVC path and one supported desktop receiver/rendering path; handle permissions, lifecycle, orientation, backpressure and recovery. | Phase 3 authenticated session | End-to-end real-device video; tested start/stop/rotation/background/permission revocation/network loss; measured latency and resource behavior; Linux or Windows receiver explicitly named as supported. |
| **6 — Supported remote control and USB** | Add capability-gated Android input controls and supported USB transport/manual connection flows. | Phases 2–3 and 5; relevant platform API reviews | Permission/developer-setup documentation; input coordinate/keyboard and cancellation tests; cable/permission/reconnect tests for each declared host/device combination. iOS input is not implied. |
| **7 — File transfer and content handoff** | Deliver reliable user-selected file transfer, shared inbox, queue/progress/history and explicit link/text/image handoff. | Phase 3 security/session; Phase 2 message framing | Integrity-checked transfer suite covering interruption, cancellation, large files, duplicate paths and low storage; destination/privacy UX tests; no traversal/overwrite vulnerability. |
| **8 — Clipboard, notifications, media and device management** | Add opt-in clipboard sync, supported notification/media integration, persistent trusted-device management, transfer history and diagnostics. | Phase 3 identity; relevant platform permission decisions; Phase 7 transfer metadata | Permission and revocation tests per platform; loop/privacy/logging tests; persistent-state and multi-device tests; metrics have real definitions and are measured. iOS support is feature-by-feature and policy-gated. |
| **9 — Web application and product website** | Add a maintained website for product/docs/release information and only browser workflows supported by a reviewed permission/security model. | Phase 1 design/content; Phase 2 protocol boundaries if browser client is approved | Reproducible web build, accessibility and browser tests, security review for local-network access; no unsupported native capability claims. |
| **10 — Android second-display mode** | Research, implement and support Android-as-display only after confirming OS driver/display-extension feasibility for each host. | Phases 1, 2, 5; platform/driver research | Supported OS/device matrix; install/uninstall, recovery and security tests; end-to-end real hardware; maintainer decision that maintenance cost is justified. |
| **11 — Production hardening and releases** | Audit security/privacy, accessibility, performance, dependency health, packaging, signing, crash handling, support docs, rollback and distribution for each supported app. | Relevant feature phases and approved launch scope | Release checklist passes for every claimed platform; signed/notarized/store artifacts only with valid credentials; checksums and provenance; documented support/update behavior; no unresolved critical/high security issue. |

## Platform responsibilities and sequencing

- **Android:** current Android source is the only phone-side implementation. Stabilize its permissions, foreground-service/capture lifecycle, identity, local transport and capability reporting before adding remote input or other integrations. Run emulator tests plus named physical Android devices.
- **iOS:** Phase 4 is a dedicated native-app implementation phase immediately after protocol, trust and session foundations. It is not deferred until Android-only capture, input, transfer or clipboard work is complete. Build a useful iOS companion slice first, and gate each additional capability on current Apple API/policy evidence. No iOS project or iOS CI job exists yet.
- **Linux:** preserve the existing PySide6/PyAV prototype. Establish reproducible dependencies, receiver tests, supported distribution packaging and OS-specific networking. Do not replace it with another framework without a reviewed migration case.
- **Windows:** preserve the C++ project while determining whether it is a viable receiver/application. Complete only the supported UI/video path; keep driver/second-display work separate and require WDK/hardware evidence. Do not treat project headers as a driver.
- **macOS desktop:** no app exists. Make a separate native Mac application decision when requirements and owners exist; respect macOS privacy prompts and distribution/signing/notarization requirements. iOS CI on a macOS runner is build infrastructure, not a macOS PhoneDock app.
- **Web:** no app/site exists. First deliver accessible product/documentation/release pages; treat browser-to-device communication as a separate security/capability decision, not a guaranteed browser port of native apps.
- **Shared components:** no shared package exists. Introduce portable code only after Phase 2 proves a stable boundary and language/toolchain fit. Protocol conformance fixtures and security review may be shared even when UI/platform code is not.
- **Design assets/tokens:** Phase 1 should reconcile the existing prototype palettes and default Android launcher icon with the proposed identity. Keep source assets and generated platform exports traceable; do not create unused design-token packages.

## Phase 4 — Native iOS companion

**Status: planned; implementation not started.** The repository has no iOS source, Xcode project, iOS CI job, simulator result, or iPhone test. Do not create an empty project before its implementation phase. When Phase 4 begins, establish a real Swift/SwiftUI app and test structure together with its first implemented, reviewable workflows.

### Native app and initial product scope

- Use Swift and SwiftUI with native iOS navigation, controls, typography, accessibility and system appearance. Deliver a polished companion interface, not a transplanted Android screen. Use Liquid Glass/system materials only where the selected iOS versions support them; provide and test a legible non-glass fallback on older or unsupported systems.
- At phase start, create the Xcode project, application target and only the structure needed by real code. A starting organization may separate the app entry point, `Devices`, `Pairing`, `Session` and `Settings` features, platform/network services, shared domain state, resources, XCTest unit tests and XCUITest UI tests. Do not commit placeholder folders or pretend an empty target is an application.
- Define the first useful iOS release around a real device list/discovery flow, explicit peer identity and approve/reject/revoke pairing, truthful connecting/connected/disconnected/error status, user-controlled cancellation/disconnection, and settings for supported privacy, appearance and connection behavior, plus actionable permission/help guidance and privacy-safe diagnostics. These workflows depend on Phases 2–3 protocol, authentication and capability agreements; they are planned features, not current functionality.
- Support automatic discovery only through a reviewed iOS-compatible transport. Offer manual connection only if the approved protocol, authentication and user experience support it. Never treat a Bonjour result, nearby peer, IP address or QR/code as trusted without the agreed pairing flow.
- Add transfer, clipboard, notification, media, capture or control workflows only after the capability investigation below and their per-feature product/security decisions. Report unavailable, permission-required and unsupported states honestly.

### Apple capability and policy investigation gate

Before specifying or advertising an iOS capability, review the current Apple developer documentation, SDK availability, privacy/entitlement requirements, App Review rules and relevant user-consent flow. Record the decision and source links in an ADR and update [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md). At minimum investigate:

| Area | Questions Phase 4 must resolve before making a product claim |
|---|---|
| Screen capture and mirroring | What user-consented ReplayKit/app-recording or broadcast workflows, if any, support PhoneDock's intended direction and streaming model? Distinguish an app's own content from system-wide capture; document audio, extension, interruption and distribution limits. Do not promise arbitrary iPhone screen mirroring. |
| Remote input/control | Which public APIs and current policies, if any, support the exact intended interaction? Do not assume system-wide touch, keyboard injection or control of other apps; explicitly exclude it unless a supported, reviewable path is demonstrated. |
| Background execution | Which approved background modes/tasks apply to the chosen workflow, for how long, and with what user-visible behavior? Design a correct foreground-only fallback; do not promise an always-running socket, discovery or capture service. |
| Local networking | Review Local Network privacy prompts/usage descriptions, Bonjour service declarations, `Network.framework` behavior, multicast requirements/entitlements if relevant, address changes and denial/revocation handling. Validate the actual discovery and transport design. |
| Inter-device communication | Compare supported Bonjour/Network framework and `MultipeerConnectivity` options only where relevant; assess OS-version, network, permission, peer-discovery and protocol-interoperability limits. Select a transport only after it fits Phases 2–3 and is testable. |
| Clipboard, notifications and other integrations | Check current access, user-gesture, extension, background and App Review constraints per feature. Do not infer continuous clipboard access or notification-listener parity from another OS. |

For each investigated capability, record one outcome—supported with conditions, restricted/entitlement-dependent, not supported for the intended workflow, or not pursued—plus minimum OS version, user consent, test evidence and any fallback. **No Android feature parity is implied.**

### macOS CI and simulator testing without personal Apple hardware

- When the actual app project is created, add a least-privilege macOS GitHub Actions job using an available macOS runner and its installed Xcode/iOS SDK. At phase kickoff, verify runner availability and record the selected runner image, `xcodebuild` version, simulator runtime and supported build destination; do not assume a particular image will remain available.
- Build and run XCTest against an official iOS Simulator destination in Xcode. Add unit tests for capability/state logic, validation, protocol fixtures and pairing/session transitions; use XCUITest for practical launch, navigation, permission-denial/recovery, settings and accessibility-ID smoke coverage. Keep network/API boundaries injectable so deterministic tests do not require an Apple device or live peer.
- Simulator CI can verify Swift compilation, unit logic, view/state integration, basic layouts/navigation and UI automation on the selected simulator runtime. These results must be labelled **simulator/CI verified**, not physical-device verified.
- Simulator tests do not establish real-device Wi-Fi/Bonjour/multicast behavior, privacy-prompt behavior across devices, sustained background execution, hardware capture/mirroring, battery/thermal performance, or interoperability with real peers. Keep those on the borrowed-iPhone checklist below.
- The iOS Simulator is Apple's Xcode simulator and runs on macOS. Do not attempt to run it on Linux or create a custom iOS emulator. This documentation change does not add an Apple CI job because there is not yet an iOS project or scheme.

### Development prerequisites and signing

- macOS/Xcode access with a supported Xcode version, iOS SDK and official simulator runtime; a suitable GitHub-hosted macOS runner for CI. No personal Mac or iPhone is required for simulator build/unit/UI checks, but physical-device claims do require a real iPhone.
- Complete Phases 1–3: accepted iOS requirements/design and threat model, reviewed protocol and capability negotiation, and an authenticated pairing/session lifecycle that the iOS app can implement and test.
- Select the minimum iOS deployment target only after API/policy review. Confirm current Apple signing/provisioning requirements for simulator builds, borrowed-device installation and each intended distribution channel at phase start. Prefer simulator CI that does not need distribution credentials; keep any required signing secrets out of pull-request jobs and untrusted code. Physical-device installation and public distribution may require separate Apple account/team, signing and provisioning setup.
- Record the selected Xcode/SDK and runner availability as project prerequisites; signing and distribution decisions are not implied by the existence of a simulator build.

### Borrowed-iPhone physical verification checklist

**Status: NOT STARTED — no iPhone, simulator, or iOS build has been tested for this project.** Use a borrowed, authorized iPhone when Phase 4 reaches device verification. For every checked item, record device model, iOS version, app commit/build, Xcode version, date, network, steps and observed result. Keep unsupported/unapproved features explicitly marked out of scope; do not check them as passed.

- [ ] Install and launch a signed test build; record first launch, upgrade/reinstall behavior, and any required provisioning setup.
- [ ] Exercise Local Network permission: grant, deny, explain the failure state, change the choice in Settings, and retry after the permission changes.
- [ ] Discover/remove/re-discover a protocol-compatible peer on a real supported Wi-Fi network; test service/address changes and document networks/interfaces not supported.
- [ ] Approve, reject, revoke and re-establish pairing; verify peer identity, persistence, session authentication and that revocation blocks reconnect.
- [ ] Verify real session status, cancel/disconnect, network loss/restore, Wi-Fi change, app foreground/background, lock/unlock and process suspension/termination behavior.
- [ ] Check VoiceOver, Dynamic Type, light/dark appearance, contrast, reduced motion, and Liquid Glass plus its fallback on the supported iOS-version matrix.
- [ ] If and only if the capability review approves screen capture/mirroring, test its permitted user-consent/start/stop/interruption flow. Otherwise record it as unsupported/not included; do not imply this checklist grants feasibility.
- [ ] If and only if a public, policy-compliant input path is approved, test its explicit consent and stop/revoke behavior. Otherwise record remote input as unsupported/not included.
- [ ] Measure sustained-session network, battery and thermal behavior for each device/OS combination being claimed; document failures and remove unsupported combinations from the support matrix.

No checked item alone establishes support for all iPhones/iOS versions. Publish a device-support claim only after the corresponding evidence is reviewed and recorded.

## Required phase gate

For every feature/phase, the pull request or release record must include:

1. requirement and acceptance criteria;
2. platforms included and excluded, with reasons;
3. source/configuration changed;
4. commands, tests, CI run IDs/results, and any real-device evidence;
5. permission, threat-model, and privacy impact;
6. known limitations, blockers, and residual work.

A compile-only result does not complete an end-user feature. Missing hardware, signing credentials, Apple/Windows SDKs, or required services must be stated as blockers rather than replaced by an unverified claim.

## Phase 0 status

Phase 0 is **complete for the repository/CI foundation scope; PR review and merge remain pending**. Hosted run [36651228945](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36651228945) passes repository/source checks, Linux dependency imports and offscreen UI smoke, Android lint/debug assembly, and the Windows x64 Release build; GitGuardian passes. Earlier CI failures were diagnosed and fixed: Linux Qt runtime dependencies and a `QColor` mismatch, Windows DNS-SD SDK field names, and Android notification/foreground-service permissions. Android's unit-test task has no product test sources, and all CI builds are compile/lint/smoke evidence only—not end-to-end feature, network, or hardware verification. Local Android/Windows builds remain blocked by missing Java/SDK and MSBuild/Windows SDK; the host also lacks Qt's `libGL.so.1`, so the local UI smoke could not run. Physical Android/Windows device tests remain explicitly outside this repository-only Phase 0 gate and must not be claimed as completed.

## Known risks and external prerequisites

- Pairing, authenticated encryption, message framing and device identity are not decided or implemented.
- Android APIs/permission behavior and encoder support vary across OS versions and hardware.
- iOS has an explicit Phase 4 implementation plan, but no Xcode project, Apple CI job, runner/Xcode selection, signing setup, or device evidence exists yet. The capability investigation and Phases 1–3 are prerequisites; this plan is not an implementation or support claim.
- No macOS desktop or web project/owner/build prerequisites are present.
- The Windows second-display concept would involve driver/OS lifecycle and security work; WDK, code signing and supported OS policy are unresolved.
- Signing/notarization, Android distribution and store accounts/credentials are not configured. Never store signing credentials in GitHub workflow source or expose them to pull-request builds.
- No project release/tag history is present; embedded application version strings do not establish a release convention.
- License attribution in the checked-in `LICENSE` is template-like and needs maintainer confirmation before distribution claims.

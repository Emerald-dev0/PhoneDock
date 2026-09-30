# PhoneDock roadmap

This is a dependency-aware delivery sequence, not a calendar promise. Each phase is complete only when its deliverables and verification evidence exist. Status rules are in [FEATURE_STATUS.md](FEATURE_STATUS.md); current platform evidence is in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md). Product scope is sourced from [PRODUCT_SPEC.md](PRODUCT_SPEC.md).

## Phase overview

| Phase | Objective | Depends on | Completion evidence |
|---|---|---|---|
| **0 — Repository recovery and engineering foundation** | Audit and preserve existing work; state current versus intended product; establish docs, contribution/status conventions, practical CI, and safe repo defaults. | None | Repository audit matches source; docs links/checks pass; CI workflows validate and the relevant GitHub jobs pass or are precisely documented as blocked; no new regression is unresolved. |
| **1 — Product, design, architecture and threat-model decisions** | Review requirements, visual direction, product boundaries, architecture options, privacy model and threat model; approve only decisions supported by evidence. | Phase 0 | Reviewed product acceptance criteria; accessibility-reviewed design prototype; threat model; ADRs for actual decisions; unresolved items explicitly listed. |
| **2 — Protocol and cross-platform engineering foundation** | Specify versioned discovery/session boundaries, device identity and capability negotiation; define test vectors, portable interfaces, error model, logging policy and CI matrix. | Phase 1 security/architecture decisions | Protocol review and conformance tests; cross-platform parsers reject malformed/oversized input; version mismatch is safe; no application advertises compatibility it has not implemented. |
| **3 — Trusted local discovery and connection lifecycle** | Replace unauthenticated prototype sessions with explicit pairing, authentication, capability negotiation, status, cancellation, disconnection and reconnect behavior. | Phase 2 protocol/security | End-to-end tests for Android/Linux and whichever desktop target passes its build; real LAN discovery/pairing and revocation tests on named OS/device versions; unknown peers cannot access sessions. |
| **4 — Android capture and desktop screen viewing** | Complete Android user-consented capture/AVC path and one supported desktop receiver/rendering path; handle permissions, lifecycle, orientation, backpressure and recovery. | Phase 3 authenticated session | End-to-end real-device video; tested start/stop/rotation/background/permission revocation/network loss; measured latency and resource behavior; Linux or Windows receiver explicitly named as supported. |
| **5 — Supported remote control and USB** | Add capability-gated Android input controls and supported USB transport/manual connection flows. | Phases 2–4 | Permission/developer-setup documentation; input coordinate/keyboard and cancellation tests; cable/permission/reconnect tests for each declared host/device combination. |
| **6 — File transfer and content handoff** | Deliver reliable user-selected file transfer, shared inbox, queue/progress/history and explicit link/text/image handoff. | Phase 3 security/session; Phase 2 message framing | Integrity-checked transfer suite covering interruption, cancellation, large files, duplicate paths and low storage; destination/privacy UX tests; no traversal/overwrite vulnerability. |
| **7 — Clipboard, notifications, media and device management** | Add opt-in clipboard sync, supported notification/media integration, persistent trusted-device management, transfer history and diagnostics. | Phase 3 identity; relevant platform permission decisions; Phase 6 transfer metadata | Permission and revocation tests per platform; loop/privacy/logging tests; persistent-state and multi-device tests; metrics have real definitions and are measured. |
| **8 — iOS companion** | Add a native SwiftUI iOS application with the subset of companion capabilities supported by iOS policy and APIs. | Phases 1–3; shared protocol | Xcode build/test on macOS CI; physical iPhone/iOS tests; capability matrix accurately excludes unsupported Android-style capture/input/background features. |
| **9 — Web application and product website** | Add a maintained website for product/docs/release information and only browser workflows supported by a reviewed permission/security model. | Phase 1 design/content; Phase 2 protocol boundaries if browser client is approved | Reproducible web build, accessibility and browser tests, security review for local-network access; no unsupported native capability claims. |
| **10 — Android second-display mode** | Research, implement and support Android-as-display only after confirming OS driver/display-extension feasibility for each host. | Phases 1, 2, 4; platform/driver research | Supported OS/device matrix; install/uninstall, recovery and security tests; end-to-end real hardware; maintainer decision that maintenance cost is justified. |
| **11 — Production hardening and releases** | Audit security/privacy, accessibility, performance, dependency health, packaging, signing, crash handling, support docs, rollback and distribution for each supported app. | Relevant feature phases and approved launch scope | Release checklist passes for every claimed platform; signed/notarized/store artifacts only with valid credentials; checksums and provenance; documented support/update behavior; no unresolved critical/high security issue. |

## Platform responsibilities and sequencing

- **Android:** current Android source is the only phone-side implementation. Stabilize its permissions, foreground-service/capture lifecycle, identity, local transport and capability reporting before adding remote input or other integrations. Run emulator tests plus named physical Android devices.
- **iOS:** no project exists. Start with native SwiftUI and Apple's native materials; establish an iOS capability boundary before promising screen capture, system input, notification, or background behavior. Build/test on macOS runners and real iPhones.
- **Linux:** preserve the existing PySide6/PyAV prototype. Establish reproducible dependencies, receiver tests, supported distribution packaging and OS-specific networking. Do not replace it with another framework without a reviewed migration case.
- **Windows:** preserve the C++ project while determining whether it is a viable receiver/application. Complete only the supported UI/video path; keep driver/second-display work separate and require WDK/hardware evidence. Do not treat project headers as a driver.
- **macOS:** no app exists. Make a separate native Mac application decision when requirements and owners exist; respect macOS privacy prompts and distribution/signing/notarization requirements.
- **Web:** no app/site exists. First deliver accessible product/documentation/release pages; treat browser-to-device communication as a separate security/capability decision, not a guaranteed browser port of native apps.
- **Shared components:** no shared package exists. Introduce portable code only after Phase 2 proves a stable boundary and language/toolchain fit. Protocol conformance fixtures and security review may be shared even when UI/platform code is not.
- **Design assets/tokens:** Phase 1 should reconcile the existing prototype palettes and default Android launcher icon with the proposed identity. Keep source assets and generated platform exports traceable; do not create unused design-token packages.

## Required phase gate

For every feature/phase, the pull request or release record must include:

1. requirement and acceptance criteria;
2. platforms included and excluded, with reasons;
3. source/configuration changed;
4. commands, tests, CI run IDs/results, and any real-device evidence;
5. permission, threat-model, and privacy impact;
6. known limitations, blockers, and residual work.

A compile-only result does not complete an end-user feature. Missing hardware, signing credentials, Apple/Windows SDKs, or required services must be stated as blockers rather than replaced by an unverified claim.

## Phase 0 status at this audit

Phase 0 deliverables are present in the recovery PR, but the initial hosted run [36648554925](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36648554925) failed Linux dependency imports, Android Gradle, and Windows C++; the repository checks and GitGuardian passed. The second run [36649242392](https://github.com/Emerald-dev0/PhoneDock/actions/runs/36649242392) passed repository checks and Linux dependency imports, but failed the Qt offscreen smoke, Android Gradle, and Windows C++ jobs. The sandbox cannot retrieve Actions log archives (EOF), so the precise Android/Windows diagnostics and Qt smoke exception are not yet known. Qt runtime libraries and evident Windows source/link issues have been corrected; sanitized failure diagnostics and Android/Windows job summaries are being added for the next run. Locally, Android is blocked by absent Java/Android SDK and Windows by absent MSBuild/Windows SDK. Phase 0 remains **in progress** until available hosted jobs pass and any regressions are resolved. Physical Android/Windows hardware validation remains outside this repository-only gate and must not be claimed as completed.

## Known risks and external prerequisites

- Pairing, authenticated encryption, message framing and device identity are not decided or implemented.
- Android APIs/permission behavior and encoder support vary across OS versions and hardware.
- iOS, macOS, and web projects/owners/build prerequisites are not present.
- The Windows second-display concept would involve driver/OS lifecycle and security work; WDK, code signing and supported OS policy are unresolved.
- Signing/notarization, Android distribution and store accounts/credentials are not configured. Never store signing credentials in GitHub workflow source or expose them to pull-request builds.
- No project release/tag history is present; embedded application version strings do not establish a release convention.
- License attribution in the checked-in `LICENSE` is template-like and needs maintainer confirmation before distribution claims.

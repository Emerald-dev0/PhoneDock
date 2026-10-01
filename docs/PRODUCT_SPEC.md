# PhoneDock product specification

**Status:** Product direction; requirements are proposed until accepted through normal project review. This document describes intended behavior, not current implementation. Repository evidence is maintained in [PROJECT_AUDIT.md](PROJECT_AUDIT.md) and platform evidence in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md).

## Purpose

PhoneDock aims to make a person's physical devices work together as one coherent workspace. It should let a user discover, intentionally trust, connect, and manage compatible devices, then use platform-supported workflows—such as Android screen viewing, file/content handoff, and optional clipboard sharing—without making a cloud account or relay a requirement for local-device use.

PhoneDock is a product family targeting Android, iOS, Linux, Windows, macOS, and the web. It is not a promise that every capability is available on every operating system. A device's actual APIs, permissions, hardware, network, and user settings determine what can be offered.

The iOS target is a real native-app objective, not a documentation-only entry. Its first planned slice is compatible-peer discovery, explicit pairing/trust, truthful session status, and useful settings, gated on the **future** shared protocol/security/session foundations in Phases 1–3; those foundations do not yet exist. Screen capture, mirroring, remote input, USB, background operation, clipboard, notifications, and media behavior are separate iOS feasibility decisions in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md); Android parity is not assumed. The native iOS implementation and borrowed-iPhone gate are specified in [ROADMAP.md](ROADMAP.md).

## Target users and workflows

- **People working across a phone and computer:** pair devices on a local network, view an Android screen on a desktop, and move selected content without an unrelated cloud workflow.
- **People managing several trusted devices:** see which devices are paired, reachable, connected, and what each supports; revoke trust when needed.
- **People who need continuity between devices:** intentionally hand off links/text/files and optionally synchronize clipboard content where operating-system policy permits.
- **Developers and maintainers:** diagnose pairing, network, codec, permission, and transfer failures with privacy-conscious diagnostics.

Representative workflow: the user opens PhoneDock on a supported Android device and desktop; discovers the local peer or enters its address; reviews an explicit pairing request; establishes an authenticated session; sees negotiated capabilities; starts an allowed workflow; observes status/progress; and can stop the workflow or revoke the device at any time.

## Product boundaries

1. **Local-first, not local-only.** Direct local operation is the default for local workflows. Optional network services may be considered later, but must be clearly disclosed, optional where practical, and must not silently become a prerequisite for a local connection.
2. **Platform-accurate capabilities.** Android, iOS, desktop operating systems, and browsers have different security and API boundaries. UI and docs must describe those differences instead of promising feature parity.
3. **Consent before sensitive access.** Screen capture, remote input, clipboard, notifications, files, and second-display behavior require transparent permission, trust, and stop/revoke controls appropriate to the platform.
4. **No simulated completion.** A button, mock connection state, static image, protocol constant, or project directory does not satisfy the feature's acceptance criteria.
5. **No silent remote access.** PhoneDock is intended for user-present local-device workflows; unattended access, internet-facing exposure, and remote control without a clear user-authorized session are not part of this specification.

## Functional requirements

Acceptance criteria below define the expected product behavior. They are proposed and have not been met merely because source or mockups exist.

| ID | Requirement and expected behavior | Minimum acceptance evidence |
|---|---|---|
| FR-01 | **Six application targets.** Provide Android and iOS mobile experiences, Linux/Windows/macOS desktop experiences, and a supporting web application/product website. Each app presents only its implemented and available capabilities. | A buildable project for each claimed target; platform-specific tests; capability states verified against actual APIs. The website is not presented as a substitute for native-only functionality. |
| FR-02 | **Local discovery and manual connection.** Discover compatible peers on supported local networks and allow a clearly documented manual connection path when supported. Discovery results are advisory, not trusted identities. | Integration tests for discovery, duplicate/lost results, multiple interfaces, IPv4/IPv6 decisions, timeouts, and manual connection; a discovered unknown peer cannot silently gain trust. |
| FR-03 | **Pairing and device trust.** First use requires an explicit user-visible trust decision. Users can identify peers, see trust/session state, reject pairing, revoke a device, and understand what the peer can do. | Negative and positive pairing tests; revoke/restore behavior; invalid/expired proof rejection; UI and logs do not leak key material. Pairing and authentication are not implemented in the baseline. |
| FR-04 | **Authenticated sessions and capability negotiation.** Establish a session only after peer authentication, negotiate a version and mutually supported capabilities, and fail closed for unsupported or unauthenticated peers. | Protocol conformance tests for version mismatch, unsupported capabilities, invalid authentication, disconnect and session expiry; reviewed security design. Exact protocol remains undecided. |
| FR-05 | **Connection lifecycle.** Present accurate states such as discovering, pairing, connecting, connected, reconnecting, disconnected, and failed. The user can cancel/disconnect; retry is bounded and does not silently reconnect after trust revocation. | State-machine tests, UI state tests, and network interruption/recovery tests. Displayed status is driven by the real session. |
| FR-06 | **Android screen viewing.** With Android's explicit screen-capture consent and compatible desktop support, stream an Android screen with aspect-ratio-correct rendering, a clear active indicator, start/stop controls, and graceful behavior when permission or codec support is unavailable. | Permission/lifecycle tests; real-device capture/rotation/lock/stop tests; end-to-end video decode and network interruption tests on a named device/OS matrix. |
| FR-07 | **Supported Android remote interaction.** Offer mouse/keyboard/touch actions only when the target device and permissions support them. Clearly disclose any additional system, accessibility, or developer setup and allow the user to stop input forwarding. | End-to-end input mapping, pointer bounds, keyboard and permission-denial tests on named Android devices. No claim of universal input injection or equivalent iOS control. |
| FR-08 | **USB and local Wi-Fi.** Support direct local Wi-Fi and USB workflows only where a platform/device-specific transport is implemented and authorized. Users can distinguish connection type and receive actionable errors. | Hardware/host-specific integration tests; pairing/authentication identical in strength to network sessions; cable unplug/replug, permission, and recovery checks. USB is not implemented in the baseline. |
| FR-09 | **File transfer and shared inbox.** Transfer explicitly selected files to a user-visible destination/inbox; show queue, progress, completion/failure, cancellation, and history. Preserve file names safely and verify content integrity. | Tests for small/large files, zero-byte files, cancellation, interruption/resume policy, duplicate names, disk-full, permissions, path traversal, and checksum equality. |
| FR-10 | **Content and link handoff.** Let a user deliberately send supported text, links, images, and other selected content between trusted devices. Show destination and result; do not silently publish or upload content. | Content-type/size tests, permission tests, explicit destination confirmation for sensitive actions, and device-to-device integration evidence. |
| FR-11 | **Clipboard synchronization.** Make synchronization optional and separately controllable by direction. Avoid feedback loops, disclose platform limits, apply safe size/format rules, and provide a pause/disable control. | Tests for bidirectional changes, duplicates, large/unsupported content, app lifecycle, and privacy controls. Platform restrictions and user consent are documented per target. |
| FR-12 | **Notification forwarding and media controls.** Forward notifications or expose media controls only on platforms that provide the needed APIs and permissions. Allow source/app selection, preview, pause, and revoke where available. | Tests for permission denial/revocation, filtering, lifecycle, supported media state, and no content in diagnostic logs. An Android foreground-service notification is not this feature. |
| FR-13 | **Device management.** Show a persistent, user-editable list of trusted devices, available capabilities, connection type/status, and a way to remove/revoke each device. | Persistence/restart tests, multiple-device tests, offline state accuracy, and successful trust revocation. |
| FR-14 | **Transfer history.** Show locally maintained transfer metadata and status, with clear retention/deletion controls. Content should not be retained by default unless a feature explicitly requires it. | Persistence, deletion, retention, and privacy tests; metadata/content distinction documented. |
| FR-15 | **Diagnostics and performance.** Surface useful, user-controlled connection/capture/transfer diagnostics and meaningful measurements such as latency, frame/transfer rate, and errors only when calculated from real measurements. | Deterministic metric definitions, instrumentation tests, throttling/overhead checks, export/log privacy tests, and network/codec failure injection. No fabricated metrics. |
| FR-16 | **Android as an additional display.** Where technically supported, provide a separate display extension with explicit platform prerequisites and safe uninstall/recovery behavior. | A maintained display implementation/driver, OS/hardware compatibility matrix, install/uninstall/recovery tests, and real-device latency/reliability evidence. A static driver project or IOCTL header is not acceptance. |
| FR-17 | **Native-feeling, accessible applications.** Each app follows platform conventions, responds to system appearance and text scaling where supported, is keyboard/screen-reader usable, and honors reduced-motion preferences. | Accessibility review and automated checks where available; platform UI tests; contrast/focus/large-text/reduced-motion evidence. |
| FR-18 | **Native iOS companion.** Provide a Swift/SwiftUI iPhone app with supported peer discovery, explicit approve/reject/revoke trust, accurate connection/session status, cancellation/disconnection, and useful privacy/connection settings with actionable permission help and privacy-safe diagnostics. Gate every additional workflow using the per-feature matrix in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md) and current Apple API/policy review. The iOS 27 ScreenCaptureKit path is beta at the 2026-10-01 research snapshot; do not make a release promise from beta or claim unsupported system-wide input/capture, USB, or Android parity. | Real Xcode project and app/test targets; macOS CI build plus XCTest and practical XCUITest on the official iOS Simulator; documented per-capability decisions; borrowed-iPhone checklist recorded before any physical-device or support claim. |

## Nonfunctional requirements

- **Security:** authenticated encrypted sessions; least privilege; bounded parsers, queues, and resource use; safe storage and rotation/revocation of trust material; explicit security review before public releases. The protocol and cryptographic library choices remain open.
- **Privacy:** local processing by default; no account requirement for core local workflows; minimize retained data; avoid sensitive content in logs/telemetry; clear per-feature controls and retention choices.
- **Reliability:** tolerate disconnects, device sleep, network changes, rotation, permission changes, process death, and storage errors without reporting false success or corrupting transferred files.
- **Performance:** establish measured baselines before setting targets. Streaming/transfer instrumentation must describe how a metric is calculated and its resource cost.
- **Battery and thermal behavior:** adapt or stop work when sessions end or platform constraints require it; test prolonged capture/transfer on real devices.
- **Compatibility:** state supported OS/device versions based on actual test evidence. Do not infer compatibility from a minimum SDK declaration or compile result alone.
- **Accessibility and localization:** platform-appropriate assistive-technology behavior, scalable text, keyboard/navigation support, localization-ready strings, and reduced motion.
- **Maintainability:** documented protocol, reproducible builds, dependency-update policy, tests at component boundaries, and explicit owners for platform-specific code.

## Out of scope unless separately approved

- Mandatory cloud accounts, cloud relay, or cloud storage for ordinary local workflows.
- Unattended internet-facing remote access or covert screen/input capture.
- Claiming iOS can expose Android-equivalent arbitrary screen capture, background behavior, or remote input.
- Universal USB support across all device/host combinations without platform-specific permission and compatibility work.
- A finalized wire protocol, shared-language runtime, monorepo build system, or application rewrite before an ADR and migration plan justify it.
- Automatic updates across installed applications merely because a GitHub Release exists. Update delivery, signing, rollback, and platform-store policies are separate work.

## Implementation status

At the audited baseline, Android, Linux, and Windows contain prototypes described in [PROJECT_AUDIT.md](PROJECT_AUDIT.md). iOS, macOS, and web source was not found. A real native iOS app is planned for Phase 4 after Phases 1–3; a separate native macOS app is planned for Phase 9; web is planned for Phase 10. None has started. Pairing, authenticated encryption, file transfer, clipboard synchronization, notification forwarding, media controls, persistent device management, and production second-display support were not found. Use [FEATURE_STATUS.md](FEATURE_STATUS.md) and [ROADMAP.md](ROADMAP.md) to track evidence and phase completion.

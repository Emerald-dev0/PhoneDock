# PhoneDock architecture

This page separates **observed architecture** from **proposed logical architecture**. Proposed states and boundaries are not implemented APIs. No protocol, shared language, or cross-platform build system is finalized. See [PROTOCOL.md](PROTOCOL.md), [SECURITY.md](SECURITY.md), and [decisions/README.md](decisions/README.md) for open decisions and ADR practice.

## Existing repository architecture

```text
Android (Kotlin / Compose)                      Linux desktop (Python / PySide6)
┌───────────────────────────────┐                ┌─────────────────────────────┐
│ MainActivity / Dashboard UI   │                │ main.py / VideoView         │
│ MediaProjection consent       │                │ device list / mouse events  │
│ ConnectionService             │                │ DiscoveryManager            │
│ ├─ ServerSocket               │                │ ├─ zeroconf browser         │
│ ├─ NsdHelper                  │                │ ├─ TCP ConnectionManager    │
│ └─ ScreenStreamer             │──── TCP ──────▶│ └─ PyAV H.264 decoder       │
│    MediaCodec AVC encoder     │                └─────────────────────────────┘
└───────────────────────────────┘

Windows (C++ prototype)
┌──────────────────────────────────────────────────────┐
│ console main.cpp → DiscoveryAgent → SessionClient    │
│                    → VideoDecoder (Media Foundation) │
│                    → Renderer (Direct3D 11, TODO)    │
└──────────────────────────────────────────────────────┘
```

Evidence: Android files under `android/app/src/main/kotlin/com/phonedock/app/`; Linux source under `desktop/`; Windows source under `windows/PhoneDock.App/`. The diagram shows source-level intent, not verified interoperability. Android/Linux/Windows do not share a library, state machine, parser, test vectors, or identity store. `windows/PhoneDock.Common/Public.h` is Windows-only and contains unused-looking protocol/display constants. The separate driver project has no implementation source.

## Proposed logical architecture

Preserve native presentation and OS integration. Define portable boundaries only where shared behavior has been demonstrated and maintainable with the existing languages/toolchains.

```text
Native applications and OS adapters
  Android / iOS / Linux / Windows / macOS / Web
                │ user consent, UI state, platform permissions
                ▼
Device and capability model (proposed)
                │ stable identity, trust state, negotiated capability set
                ▼
Session / security boundary (proposed; authenticated and encrypted)
       ┌────────┴────────┐
       ▼                 ▼
Control/data plane     Media plane
(discovery, pairing,  (capture, encode, bounded stream,
status, file, text)    decode, render, metrics)
       └────────┬────────┘
                ▼
Local transport adapters (Wi-Fi/USB only when supported)
```

The web target may deliver product information and selected browser-supported operations, but is not assumed to own unrestricted local sockets, background work, or native device privileges. Desktop and mobile interfaces remain platform-specific. A shared protocol specification, fixtures, design tokens or small portable modules may be useful; their technology and responsibilities require evidence and an ADR before implementation.

## Application boundaries

- **Presentation:** render state from real services, collect user actions, surface permission requirements and errors; never fabricate connection, performance or transfer success.
- **Platform integration:** MediaProjection/MediaCodec, iOS capture/background/notification APIs, desktop display/input, file pickers and permissions remain in platform adapters. Capability reporting must reflect runtime availability.
- **Device identity and trust:** separate stable peer identity from mutable network addresses/service names. Persist trust only after explicit pairing; provide revoke/delete behavior. No such identity store exists today.
- **Session coordinator:** own connect/cancel/disconnect/reconnect transitions, timeouts and cleanup. A screen or ViewModel must not be the authoritative network state.
- **Protocol/session security:** validate versions, identity, negotiated capabilities, message lengths and permissions before application data is processed. Avoid custom cryptography.
- **Transport adapters:** discovery is not authentication. Wi-Fi, USB and any future transport should carry the same authenticated session semantics where practical, while exposing platform-specific limitations.
- **Feature services:** streaming, file transfer, clipboard, notifications, media controls and diagnostics should have explicit ownership, consent, cancellation and bounded resource policies. None should share implicit global mutable UI state.

## Device identity and capability negotiation (proposed)

Treat a peer as a trusted identity plus a current set of addresses, not as a DNS-SD display name or IP address. Discovery should produce an **untrusted candidate**. Pairing should authenticate that candidate with a clear, user-verifiable action; exact ceremony and key storage remain unresolved. Sessions should establish trust before enabling sensitive operations.

After authentication, peers should negotiate a protocol version and only the capabilities both peers and their current OS/hardware support. Capability states should distinguish unavailable, permission-required, temporarily unavailable, supported, and active as useful to the UI. Do not infer a capability from a compiled module or display it as active until the service reports it.

## Proposed connection lifecycle

The following lifecycle is a design aid, not the current code's behavior:

```text
idle → discovering → candidate selected → pairing/trust decision
     → authenticating → negotiating capabilities → connected
     → reconnecting (bounded) → connected or failed/disconnected

Any active state → user cancellation / permission revocation / trust revocation
                  → cleanup → idle/disconnected
```

Transitions need timeouts, cancellation, error categories and idempotent cleanup. A reconnect must not bypass revoked trust or repeat a sensitive action silently. The current Android service accepts a socket and waits; the Linux UI has its own state; there is no shared lifecycle implementation.

## Transport and discovery boundaries

### Existing evidence

- Android calls `NsdManager` for `_phonedock._tcp` and binds a dynamically assigned TCP port.
- Linux browses `_phonedock._tcp.local.` with `zeroconf`.
- Windows uses Windows DNS service browsing for `_phonedock._tcp.local`.
- Android/Linux/Windows use separate socket APIs. No USB transport, manual connection form, persistent trust, or authentication was found.
- Current TCP code exchanges no defined hello/capability negotiation. The Android listener does not consume Linux input messages.

### Proposed separation

Use discovery to locate candidates and transport to move authenticated session records; never trust discovery metadata by itself. Specify local network interface, IPv4/IPv6, timeouts, port policy, multicast behavior and manual-connect behavior only after prototype testing across OSes. Keep USB as a separate adapter with explicit host/device permissions; don't silently treat ADB or driver prerequisites as universally available.

## Video and data pipelines

### Existing video attempt

1. Android requests user consent through MediaProjection and constructs a `ScreenStreamer`.
2. The streamer configures an AVC `MediaCodec`, attaches a virtual display, and calls back with output buffer bytes/timestamps/key-frame flags.
3. `ConnectionService` writes a 4-byte length plus 1-byte flag and payload to one active socket.
4. Linux parses a 4-byte length/type prefix and sends payloads to PyAV; Windows reads a similar prefix and has Media Foundation/Direct3D scaffolding.

These are source paths, not tested pipelines. Open questions include codec configuration/format changes, `BufferInfo` offsets, frame queue/backpressure, partial reads, size limits, decode timing, rotation, rendering, reconnect and output cleanup. Windows `VideoDecoder::Decode` and `Renderer::Present` are TODOs.

### Proposed future data flow

Capture/encode should be separate from transport and UI; the UI should consume decoded frames through a bounded, lifecycle-owned channel. File/content transfer should use separately typed, integrity-checked records and safe destinations rather than reusing video framing. Clipboard and notification flows need opt-in policy and per-feature privacy controls. No file, clipboard, notification, or media data pipeline was found.

## Error propagation and diagnostics

Return structured failures across discovery, pairing, transport, permission, codec, storage and rendering boundaries. Preserve actionable user messages while keeping protocol internals and sensitive content out of routine logs. Diagnostic events should use a documented schema, bounded retention, redaction, and explicit user controls. Current implementations primarily print/log exceptions or Android service messages; no shared error taxonomy or metrics system exists.

## UI and background work

UI layers should observe lifecycle-safe state and issue intent; they should not own long-lived sockets, encoders or retry loops. Background services need explicit cancellation and cleanup. Android `DashboardViewModel` currently toggles a local boolean instead of binding to `ConnectionService`; `VideoDecoderThread` starts a `QThread` but does not override `run`, so thread affinity needs review; the C++ entry point is a console program. These are implementation gaps, not architectural recommendations already applied.

## iOS project boundary planned for Phase 4

The iOS implementation is a real native-app phase, but no iOS project exists yet. At Phase 4 kickoff, create an Xcode project and real SwiftUI app/test targets; do not add a placeholder target in advance. Keep platform presentation and OS APIs native, and adapt to the protocol, trust and capability interfaces delivered by Phases 2–3 rather than inventing a separate wire protocol.

A small initial feature boundary should cover the app lifecycle, device discovery, explicit pairing/trust, session status and settings. Organize only code that exists—for example, `App`, `Devices`, `Pairing`, `Session`, `Settings`, platform/network adapters, shared domain models, app resources, `PhoneDockTests` and `PhoneDockUITests`. Use SwiftUI views for presentation and testable services/state objects for connection flows; do not create speculative packages merely to mirror this outline.

Treat screen capture/mirroring, remote input, background work, USB, clipboard/notifications, and local/inter-device networking as per-feature platform decisions, not shared capabilities. Apple's iOS 27 ScreenCaptureKit path is beta at the 2026-10-01 research snapshot; the current ReplayKit recording/broadcast references mark major APIs deprecated in iOS 27. Record supported OS range, user consent, declarations/entitlements, distribution/policy status, simulator-vs-hardware scope, and fallback in an ADR and [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md) before advertising any feature. Simulator verification is planned on macOS/Xcode; the borrowed-iPhone checklist in [ROADMAP.md](ROADMAP.md) remains the gate for physical-device claims. No iOS source or test result currently exists.

## macOS build host versus macOS product

macOS has two separate roles in the plan. Phase 4 uses official macOS/Xcode runners to build and test the iOS target in Apple's Simulator; this is build infrastructure, not a PhoneDock Mac application. Phase 9 is a separate native macOS product with its own app target, platform permissions, test destination, and support evidence. A runner or shared Swift source does not complete the Mac product, and the Mac app is not a prerequisite for iOS CI. No macOS app source/project exists today.

## Repository layout and migration policy

### Keep the existing applications in place

```text
android/               # existing Gradle/Kotlin Android app
desktop/               # existing Python/PySide6 Linux prototype
windows/               # existing C++ Windows prototype and driver scaffold
```

### Add only real responsibilities over time

```text
docs/                   # requirements, audit, architecture, security, tests, design
  decisions/            # reviewed ADRs only
.github/workflows/      # CI and version-tag release policy
scripts/                # repository checks and maintained build/release helpers

ios/                    # create the real SwiftUI app/test project at Phase 4; no placeholder before then
macos/                  # only when an actual Mac application is approved
web/                    # only when a maintained site/app is approved
shared/ or packages/    # only after a boundary, language and owner are justified
tests/                  # cross-platform fixtures only when there are real tests/assets
assets/                 # approved brand assets/tokens when design work produces them
```

Do not move existing apps to `apps/` merely to match a template. Do not create placeholder packages. Later moves must update project references, scripts, CI paths and docs in the same reviewed change. The precise target organization remains open.

## Architecture questions still unresolved

1. Which message format and protocol versioning strategy can be safely shared across Kotlin, Python, C++, Swift and a possible browser client?
2. What pairing ceremony, persistent device identifier and platform key store are appropriate?
3. Should transports use one encrypted channel or separately negotiated media/data channels, and which vetted libraries/APIs are available per target?
4. How should local discovery handle IPv6, multiple interfaces, guest networks, enterprise Wi-Fi, and manual address input?
5. What is the supported boundary between Android input control (ADB, accessibility, other APIs) and iOS capabilities?
6. Is Android-as-display on Windows technically maintainable without a signed driver; what is feasible on Linux/macOS?
7. What shared code is actually worth maintaining versus generated protocol fixtures and native adapters?
8. What supported OS/device matrix, performance targets, data-retention defaults and release channels should be promised?

Record resolved decisions under `docs/decisions/` with context, options, consequences and status; do not treat this proposed architecture as an ADR.


# PhoneDock

<p align="center">
  <strong>Your devices. One connected workspace.</strong>
</p>

<p align="center">
  Connect your Android phone, iPhone, Linux computer, Windows PC, and Mac through a unified, privacy-first device experience.
</p>

<p align="center">
  <em>Control. Transfer. Connect. Continue.</em>
</p>

---

> **Project status:** Revival and cross-platform development.
>
> PhoneDock is an existing project being reworked into a complete, cross-platform device ecosystem. Some components and prototypes already exist, but their current functionality, compatibility, and reliability must be verified against the source code. Features described as planned are not necessarily implemented.

## Table of Contents

- [1. Overview](#1-overview)
- [2. The Vision](#2-the-vision)
- [3. Supported Platforms](#3-supported-platforms)
- [4. Product Principles](#4-product-principles)
- [5. Feature Set](#5-feature-set)
- [6. Applications](#6-applications)
- [7. Design System](#7-design-system)
- [8. System Architecture](#8-system-architecture)
- [9. Device Connectivity](#9-device-connectivity)
- [10. Screen Streaming and Remote Control](#10-screen-streaming-and-remote-control)
- [11. File Transfer and Content Handoff](#11-file-transfer-and-content-handoff)
- [12. Clipboard and Notifications](#12-clipboard-and-notifications)
- [13. Second-Display Mode](#13-second-display-mode)
- [14. Security and Privacy](#14-security-and-privacy)
- [15. Performance and Reliability](#15-performance-and-reliability)
- [16. Diagnostics and Observability](#16-diagnostics-and-observability)
- [17. Repository Structure](#17-repository-structure)
- [18. Technology Strategy](#18-technology-strategy)
- [19. Development Setup](#19-development-setup)
- [20. Automated Builds and Releases](#20-automated-builds-and-releases)
- [21. Testing Strategy](#21-testing-strategy)
- [22. Accessibility and Internationalization](#22-accessibility-and-internationalization)
- [23. Development Roadmap](#23-development-roadmap)
- [24. Engineering Standards](#24-engineering-standards)
- [25. Contributing](#25-contributing)
- [26. Known Limitations](#26-known-limitations)
- [27. License](#27-license)

---

## 1. Overview

PhoneDock is a local-first, cross-platform device integration system designed to make physical devices work together as parts of one connected workspace.

It aims to bring phone control, screen mirroring, file transfer, clipboard synchronization, notifications, device discovery, content handoff, and other useful device interactions into a coherent product.

Instead of treating a phone and a computer as completely separate environments, PhoneDock allows compatible devices to discover one another, establish trusted connections, and exchange supported information and capabilities.

The product is designed around six application targets:

- Android mobile application
- iOS mobile application
- Linux desktop application
- Windows desktop application
- macOS desktop application
- Web application and product website

Not every feature is available on every platform. PhoneDock must detect actual operating-system capabilities, communicate limitations clearly, and provide useful alternatives where possible.

### The core idea

**Make your phone part of your computer. Make your computer part of your workflow.**

PhoneDock is not simply a screen-mirroring utility. It is a broader device integration platform built around local connectivity, thoughtful interaction design, security, and reliable engineering.

---

## 2. The Vision

Modern workflows frequently cross device boundaries.

A developer might work in an editor on a Linux laptop, receive a message on an Android phone, copy a code snippet from a computer to a mobile application, transfer a screenshot, and return to the desktop without wanting to manage five unrelated tools.

PhoneDock aims to make those transitions simpler.

### Example workflows

**Control your phone from your computer**

View a compatible Android device, interact with supported applications, type with a physical keyboard, and use the mouse for supported touch interactions.

**Move content between devices**

Send files, folders where supported, links, images, screenshots, and text without depending on a third-party cloud storage service.

**Share a clipboard**

Copy content on one supported device and make it available on another when clipboard permissions and platform restrictions allow it.

**Keep connected devices visible**

See paired devices, connection status, transfer activity, available capabilities, and relevant device information from one interface.

**Use your phone as an additional display**

Where supported, use an Android device as an additional computer display through a dedicated display-streaming and rendering subsystem.

**Continue across operating systems**

Provide a consistent PhoneDock identity across Android, iOS, Linux, Windows, and macOS while respecting the capabilities and conventions of each platform.

---

## 3. Supported Platforms

PhoneDock is intended to support the following platforms.

| Platform | Primary role | Implementation direction |
|---|---|---|
| Android | Primary phone-side companion | Native Android application |
| iOS | Apple mobile companion | Native iOS application |
| Linux | Desktop device management and control | Recover and improve the existing desktop implementation |
| Windows | Desktop device management and control | Complete the original Windows target |
| macOS | Desktop device management and control | First-class Mac application and distribution |
| Web | Website, documentation, downloads, release information, and supported browser-based utilities | Responsive web application |

The support matrix must distinguish between:

1. Planned functionality.
2. Implemented functionality.
3. Functionality verified by automated tests.
4. Functionality verified against real hardware.
5. Functionality unavailable because of operating-system restrictions.

A successful compilation does not prove that a feature works on a real device.

### Platform capability policy

Android and iOS are not interchangeable.

Android can permit screen capture, accessibility-mediated interactions, USB debugging integrations, and other functionality subject to permissions and device restrictions.

iOS imposes different restrictions on arbitrary screen capture, remote input injection, background execution, and system-level access.

PhoneDock must not promise equivalent capabilities where operating systems do not provide equivalent APIs.

The same principle applies to Linux, Windows, macOS, and browser-based functionality.

---

## 4. Product Principles

### 4.1 Local-first operation

Core device-to-device functionality should work over direct local connections wherever technically possible.

A mandatory cloud relay or user account should not be required for ordinary local pairing, screen streaming, and file exchange when the relevant devices and network support those operations.

Cloud infrastructure may be introduced for optional services, distribution, update delivery, or other explicitly documented capabilities. Such services must not silently become a requirement for features designed to work locally.

### 4.2 Privacy by default

Device connections must be authenticated. Sensitive operations must be visible and controllable. Users must be able to manage trusted devices and revoke access.

Screen streaming, clipboard synchronization, and notification forwarding must have explicit permission and privacy controls.

### 4.3 Native-feeling experiences

Each application should feel carefully designed for its operating system.

PhoneDock shares a common identity, interaction principles, terminology, and design tokens without forcing identical interfaces onto platforms with different conventions.

### 4.4 Real implementations

A button must perform its advertised action. A settings control must affect actual behavior. A displayed connection status must reflect the real connection state.

Mock data, simulated success, placeholder screens, and nonfunctional controls must not be presented as completed features.

### 4.5 Observable engineering

Performance, reliability, and compatibility should be measured.

The project should include automated checks, meaningful diagnostics, reproducible builds, documented architectural decisions, and tests against real devices wherever practical.

### 4.6 Incremental delivery

Work is divided into explicit development phases. Each phase has defined deliverables, platform responsibilities, tests, and acceptance criteria.

Large changes must be implemented in coherent increments rather than through uncontrolled rewrites.

---

## 5. Feature Set

The following is the intended product scope. Individual features remain subject to implementation, platform support, security review, and testing.

### 5.1 Device discovery and connection

- Automatic discovery on compatible local networks.
- Manual IP or host-based connection where supported.
- USB connectivity on supported platforms.
- First-time device pairing.
- Authenticated connection establishment.
- Trusted-device management.
- Device capability negotiation.
- Connection status and history.
- Connection cancellation and disconnection.
- Reconnection after temporary failures.
- Useful connection diagnostics.
- Multiple paired devices.
- Clear distinction between paired, reachable, connecting, connected, and disconnected states.

### 5.2 Screen mirroring

- View a compatible Android device on a desktop.
- Maintain the phone's aspect ratio.
- Support fit-to-window and native-resolution viewing modes.
- Provide configurable streaming quality.
- Support adaptive resolution or bitrate where appropriate.
- Use hardware-accelerated encoding and decoding when available.
- Provide graceful fallbacks.
- Expose performance information in a diagnostic view.
- Handle device rotation, screen changes, and connection interruptions.

### 5.3 Remote control

- Mouse-based touch interaction where permitted.
- Tap, double-tap, long-press, drag, and scroll where supported.
- Keyboard text input through an appropriate supported mechanism.
- Navigation controls where permitted.
- Correct coordinate mapping between the rendered screen and physical device.
- Keyboard shortcut handling where appropriate.
- Clear capability indicators when a device cannot support a requested operation.
- Explicitly document operations that require ADB, Accessibility Services, or additional permissions.

### 5.4 Clipboard synchronization

- Optional computer-to-phone clipboard sharing.
- Optional phone-to-computer clipboard sharing.
- User-controlled synchronization.
- Loop prevention and duplicate-change detection.
- Text-size limits and sensible handling of unsupported content.
- Sensitive-content safeguards where practical.
- Clear indicators showing whether synchronization is enabled.
- Error reporting when the operating system blocks an operation.

Clipboard synchronization must never be enabled in a way that silently overrides user expectations.

### 5.5 File transfer

- Send files between compatible devices.
- Receive files into user-selected locations.
- Transfer queues.
- Progress reporting.
- Cancellation.
- Large-file support.
- Transfer integrity verification.
- Interrupted-transfer recovery where feasible.
- Safe filename and path handling.
- Destination confirmation where appropriate.
- Conflict handling for existing files.
- Drag-and-drop on supported desktop environments.
- Folder transfer where supported.
- Searchable transfer history.
- Retry options when the source content remains available.

### 5.6 Content handoff

- Send a web link from a computer to a phone.
- Send a link from a phone to a computer.
- Share text snippets.
- Share images and screenshots where supported.
- Provide a clear destination-device selector.
- Allow users to review content before transferring it.
- Handle unsupported content types gracefully.

### 5.7 Notifications

- Forward supported Android notifications to a paired desktop.
- Allow users to select which applications may be forwarded.
- Provide privacy controls for sensitive notification content.
- Support notification dismissal or actions only where the platform and originating application permit them.
- Handle permission revocation.
- Avoid exposing notification content in diagnostic logs.

Notification mirroring is capability-dependent. PhoneDock must not assume that iOS exposes unrestricted notifications from other applications.

### 5.8 Device information and media

Where supported, PhoneDock may display:

- Device name and model.
- Operating-system version.
- Connection type.
- Battery status.
- Connection quality.
- Active transfer count.
- Media playback status.
- Supported playback controls.
- Screen dimensions and orientation.
- Available device capabilities.

Information should be displayed only when it can be obtained reliably and with appropriate permissions.

### 5.9 Device management

- Add and remove trusted devices.
- Rename locally displayed devices.
- View supported capabilities.
- Manage per-device permissions.
- Disconnect active sessions.
- Review recent transfers.
- Inspect connection errors.
- Configure privacy behavior.
- Configure startup and background behavior where supported.

### 5.10 Diagnostics

- Connection lifecycle inspection.
- Discovery status.
- Pairing and authentication status.
- Transport status.
- Video pipeline status.
- Encoder and decoder information.
- Round-trip time where measurable.
- Frame rate and dropped-frame metrics.
- Transfer progress and failure information.
- Relevant permission status.
- Exportable diagnostic reports with sensitive data excluded by default.

### 5.11 Second-display mode

- Use a compatible Android device as an additional display for a computer.
- Support resolution and orientation configuration where possible.
- Support display positioning and configuration through the host operating system.
- Optimize video encoding, transport, and rendering.
- Recover from network interruptions.
- Report unsupported host configurations clearly.

This is a separate subsystem, not merely another screen-mirroring setting.

---

## 6. Applications

### 6.1 Android application

The Android application is the primary mobile companion for device integration.

Responsibilities include:

- First-run onboarding.
- Device pairing and connection management.
- Screen capture through supported Android APIs.
- Required foreground services and user-visible capture indicators.
- Supported remote-input mechanisms.
- File sending and receiving.
- Clipboard-related interactions where supported.
- Optional notification forwarding.
- Device identity and capability reporting.
- Network discovery.
- Permission management.
- Connection recovery.
- Privacy controls.
- Diagnostic information.

The application should remain useful when certain permissions are unavailable. It must explain what is missing instead of presenting misleading success states.

### 6.2 iOS application

The iOS application is a native companion designed around public Apple APIs and iOS interaction conventions.

Potential responsibilities include:

- Device discovery and pairing where supported.
- Connection status.
- Sending and receiving files through supported mechanisms.
- Content handoff.
- Device management.
- Supported clipboard interactions.
- Transfer history.
- Privacy settings.
- Connection diagnostics.
- Supported background and foreground workflows.

The iOS app must account for background execution restrictions, local-network permissions, sandboxing, and platform-specific APIs.

Features requiring unavailable system privileges must not be implemented through unsupported workarounds.

### 6.3 Linux desktop application

The Linux application provides device management, screen viewing, supported remote control, file transfer, and other desktop functionality.

The existing Python/PySide6 implementation and PyAV video-decoding work should be audited before major changes.

The application should aim to provide:

- A polished desktop interface.
- USB and local-network connection support where implemented.
- Reliable screen rendering.
- Keyboard and mouse integration.
- File-transfer workflows.
- Clipboard and notification integration where supported.
- Diagnostics.
- Linux-appropriate packaging.
- Compatibility documentation for supported desktop environments.

Packaging targets may include AppImage, Flatpak, or distribution packages, depending on dependency compatibility and release requirements.

### 6.4 Windows desktop application

The Windows application continues the original project direction.

It should provide:

- Device discovery and pairing.
- USB and Wi-Fi connections.
- Screen mirroring.
- Supported remote control.
- Clipboard synchronization.
- File transfer.
- Notification forwarding where supported.
- Device and session management.
- Diagnostics.
- Second-display host functionality.
- Installable, versioned release artifacts.

The existing Windows folder and prototypes must be inspected before deciding which components to preserve.

### 6.5 macOS desktop application

macOS is a first-class desktop target, not an afterthought.

The application should provide:

- Device discovery and pairing.
- Supported USB and network connectivity.
- Screen mirroring and remote control where supported.
- File transfer and content handoff.
- Clipboard integration.
- Device management.
- Appropriate menu-bar and keyboard-shortcut behavior.
- macOS window and lifecycle integration.
- Diagnostics.
- Signed and notarized distribution when the required Apple credentials are available.

The implementation must be tested on macOS runners and, where practical, real Apple hardware.

### 6.6 Web application and website

The web experience supports the wider PhoneDock product.

Its responsibilities may include:

- Product landing page.
- Platform and compatibility information.
- Documentation.
- Download pages.
- Release history and release notes.
- Installation instructions.
- Troubleshooting.
- Security and privacy documentation.
- Supported browser-based utilities.
- Optional local-network workflows that are feasible under browser security restrictions.

The web application must not pretend that a normal browser has the same permissions as a native desktop application.

Any browser-based device interaction must explicitly identify its prerequisites and limitations.

A public website or documentation page must remain usable without requiring a PhoneDock account unless a future, separately specified service genuinely needs one.

---

## 7. Design System

PhoneDock must have a recognizable identity across all applications.

### 7.1 Visual direction

The visual direction combines:

- Apple-inspired material depth.
- Carefully controlled translucent surfaces.
- Subtle borders and layered elevation.
- Clean typography.
- Generous spacing.
- Smooth, purposeful transitions.
- Responsive interaction feedback.
- Clear information hierarchy.
- Excellent light and dark appearances.

The goal is a professional application, not a collection of generic SaaS cards.

### 7.2 Liquid Glass-inspired interfaces

The Android application may use a Liquid Glass-inspired aesthetic through Jetpack Compose, translucent surfaces, restrained blur, layered components, and fluid animations.

The iOS application should use native SwiftUI materials and Apple's Liquid Glass APIs where available and appropriate for the deployment target.

Desktop applications may adopt platform-appropriate translucency and depth without sacrificing readability, performance, accessibility, or OS conventions.

The visual treatment must adapt gracefully to devices that do not support a particular effect.

### 7.3 Initial brand direction

The proposed brand direction is:

- **Primary:** deep indigo-blue.
- **Accent:** electric ice blue.
- **Light surfaces:** soft porcelain.
- **Dark surfaces:** deep ink.
- **Material treatment:** restrained glass, fine borders, subtle depth.
- **Typography:** native system typography with a consistent hierarchy.
- **Iconography:** a consistent custom icon family.

The final palette, typography, spacing, icon rules, logo geometry, and component tokens must be documented in `docs/DESIGN_SYSTEM.md`.

### 7.4 Logo

The logo should be distinctive, legible at small sizes, and recognizable in application icons, desktop title bars, websites, and mobile home screens.

The initial creative direction is a minimal geometric symbol that combines the idea of a phone with a dock, connection, or shared workspace.

The implementation should include suitable vector assets, application icons, and light/dark variants where needed.

The final logo must be an intentional design decision, not an arbitrary Unicode symbol or emoji.

### 7.5 Interaction quality

Every application must account for:

- Loading and connecting states.
- Empty states.
- Permission-denied states.
- Disconnected states.
- Retry and recovery states.
- Success and failure feedback.
- Keyboard navigation where applicable.
- Reduced-motion preferences.
- Appropriate touch targets.
- Responsive layouts.
- Accessibility labels.
- Light and dark themes.

Animations must communicate state changes and support usability rather than obstructing tasks.

---

## 8. System Architecture

PhoneDock consists of platform-specific applications connected through a shared protocol and a set of reusable engineering components.

The architecture should separate user interfaces from connection logic, device capabilities, transport, and data handling.

### Conceptual architecture

```text
                    PHONEDOCK ECOSYSTEM

  Android       iOS        Linux       Windows       macOS
  Mobile       Mobile     Desktop      Desktop      Desktop
     \            |           |           |            /
      \           |           |           |           /
       +----------+-----------+-----------+----------+
                              |
                    Shared protocol contract
                              |
             +----------------+----------------+
             |                |                |
          Discovery        Sessions          Security
             |                |                |
             +----------------+----------------+
                              |
                     Transport adapters
                       /             \
                    USB            Local network
                       \             /
                        Device bridge
                              |
                   Streaming and data channels

                 Web application / website
             Documentation, downloads, support
```

This diagram describes logical responsibilities, not a requirement that every component run in one process.

### Architecture requirements

- The protocol must not depend on a particular UI framework.
- Platform-specific APIs must be isolated behind well-defined interfaces.
- Device capabilities must be negotiated rather than assumed.
- Connection state must be represented explicitly.
- Data channels must have documented message types and error behavior.
- Network and USB transports must share a coherent session model where appropriate.
- Video streaming must not block the UI thread.
- File transfer must not require loading entire files into memory.
- Long-running work must be cancellable where practical.
- Errors must retain enough context for diagnosis without exposing sensitive content.
- Shared protocol changes must be versioned and tested against compatibility expectations.

### Architecture decisions

Significant architectural decisions must be documented in Architecture Decision Records.

Each record should describe the problem, alternatives, evidence, trade-offs, decision, and verification plan.

---

## 9. Device Connectivity

### USB

USB should provide a direct connection where the operating system, device, drivers, and Android configuration support it.

USB implementation must account for platform-specific permissions and transport differences.

ADB may be used for appropriate Android workflows, but it must not be assumed to be available to ordinary users without the required setup.

### Local Wi-Fi

Devices may connect through the same local network.

The connection system should support:

- Automatic discovery where available.
- Manual connection details as a fallback.
- Network changes.
- Interrupted connections.
- Device sleep and wake.
- Connection timeout and cancellation.
- Reconnection attempts.
- Clear diagnostics when network isolation prevents communication.

The local network may not provide direct device-to-device communication even when both devices have internet access.

### Pairing and trust

The first connection should establish trust through an explicit pairing flow.

The system must not automatically trust every device found on a network.

Pairing should establish an authenticated device identity and the permissions associated with a trusted relationship.

Users must be able to revoke trust and disconnect devices.

### Session lifecycle

```text
Discovery
    |
    v
Pairing
    |
    v
Authentication
    |
    v
Capability negotiation
    |
    v
Session establishment
    |
    v
Connected
    |
    +------> Temporary interruption
    |                  |
    |                  v
    |             Reconnection
    |                  |
    +<-----------------+
    |
    v
Disconnected / Revoked
```

The implementation must handle failures at each stage without incorrectly displaying the device as connected.

---

## 10. Screen Streaming and Remote Control

### Screen-streaming pipeline

```text
Android display
      |
      v
Screen capture API
      |
      v
Video encoding
      |
      v
Authenticated transport
      |
      v
Desktop video decoder
      |
      v
Video rendering surface
```

The pipeline should minimize unnecessary copies, format conversions, and buffering.

Hardware acceleration should be used where supported and verified, with documented fallbacks.

### Input pipeline

```text
Desktop input
      |
      v
Input mapping
      |
      v
Capability and permission checks
      |
      v
Authenticated input channel
      |
      v
Supported Android input mechanism
```

Input injection must use legitimate, supported mechanisms and clearly document any additional setup required.

The system must not report successful remote control when the input operation has not actually occurred.

### Performance goals

Performance targets should be established through benchmarks rather than assumed values.

Measurements should include:

- End-to-end interaction latency.
- Round-trip time where measurable.
- Video frame rate.
- Dropped frames.
- Bitrate.
- CPU and memory usage.
- Encoder and decoder behavior.
- Reconnection time.
- Transfer throughput.

Initial targets should be documented after measuring the baseline on representative hardware.

---

## 11. File Transfer and Content Handoff

File transfer is a core PhoneDock capability.

The system should support reliable, observable transfers without requiring cloud storage for ordinary local operation.

### Requirements

- Explicit source and destination devices.
- Clear transfer progress.
- Cancellation and failure reporting.
- Integrity verification.
- Safe handling of file names and paths.
- Large-file streaming.
- Appropriate disk-space checks.
- Duplicate and conflict handling.
- Interrupted-transfer recovery where feasible.
- User-selected destination locations.
- Transfer history.
- Privacy-conscious logs.

### Content handoff

Text, links, and supported media can be sent between compatible devices.

Content handoff should use a clear destination selector and provide confirmation of the actual transfer result.

The feature must not silently upload content to a cloud service.

---

## 12. Clipboard and Notifications

### Clipboard

Clipboard synchronization must be optional and explicit.

It must prevent synchronization loops and account for applications and operating systems that restrict clipboard access.

Sensitive information must not be unnecessarily retained, logged, or synchronized.

### Notifications

Notification forwarding should be opt-in, configurable per application where supported, and designed to avoid unnecessary exposure of private information.

Actions such as dismissal or reply are available only where the operating system and originating application permit them.

---

## 13. Second-Display Mode

PhoneDock's second-display mode is an advanced feature intended to make a compatible Android device function as an additional display for a supported computer.

It requires a dedicated architecture for:

- Host display configuration.
- Display capture or virtual-display output.
- Encoding and transport.
- Android-side decoding and rendering.
- Resolution and orientation.
- Display positioning.
- Input behavior where applicable.
- Connection recovery.
- Performance monitoring.

The exact implementation depends on the host operating system and its supported display APIs.

This feature must be developed and tested separately from ordinary phone mirroring.

It must not be marked complete simply because a desktop screen can be streamed into a mobile window.

---

## 14. Security and Privacy

Security is a fundamental product requirement.

### Minimum expectations

- Authenticated device pairing.
- Encrypted communication for sensitive device sessions.
- Secure identity and key handling.
- Explicit trust and revocation.
- Least-privilege access.
- User-controlled sensitive capabilities.
- Safe file handling.
- Input validation.
- Protection against unauthorized session establishment.
- No hardcoded production credentials.
- No unnecessary transmission of device content.
- Privacy-conscious diagnostic logs.
- Documented security assumptions.
- Dependency vulnerability checks.
- A documented threat model.

### Local-first does not mean automatically secure

A local network is not inherently trusted.

PhoneDock must authenticate peers and protect sensitive sessions even when both devices are on the same Wi-Fi network.

The protocol should use established cryptographic libraries and secure transport mechanisms rather than inventing its own encryption scheme.

### Privacy controls

Users should be able to:

- Disable clipboard synchronization.
- Disable notification forwarding.
- Stop active screen sharing.
- Remove trusted devices.
- Disconnect sessions.
- Control available permissions.
- Inspect active connections.
- Clear appropriate local history.
- Understand which features require network access.

---

## 15. Performance and Reliability

PhoneDock should be designed for repeated daily use.

### Performance

- Keep rendering responsive.
- Avoid blocking UI threads.
- Use streaming and bounded buffering.
- Avoid loading entire large files into memory.
- Use hardware acceleration where practical.
- Measure resource usage.
- Make quality settings understandable.
- Degrade gracefully on slower devices and networks.

### Reliability

- Recover from temporary network interruption.
- Handle application suspension and resume.
- Handle device sleep and wake.
- Detect stale sessions.
- Cancel operations safely.
- Preserve transfer integrity.
- Report failures with actionable explanations.
- Avoid silent data loss.
- Avoid retry loops that consume excessive resources.

### Compatibility

Supported devices, operating systems, and known restrictions should be documented.

Compatibility claims must be supported by actual builds, tests, or hardware verification.

---

## 16. Diagnostics and Observability

PhoneDock should explain failures instead of returning only a generic error.

The diagnostic system should report relevant states such as:

- Device discovery.
- Pairing.
- Authentication.
- Transport.
- Session establishment.
- Video encoding and decoding.
- Input capability.
- Clipboard permission.
- Transfer status.
- Reconnection.
- Platform-specific dependencies.

Diagnostics should provide suggested next steps when possible.

Sensitive clipboard content, notification bodies, file contents, authentication tokens, and private keys must not appear in ordinary logs.

Debug logging should be configurable and documented.

---

## 17. Repository Structure

The final repository layout must be based on an audit of the existing project.

The following is the intended logical organization, not permission to delete or blindly move existing files.

```text
PhoneDock/
|
|-- README.md
|-- LICENSE
|-- CONTRIBUTING.md
|-- SECURITY.md
|-- .gitignore
|-- .editorconfig
|
|-- apps/
|   |
|   |-- android/
|   |   |-- app/
|   |   |-- README.md
|   |
|   |-- ios/
|   |   |-- PhoneDock/
|   |   |-- PhoneDock.xcodeproj/
|   |   |-- README.md
|   |
|   |-- linux/
|   |   |-- README.md
|   |
|   |-- windows/
|   |   |-- README.md
|   |
|   |-- macos/
|   |   |-- README.md
|   |
|   |-- web/
|       |-- README.md
|
|-- packages/
|   |
|   |-- protocol/
|   |-- device-core/
|   |-- discovery/
|   |-- transport/
|   |-- security/
|   |-- diagnostics/
|   |-- design-tokens/
|
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- PRODUCT_SPEC.md
|   |-- DESIGN_SYSTEM.md
|   |-- PLATFORM_SUPPORT.md
|   |-- PROTOCOL.md
|   |-- SECURITY.md
|   |-- ROADMAP.md
|   |-- TESTING.md
|   |
|   |-- decisions/
|   |
|   |-- development/
|   |
|   |-- platform-guides/
|
|-- assets/
|   |-- brand/
|   |-- icons/
|   |-- screenshots/
|
|-- tests/
|   |-- protocol/
|   |-- integration/
|   |-- fixtures/
|
|-- scripts/
|   |-- development/
|   |-- build/
|   |-- release/
|
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |-- workflows/
|
|-- CHANGELOG.md
```

### Structure rules

- Preserve existing source code until its purpose and dependencies are understood.
- Keep platform-specific code in platform-appropriate modules.
- Share protocol contracts and portable logic where it makes engineering sense.
- Do not create empty packages simply to match a diagram.
- Do not move files merely to make the repository look more organized.
- Document build instructions for each maintained application.
- Keep generated artifacts out of version control unless explicitly required.
- Ensure all structure and documentation reflect the actual repository.

---

## 18. Technology Strategy

PhoneDock must use technologies that are appropriate for the product and the platforms it supports.

The final stack should be decided after reviewing the existing implementation and documenting the relevant trade-offs.

### Android

Preferred direction: Kotlin, Android SDK, Jetpack Compose, and supported Android platform APIs.

Existing working code should be preserved where it is technically sound.

### iOS

Preferred direction: Swift, SwiftUI, and public Apple APIs.

The implementation should use native Apple interaction patterns and Liquid Glass capabilities when supported by the target OS.

### Desktop

The existing Linux implementation uses Python, PySide6, and PyAV according to the original project documentation.

Those technologies should be assessed before considering a rewrite.

Windows and macOS must have a documented, tested implementation strategy. A shared codebase is desirable where it reduces maintenance without sacrificing reliability or platform integration.

### Shared components

A shared protocol and portable core should reduce duplication across applications.

Rust is a candidate for performance-sensitive, portable components if the existing architecture justifies it. It is not a mandatory rewrite target.

### Web

Use a maintained web stack suited to the actual product requirements, with responsive design, accessibility, automated checks, and reproducible builds.

### Technology decision policy

Before adopting a major framework or replacing a working implementation, document:

1. The problem being solved.
2. The current implementation.
3. The alternatives.
4. Platform compatibility.
5. Maintenance cost.
6. Performance implications.
7. Migration risks.
8. A verification plan.

---

## 19. Development Setup

Development prerequisites depend on the application being worked on.

### Android

- Android Studio.
- A compatible JDK.
- Android SDK and required build tools.
- An emulator or supported physical Android device.

### iOS and macOS

- macOS.
- Xcode and the required SDKs.
- Appropriate signing configuration for the intended distribution method.
- Physical Apple hardware for real-device testing where necessary.

### Linux

- A supported Python environment if the existing PySide6 application remains in use.
- Project-specific Python dependencies.
- Video and multimedia dependencies required by the implementation.
- Platform development libraries needed for packaging.

### Windows

- The build tools required by the selected implementation.
- Relevant Windows SDKs and dependencies.
- A supported Android device for integration testing.

### Web

- The selected runtime and package manager.
- Dependencies specified by the web application.
- A supported development browser.

### General setup

The root README must provide accurate, executable instructions for the actual repository.

Each application should have a focused README covering prerequisites, installation, development, testing, and known limitations.

Do not invent commands for applications that have not yet been implemented.

---

## 20. Automated Builds and Releases

PhoneDock should use GitHub Actions for continuous integration and controlled release automation.

### Pull-request checks

Where applicable, workflows should:

- Validate formatting.
- Run linting and static analysis.
- Run unit tests.
- Build affected applications.
- Validate documentation and repository conventions.
- Check dependency and security issues.
- Report failures clearly.

### Platform builds

The release system should use suitable runners for each platform.

| Target | Intended automated output |
|---|---|
| Linux | Supported Linux package or distributable |
| Windows | Windows installer or distributable |
| macOS | macOS application package or archive |
| Android | Android build artifact, with signed distribution where configured |
| iOS | Build and test through macOS runners; distribution when Apple signing is configured |
| Web | Tested production build and deployment where configured |

The actual artifact formats depend on the selected technology stack.

### Versioning and releases

The project should adopt a documented versioning convention.

A tagged release should:

1. Validate the tag and version.
2. Run the relevant tests.
3. Build the applicable targets.
4. Produce versioned artifacts.
5. Generate checksums where appropriate.
6. Publish release notes.
7. Attach available artifacts to a GitHub Release.
8. Clearly report any platform build that could not be produced.

Signing and notarization must be performed only when the necessary certificates, credentials, and configuration are available.

### Dependency maintenance

Automated dependency updates should be reviewed and tested before merging.

Scheduled CI should detect build regressions and dependency issues without blindly upgrading every dependency.

### Application updates

Building and publishing a new version does not automatically update installed copies.

Secure in-app update checks and automatic installation, if introduced, must have a separate design covering artifact verification, platform rules, user consent, and recovery.

---

## 21. Testing Strategy

Testing must cover both shared components and real platform behavior.

### Unit tests

- Protocol message validation.
- Device identity handling.
- Connection-state transitions.
- Capability negotiation.
- Transfer calculations.
- Retry and cancellation behavior.
- Security-related validation.
- Design-system and application logic where applicable.

### Integration tests

- Discovery.
- Pairing.
- Authentication.
- Connection establishment.
- Session interruption and recovery.
- File-transfer integrity.
- Clipboard loop prevention.
- Protocol compatibility.
- Error propagation.

### Platform tests

- Linux builds and supported desktop environments.
- Windows builds and relevant system integration.
- macOS builds and supported OS versions.
- Android permission and lifecycle behavior.
- iOS sandbox and background behavior.
- Browser compatibility for supported web features.

### Hardware tests

Where practical, test against real Android devices and supported computers.

Emulator success is useful but does not prove compatibility with all physical devices.

### Reliability tests

- Network interruption.
- Device sleep and wake.
- Application restart.
- Invalid pairing attempts.
- Permission revocation.
- Interrupted transfers.
- Large files.
- Slow networks.
- Unsupported capabilities.
- Disk-space and destination errors.

### Acceptance criteria

A feature is complete only when:

- The implementation exists.
- Relevant tests pass.
- Failure states are handled.
- Documentation is updated.
- Supported platforms are identified.
- Limitations are documented.
- Claims about real-device behavior are supported by evidence.

---

## 22. Accessibility and Internationalization

PhoneDock should support users with different accessibility needs.

The applications should consider:

- Appropriate contrast.
- Readable typography.
- Scalable layouts.
- Screen-reader labels.
- Keyboard navigation on desktop.
- Visible focus indicators.
- Reduced-motion preferences.
- Accessible touch targets.
- Meaningful error messages.
- Localization-ready strings.
- Date, time, and number formatting appropriate to the locale.

Translucent materials and decorative effects must never take precedence over readable content.

---

## 23. Development Roadmap

The roadmap defines the intended sequence of development.

The completion status of each phase must be based on verified repository state and acceptance criteria, not on the existence of a folder, mockup, or prototype.

### Phase 0 — Repository Recovery and Project Foundation

- [ ] Inspect the complete repository.
- [ ] Identify existing Android, Windows, Linux, and other application code.
- [ ] Record working, partial, planned, and unverified features.
- [ ] Identify the actual build systems and dependencies.
- [ ] Document the current architecture and technical risks.
- [ ] Replace the outdated README with the complete product specification.
- [ ] Establish the documentation structure.
- [ ] Document the proposed repository organization.
- [ ] Establish initial GitHub Actions checks compatible with the existing stack.
- [ ] Add or improve repository conventions and contribution guidance.
- [ ] Create a phase-by-phase roadmap with explicit acceptance criteria.

**Exit condition:** The project has an accurate source-of-truth specification, a verified baseline, actionable documentation, and working foundational automation.

### Phase 1 — Brand, Design System, and Architecture

- [ ] Finalize the logo and brand assets.
- [ ] Finalize colors, typography, spacing, icons, and material rules.
- [ ] Define light and dark appearances.
- [ ] Define platform-specific interaction guidelines.
- [ ] Document system boundaries and shared components.
- [ ] Define the device capability model.
- [ ] Define connection and session states.
- [ ] Document the protocol and versioning strategy.
- [ ] Establish architectural decision records.
- [ ] Define accessibility and performance standards.

**Exit condition:** The brand and architecture are documented well enough to guide implementation across all applications.

### Phase 2 — Cross-Platform Engineering Foundation

- [ ] Establish maintainable application boundaries.
- [ ] Preserve working implementations.
- [ ] Establish supported build configurations.
- [ ] Define shared protocol contracts.
- [ ] Implement or formalize connection-state handling.
- [ ] Establish device identity and capability negotiation.
- [ ] Add initial unit and integration tests.
- [ ] Establish CI for implemented targets.
- [ ] Document platform prerequisites.

**Exit condition:** The core architecture builds and tests reproducibly, with documented interfaces and platform boundaries.

### Phase 3 — Desktop Experience and Connection Lifecycle

- [ ] Build the device-management interface.
- [ ] Implement onboarding and connection setup.
- [ ] Implement discovery and manual connection.
- [ ] Implement pairing and authentication.
- [ ] Display accurate connection states.
- [ ] Add trusted-device management.
- [ ] Add useful error messages and diagnostics.
- [ ] Implement the supported workflow across Linux, Windows, and macOS.

**Exit condition:** A compatible device can be paired and connected through a tested desktop workflow.

### Phase 4 — Android Companion and Screen Streaming

- [ ] Refine Android onboarding and permissions.
- [ ] Establish device identity and capabilities.
- [ ] Implement or stabilize screen capture.
- [ ] Implement or stabilize video encoding and transport.
- [ ] Implement desktop decoding and rendering.
- [ ] Support resolution and orientation changes.
- [ ] Add streaming-quality controls.
- [ ] Measure latency and resource usage.
- [ ] Verify behavior on real Android devices.

**Exit condition:** Supported Android devices can stream their screens to compatible desktop clients with observable performance and clear failure handling.

### Phase 5 — Remote Control and USB Connectivity

- [ ] Implement supported mouse and keyboard input.
- [ ] Implement coordinate mapping.
- [ ] Add supported navigation operations.
- [ ] Complete USB transport on supported platforms.
- [ ] Document ADB and permission requirements.
- [ ] Test input restrictions and failure behavior.
- [ ] Verify USB and Wi-Fi connection recovery.

**Exit condition:** Supported devices can be controlled through verified input mechanisms and documented connection methods.

### Phase 6 — File Transfer and Content Handoff

- [ ] Implement send and receive workflows.
- [ ] Add transfer queues and progress.
- [ ] Add cancellation and integrity checks.
- [ ] Handle interrupted transfers.
- [ ] Add destination selection and conflict handling.
- [ ] Implement link and text handoff.
- [ ] Add transfer history.
- [ ] Test large-file behavior and error recovery.

**Exit condition:** Supported devices exchange files and content reliably, with verifiable results.

### Phase 7 — Clipboard, Notifications, and Device Integration

- [ ] Implement optional clipboard synchronization.
- [ ] Prevent clipboard loops.
- [ ] Add privacy controls.
- [ ] Implement supported notification forwarding.
- [ ] Add per-app notification permissions where possible.
- [ ] Add supported media controls.
- [ ] Add device information and status.
- [ ] Test permission revocation and lifecycle changes.

**Exit condition:** Supported integration features work with explicit controls and documented platform restrictions.

### Phase 8 — iOS Companion

- [ ] Establish the native SwiftUI application.
- [ ] Implement the shared design language using native iOS materials.
- [ ] Implement supported device discovery and pairing.
- [ ] Implement supported file exchange.
- [ ] Implement content handoff.
- [ ] Add device management and transfer history.
- [ ] Add supported clipboard functionality.
- [ ] Implement permission and lifecycle handling.
- [ ] Build and test on appropriate Apple runners.
- [ ] Verify supported functionality on real iOS hardware.

**Exit condition:** The iOS companion provides a tested, genuinely supported feature set and does not promise unavailable system capabilities.

### Phase 9 — Web Application and Product Website

- [ ] Establish the responsive web experience.
- [ ] Publish product and platform information.
- [ ] Add installation and troubleshooting guides.
- [ ] Publish downloads and release notes.
- [ ] Add browser-compatible utilities where useful.
- [ ] Add accessibility and responsive-layout testing.
- [ ] Configure production builds and deployment.

**Exit condition:** Users can discover PhoneDock, understand compatibility, find documentation, and obtain available releases.

### Phase 10 — Second-Display Mode

- [ ] Define host-specific display architecture.
- [ ] Implement supported host display output.
- [ ] Implement Android-side receiving and rendering.
- [ ] Add resolution and orientation handling.
- [ ] Add display configuration.
- [ ] Optimize encoding and transport.
- [ ] Implement interruption recovery.
- [ ] Benchmark latency and image quality.
- [ ] Verify actual extended-display behavior.

**Exit condition:** A supported host operating system can use a compatible Android device as a genuine additional display, with verified configuration and performance.

### Phase 11 — Production Hardening and Release

- [ ] Complete the security review.
- [ ] Validate trusted-device revocation.
- [ ] Run compatibility and reliability tests.
- [ ] Establish release versioning.
- [ ] Complete platform build workflows.
- [ ] Configure signing and notarization where possible.
- [ ] Produce versioned release artifacts.
- [ ] Document installation and updates.
- [ ] Publish supported-platform information.
- [ ] Prepare release notes and troubleshooting guidance.

**Exit condition:** PhoneDock has reproducible builds, documented compatibility, tested core workflows, and a maintainable release process.

---

## 24. Engineering Standards

All contributors and coding agents must follow these standards.

### Inspect before changing

Read the relevant source files, build configuration, dependencies, and tests before making changes.

### Preserve working functionality

Do not replace a working implementation simply because another framework is more fashionable.

### Implement real behavior

Do not leave placeholder buttons, mocked success messages, or incomplete handlers while claiming that a feature is complete.

### Test the affected system

Run relevant formatting, linting, tests, and builds. Report checks that could not run and explain why.

### Keep documentation synchronized

Update the README, architecture documents, platform support matrix, and feature status when implementation changes.

### Respect platform boundaries

Do not assume that Android, iOS, Linux, Windows, macOS, and browser APIs behave identically.

### Avoid unnecessary dependencies

Every new dependency must have a clear purpose and an acceptable maintenance and security profile.

### Report honestly

Distinguish verified results from assumptions, prototypes, and planned work.

### Use coherent pull requests

Each development phase should produce a meaningful, reviewable body of work with tests and documentation. Do not fragment tightly related changes into unnecessary pull requests.

---

## 25. Contributing

Contributions are welcome once the project's contribution and licensing requirements have been established.

Before submitting a pull request:

1. Review the relevant architecture and platform documentation.
2. Follow the project's formatting and testing conventions.
3. Keep changes focused on the intended milestone.
4. Update documentation where behavior changes.
5. Include reproduction steps for bug fixes.
6. Identify platforms that were tested.
7. Document known limitations.
8. Avoid committing credentials, private data, generated build artifacts, or unrelated changes.

Bug reports should include, where relevant:

- PhoneDock version.
- Host operating system and version.
- Android or iOS version.
- Device model.
- Connection method.
- Steps to reproduce.
- Expected behavior.
- Actual behavior.
- Relevant sanitized diagnostic output.

---

## 26. Known Limitations

PhoneDock operates within the permissions and capabilities provided by each operating system.

Potential limitations include:

- Android screen capture requires appropriate user authorization.
- Remote input may require ADB, Accessibility Services, or other supported mechanisms.
- iOS restricts arbitrary screen capture, input injection, background execution, and system-level access.
- USB support depends on device, operating system, transport, and permission requirements.
- Local networks may block peer-to-peer traffic or multicast discovery.
- Hardware video acceleration varies across devices and drivers.
- Notification access and actions differ between platforms.
- Second-display functionality requires host-specific display integration.
- macOS distribution may require signing and notarization.
- Windows, Linux, and mobile packaging have different dependency and distribution requirements.
- Browser-based functionality is constrained by browser security policies.

These limitations must be documented accurately as implementation progresses.

The platform support matrix must be updated when capabilities are implemented and verified.

---

## 27. License

The project's final open-source license must be confirmed and included in the repository.

Until that decision has been made and a valid `LICENSE` file is present, the README must not claim that a particular open-source license applies.

---

## Why PhoneDock Exists

Your phone and your computer are already powerful devices.

PhoneDock aims to make them work together as naturally as possible.

Not simply:

> Mirror my phone.

But:

> **Make my phone part of my computer.**

And when the situation calls for it:

> **Let my devices become one connected workspace.**

That is PhoneDock.

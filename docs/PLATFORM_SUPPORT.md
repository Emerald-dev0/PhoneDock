# Platform support and capability matrix

This matrix separates **source found in the repository** from **intended product scope**. No platform capability is considered complete because a directory, UI, interface, or prototype exists. Status definitions and evidence rules: [FEATURE_STATUS.md](FEATURE_STATUS.md). Feature requirements: [PRODUCT_SPEC.md](PRODUCT_SPEC.md).

## Application targets

| Target | Source and technology actually found | Baseline evidence status | Intended role (not a claim of availability) | Build/testing prerequisites and compatibility limits |
|---|---|---|---|---|
| **Android** | Kotlin; Android Gradle Plugin 8.7.2; Kotlin 2.0.21; Jetpack Compose/Material 3; `minSdk 26`, `targetSdk 35`, `compileSdk 35`; one `:app` module | Compose onboarding/dashboard is a prototype. NSD, TCP listener, MediaProjection and MediaCodec AVC source exist but are unverified/partial. No real-device result. | Phone-side companion and user-consented Android screen source; additional capabilities only where Android APIs/permissions/device support permit. | JDK 17 is CI choice; Android SDK/build tools API 35; emulator plus named physical devices. Test runtime permission, projection/foreground-service lifecycle, rotation, codec variation, network change, and power behavior. `local.properties` must remain local/ignored. |
| **iOS** | No Swift/SwiftUI, Xcode project/workspace, package manifest, or iOS assets | **Planned but not found** | Native SwiftUI companion with only iOS-supported and user-authorized workflows; not feature parity with Android. | macOS runner, Xcode/iOS SDK/simulator and physical iPhone verification. Screen capture, remote input, background, clipboard and notification behavior must be reviewed against Apple APIs/policy before specification. |
| **Linux desktop** | Python 3, PySide6 6.11.2, PyAV 18.1.0, `zeroconf` 0.151.5; Bash launcher and Debian packaging script | UI is a prototype; discovery/TCP/H.264 source exists but is unverified; package script is unverified and prototype-grade. No distribution compatibility test. | Desktop discovery/device management, supported Android screen viewer/control, transfers and diagnostics as later implemented. | Python 3.11 is CI's interpreter; direct dependencies are in `desktop/requirements.txt`. The PySide6 wheel selected in the x86_64 sandbox requires glibc 2.34 or newer; other architectures/distros remain unverified. Qt/PyAV runtime, display/session and multicast network are needed; `dpkg-deb` for the existing Debian script. Distribution/Wayland/X11, codec and library behavior need a declared test matrix. |
| **Windows desktop** | C++20 Visual Studio `.vcxproj`, Windows DNS service APIs, Winsock, Media Foundation, Direct3D 11, C++/WinRT header; a separate driver `.vcxproj` | App source is a prototype and unbuilt locally; decode/render methods are TODOs. Driver project has no implementation source and a malformed project GUID. | Native Windows desktop client; second-display work is separate research, not current support. | Windows runner with Visual Studio C++ toolset v143 and Windows SDK; local Developer PowerShell for MSBuild. Real Windows network/codecs required. Driver needs actual source, WDK, signing/policy and hardware before a build/support claim. |
| **macOS desktop** | No app source or Apple project/configuration | **Planned but not found** | First-class native Mac device workspace, respecting macOS conventions. Technology choice remains open. | macOS/Xcode runner and SDK; Apple signing/notarization credentials and distribution plan before public release. Validate permissions, sandbox, supported network and media APIs on physical Macs. |
| **Web app and product website** | No web source, framework config, package manifest, or deployed site | **Planned but not found** | Product information, documentation, download/release information and any browser utilities that are secure and supported. Not a substitute for native OS integration. | Browser support/build stack must be selected when source exists. Browser-local-network, permissions, secure-context and background constraints require feature-by-feature review. Validate accessibility and supported browsers. |

## Capability matrix

`Source found` means some related code exists, not that an end-user workflow is complete or interoperable. `Target` describes intended direction only. `Not found` means no implementation evidence was located. Platform-specific availability must be negotiated at runtime after actual implementation.

| Capability | Android | iOS | Linux | Windows | macOS | Web |
|---|---|---|---|---|---|---|
| App/UI | Compose prototype | Target; no source | PySide6 prototype | C++ console/prototype | Target; no source | Target; no source |
| Automatic local discovery | NSD source; unverified | Target; no source | Zeroconf source; unverified | DNS-SD source; unverified | Target; no source | Not found; browser constraints apply |
| Manual host/IP connection | Not found | Target; no source | Not found in UI | Client API takes an address, but no manual UI | Target; no source | Not found |
| Pairing, authenticated trust, device identity | Not found | Not found | Not found | Not found | Not found | Not found |
| TCP session/video-frame experiment | Server source; partial | Not found | Receiver source; unverified | Receiver source; unverified | Not found | Not found |
| Android screen capture source | MediaProjection/AVC source; unverified | Not applicable to Android source; iOS capture is a separate decision | Not applicable | Target receiver; decode/render incomplete | Target receiver; no source | Not found |
| Remote Android input | Server input handling not found | Not found | Input packet sender only; Android receiver absent | Not found | Not found | Not found |
| USB connection | Not found | Not found | Not found | Not found | Not found | Not found |
| File transfer/shared inbox | Not found | Not found | Not found | Not found | Not found | Not found |
| Content/link handoff | Not found | Not found | Not found | Not found | Not found | Not found |
| Clipboard synchronization | Not found | Not found | Not found | Not found | Not found | Not found |
| Notification forwarding | Not found; service status notification only | Not found | Not found | Not found | Not found | Not found |
| Device media controls/status/history | Not found | Not found | Not found | Not found | Not found | Not found |
| Diagnostics/performance metrics | Not found; Linux UI has a static `0 ms` label | Not found | Static placeholder label only | Not found | Not found | Not found |
| Android as a second display | No implementation | Not found | Not found | Windows-only GUID/IOCTL and empty driver project; no working display extension | Not found | Not found |
| Product site/downloads | Not found | Not found | Not found | Not found | Not found | No site source found |

## Platform restrictions and verification expectations

- **Android:** screen capture requires user consent and platform lifecycle compliance. Remote interaction, background operation, local-network discovery and notification integration have separate API/permission limits. The checked-in manifest and target SDK are not a compatibility test. Capture/encoder support and performance vary by device.
- **iOS:** design and implementation must follow iOS system privacy and capability boundaries. Do not promise arbitrary screen capture, system input injection, unrestricted clipboard access, or Android-equivalent background behavior without a reviewed supported API path.
- **Linux:** network discovery, multimedia codecs, display session, packaging, sandboxing, and device permissions vary across distributions and desktop sessions. Declare supported distributions and validate on them before release.
- **Windows:** app APIs and codecs vary by Windows/SDK/hardware; display-driver functionality has separate WDK, signing, deployment, recovery, and OS-version requirements. A `.vcxproj` is not proof of a working app or driver.
- **macOS:** privacy prompts, sandboxing, distribution, signing/notarization and APIs differ from iOS and Linux. Do not infer support from an iOS target.
- **Web:** browser APIs are constrained by same-origin/security models, permissions and background lifecycle. A web client cannot be assumed to open arbitrary native TCP connections or run a native display/driver path.

## Build and test evidence policy

- CI jobs currently target the existing Android Gradle module, Python/Linux desktop dependency/source checks plus a short offscreen UI smoke, and the Windows C++ application project. The Windows driver is excluded because it lacks sources and requires the WDK; iOS/macOS/web have no projects to build.
- A successful build establishes buildability for that runner/toolchain only. It does not establish discovery, session security, video, input, transfer, or hardware compatibility.
- Each feature row must be updated only with a CI result or named platform/device test record as defined in [FEATURE_STATUS.md](FEATURE_STATUS.md) and [TESTING.md](TESTING.md).
- There is no claimed supported release matrix at this point. Device/OS/distribution/browser versions should be added only when they are actually tested and maintained.

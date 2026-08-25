# PhoneDock

> Turn your Android phone into a native extension of your Windows PC.

PhoneDock is a local-first Android ↔ Windows device bridge that allows you to interact with your physical Android phone directly from your Windows desktop.

Control your phone with your PC's mouse and keyboard, synchronize your clipboard, transfer files, access notifications, and interact with Android applications without constantly reaching for your phone.

PhoneDock also includes a reverse display mode that can turn the Android device into a secondary display for Windows.

---

## The Idea

Your phone and your computer are already two powerful devices.

The problem is that they are often treated as completely separate worlds.

You might be working in VS Code on your PC and suddenly need to:

- Check a message on your phone
- Copy something from your phone
- Send a file to your phone
- Test an Android application
- Control music playing on your phone
- Read a notification
- Search something on mobile
- Interact with an Android-only application

The usual solution is to physically pick up the phone.

PhoneDock is built around a different idea:

> **What if your physical Android phone could simply become another device inside your Windows workspace?**

That's PhoneDock.

---

## What PhoneDock Does

PhoneDock creates a direct connection between an Android phone and a Windows PC.

The primary direction is:

```text
Android Phone
      │
      │
      ▼
  PhoneDock
      │
      │
      ▼
 Windows PC
```

The Windows application displays the Android device and allows the user to interact with it.

The connection can operate through:

* USB
* Local Wi-Fi

For wireless operation, the phone and PC only need to be connected to the same local network.

No cloud server is required for normal operation.

---

# Core Features

## 📱 Control Your Android Phone From Windows

PhoneDock allows the Windows PC to interact with the physical Android phone.

Depending on device capabilities and permissions, this includes:

* View the Android screen
* Click and interact with applications
* Scroll
* Drag
* Navigate Android
* Type using the Windows keyboard
* Use keyboard shortcuts where supported
* Control media
* Access Android applications

The goal is for the phone window to feel like a natural part of the Windows desktop.

---

## 🖱️ Mouse Control

Use your Windows mouse to interact with Android.

Potential interactions include:

* Tap
* Double tap
* Long press
* Drag
* Scroll
* Navigation
* Text selection

Input events are translated by PhoneDock and delivered to the Android device.

---

## ⌨️ Keyboard Control

Your physical Windows keyboard becomes an input method for Android.

Instead of typing on the phone's small keyboard, you can type directly from your PC.

```text
Windows Keyboard
       │
       ▼
   PhoneDock
       │
       ▼
Android Text Field
```

PhoneDock is designed to support normal text input as well as appropriate special keys.

---

## 📋 Clipboard Synchronization

PhoneDock can synchronize clipboard content between Windows and Android.

For example:

```text
Windows
   │
   │ Copy
   ▼
PhoneDock
   │
   ▼
Android
   │
   │ Paste
   ▼
Android App
```

The reverse direction is supported as well.

Clipboard synchronization can be controlled by the user.

---

## 📁 File Transfer

Move files between your Android device and Windows PC without relying on cloud storage.

Example:

```text
Windows Explorer
       │
       │ drag file
       ▼
   PhoneDock
       │
       ▼
     Android
```

Potential capabilities include:

* Windows → Android
* Android → Windows
* Drag and drop
* Transfer progress
* Transfer cancellation
* Large-file support
* Interrupted-transfer recovery

---

## 🔔 Notifications

PhoneDock can optionally forward Android notifications to Windows.

This means you can see important phone notifications without picking up your phone.

Users should be able to control:

* Whether notifications are synchronized
* Which applications are allowed
* Notification privacy

---

# 🔄 Two-Way Display Modes

PhoneDock has two fundamentally different display directions.

## Mode 1 — Control Your Phone

This is the primary PhoneDock experience.

```text
        Android
           │
           │ screen + interaction
           ▼
        Windows
```

Your Android phone appears inside Windows.

You control the physical phone from your PC.

---

## Mode 2 — Use Your Phone as a Second Monitor

PhoneDock can also work in the opposite direction.

```text
        Windows PC
             │
             │ display output
             ▼
        Android Phone
```

The Android phone becomes an additional display for Windows.

This provides a spacedesk-like experience where you can move additional Windows applications onto the phone.

For example:

```text
┌────────────────────────┐    ┌─────────────────────┐
│                        │    │                     │
│ VS Code                │    │ Terminal            │
│                        │    │                     │
│ Browser                │    │ Discord             │
│                        │    │                     │
│                        │    │ Logs                │
└────────────────────────┘    └─────────────────────┘
       Windows PC                  Android Phone
       Main Display                Second Display
```

These two modes are separate.

PhoneDock's identity is **Android → Windows device integration**, while the second-monitor feature provides an additional **Windows → Android display** capability.

---

# 🔌 Connection Methods

PhoneDock is designed around two primary connection methods.

## USB

USB provides a direct connection between the Android device and Windows.

```text
Android
   │
   │ USB
   ▼
Windows
```

USB is particularly useful when:

* Wi-Fi is unavailable
* Maximum stability is required
* Low latency is important
* The user is developing/testing Android applications

---

## 📶 Wireless

PhoneDock can operate over a local network.

The basic requirement is:

> Connect the Android phone and Windows PC to the same network.

For example:

```text
University Wi-Fi

       ┌───────────────┐
       │               │
       ▼               ▼
    Windows          Android
       │               │
       └───────┬───────┘
               │
          PhoneDock
```

No internet connection should be required for the core communication once the devices are on the same local network.

PhoneDock should use local discovery where supported and provide a manual IP connection fallback when automatic discovery is unavailable.

---

# 🔐 Local-First & Privacy

PhoneDock is designed as a local-first system.

The normal communication path is:

```text
Android ←────────────→ Windows
```

not:

```text
Android → Cloud → Windows
```

This means your phone's:

* Screen
* Clipboard
* Files
* Notifications
* Input
* Device information

do not need to pass through an external server during normal operation.

Security is treated as a core part of the architecture.

Connections should use authenticated sessions and encrypted transport where appropriate.

---

# 🧠 Architecture

PhoneDock consists of two primary applications:

```text
┌───────────────────────────┐
│       Android App        │
│                           │
│ Screen Capture            │
│ Input                     │
│ Clipboard                 │
│ File Transfer             │
│ Notifications             │
│ Discovery                 │
│ Connection                │
└─────────────┬─────────────┘
              │
       PhoneDock Protocol
              │
┌─────────────┴─────────────┐
│      Windows App          │
│                           │
│ Device Discovery          │
│ Video Rendering            │
│ Keyboard Input             │
│ Mouse Input                │
│ Clipboard                  │
│ File Transfer              │
│ Notifications              │
│ Connection Management      │
└───────────────────────────┘
```

The exact implementation architecture is documented separately as the project evolves.

---

# 🎥 Video Pipeline

The primary phone-control mode requires the Android screen to reach Windows with as little latency as possible.

The conceptual pipeline is:

```text
Android Screen
      │
      ▼
Screen Capture
      │
      ▼
Hardware Encoder
      │
      ▼
PhoneDock Transport
      │
      ▼
Windows Receiver
      │
      ▼
Hardware Decoder
      │
      ▼
PhoneDock Window
```

The implementation should prioritize hardware acceleration where supported.

The system should avoid unnecessary copies and conversions.

---

# 🖱️ Input Pipeline

Input travels in the opposite direction.

```text
Windows Mouse / Keyboard
          │
          ▼
      PhoneDock
          │
          ▼
   Input Translation
          │
          ▼
       Android
```

The exact input implementation depends on Android security restrictions, permissions, and supported APIs.

PhoneDock should never pretend a capability exists when the operating system does not actually allow it.

---

# 🔄 Connection Lifecycle

A typical connection should follow this process:

```text
Discovery
    │
    ▼
Pairing
    │
    ▼
Authentication
    │
    ▼
Capability Negotiation
    │
    ▼
Session Establishment
    │
    ▼
Streaming / Control
    │
    ▼
Connected
```

If the connection is interrupted:

```text
Connected
    │
    ▼
Connection Lost
    │
    ▼
Reconnect
    │
    ├── Success ──→ Connected
    │
    └── Failure ──→ Retry / User Diagnostics
```

PhoneDock should attempt to recover from temporary connection failures without unnecessarily destroying the user's session.

---

# 📡 Device Discovery

PhoneDock should automatically discover compatible devices on the local network.

Possible discovery mechanisms include:

* mDNS
* UDP broadcast
* Multicast
* Direct IP connection

Because different networks handle multicast and broadcast traffic differently, PhoneDock should not rely on a single discovery mechanism.

A manual connection option should always be available where practical.

---

# 🤝 Pairing

PhoneDock should not blindly trust every device on the local network.

The first connection between devices should establish trust.

Example:

```text
New PhoneDock Device

TECNO KM5 wants to connect.

[ Cancel ]       [ Allow ]
```

Trusted devices can later be managed from settings.

---

# 📊 Performance

PhoneDock is designed around responsiveness.

Important metrics include:

* FPS
* Bitrate
* Latency
* RTT
* Dropped frames
* Encoder
* Decoder
* Connection type
* Reconnection time

A developer/debug mode may expose these metrics.

Example:

```text
PhoneDock Debug

FPS             60
Bitrate         8.4 Mbps
RTT             7 ms
Dropped Frames  0
Encoder         Hardware
Decoder         Hardware
Transport       Wi-Fi
```

Performance should be measured rather than assumed.

---

# 🧪 Testing Philosophy

PhoneDock is intended to be tested against real devices.

Testing should cover:

### Connection

* USB
* Wi-Fi
* Same-network discovery
* Manual IP
* Reconnection

### Video

* Screen capture
* Encoding
* Decoding
* Frame rate
* Latency
* Dropped frames

### Input

* Mouse
* Keyboard
* Touch translation
* Navigation
* Text input

### Synchronization

* Clipboard
* Files
* Notifications

### Reliability

* Network interruption
* Device sleep
* App restart
* Windows restart
* Android lifecycle changes

---

# 🩺 Diagnostics

A connection failure should not simply produce:

> "Connection failed."

PhoneDock should provide meaningful diagnostics.

Example:

```text
PhoneDock Diagnostics

Device Discovery      ✓
Device Pairing        ✓
Authentication        ✓
Transport             ✓
Video Encoder         ✓
Video Decoder         ✓
Input Channel         ✗

Problem:
Required Android input capability
is unavailable.
```

The goal is to make problems understandable to both developers and users.

---

# 🛠️ Development

PhoneDock is currently under active development.

The Android application is being developed using **Android Studio**.

The Windows application is being developed separately as the desktop counterpart.

The communication protocol is designed to remain independent of the user interface so that the system can evolve without tightly coupling both applications.

---

# 📂 Project Structure

The project structure will evolve alongside the implementation.

A conceptual structure is:

```text
PhoneDock/
│
├── android/
│   ├── app/
│   ├── connection/
│   ├── capture/
│   ├── input/
│   ├── clipboard/
│   ├── transfer/
│   └── ...
│
├── windows/
│   ├── app/
│   ├── connection/
│   ├── rendering/
│   ├── input/
│   ├── clipboard/
│   ├── transfer/
│   └── ...
│
├── protocol/
│   ├── discovery/
│   ├── connection/
│   ├── messages/
│   └── ...
│
├── docs/
│   ├── architecture/
│   ├── protocol/
│   ├── testing/
│   └── decisions/
│
└── README.md
```

The actual repository structure should be kept aligned with the implementation.

---

# 🧭 Development Roadmap

## Phase 1 — Foundation

* [x] Android application (v1.1)
* [x] Linux application (Native Python/PySide6 v1.1)
* [/] Windows application
* [ ] Device identity
* [/] Basic connection
* [ ] USB communication

## Phase 2 — Screen Streaming

* [x] Android screen capture
* [x] Video encoding
* [x] Linux video decoding (PyAV)
* [ ] Windows video decoding
* [ ] Low-latency rendering

## Phase 3 — Remote Control

* [x] Mouse input (Injection foundation)
* [ ] Keyboard input
* [ ] Android navigation
* [ ] Text input

## Phase 4 — Device Integration

* [ ] Clipboard synchronization
* [ ] File transfer
* [ ] Notifications
* [ ] Device information
* [ ] Media controls

## Phase 5 — Wireless

* [x] Local discovery
* [x] Wi-Fi connection
* [ ] Pairing
* [ ] Secure transport
* [/] Reconnection
* [ ] Network diagnostics

## Phase 6 — Second Display

* [ ] Windows display architecture
* [ ] Android display receiver
* [ ] Display configuration
* [ ] Resolution handling
* [ ] Performance optimization

## Phase 7 — Production

* [x] Polished onboarding
* [ ] Settings
* [ ] Diagnostics
* [ ] Security review
* [ ] Performance benchmarks
* [ ] Documentation
* [ ] Release builds

---

# ⚠️ Platform Limitations

PhoneDock interacts with operating-system-level functionality.

Android and Windows impose security and permission boundaries on applications.

Therefore some capabilities may require:

* User permissions
* Accessibility services
* ADB during development
* Special system APIs
* Device-specific support

PhoneDock should clearly document these limitations rather than relying on unsupported or misleading implementations.

---

# 🔬 Engineering Decisions

PhoneDock documents important engineering decisions as the project develops.

For significant architectural choices, we aim to document:

1. The original problem
2. Solutions considered
3. Experiments performed
4. What failed
5. Why it failed
6. The selected approach
7. Trade-offs
8. Verification results

This is important because the goal is not simply to make something that works once.

The goal is to understand **why it works**.

---

# 🚧 Current Status

PhoneDock is currently in active development.

The project is being built incrementally, starting with the Android foundation and communication architecture before expanding into the complete Windows experience.

Features listed in this README may represent planned functionality and should not be interpreted as completed unless explicitly marked otherwise.

---

# 🤝 Contributing

Contributions, experiments, bug reports, hardware compatibility reports, and architectural discussions are welcome.

When submitting an issue, include where possible:

* Windows version
* Android version
* Phone model
* Connection type
* PhoneDock version
* Relevant logs
* Steps to reproduce
* Expected behavior
* Actual behavior

---

# 📜 License

PhoneDock will be released under an open-source license.

The final license will be specified before the first public release.

---

# 💡 Why PhoneDock Exists

There are already tools that solve pieces of this problem.

There are tools for:

* Screen mirroring
* Remote Android control
* File transfer
* Clipboard synchronization
* Second displays
* Android debugging

PhoneDock is an attempt to bring these experiences together into one coherent local-first system.

The goal is not:

> "Mirror my phone."

The goal is:

> **"Make my phone part of my computer."**

And when the situation calls for it:

> **"Let my phone become another screen for my computer."**

That's PhoneDock.

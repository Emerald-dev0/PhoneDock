# PhoneDock protocol findings and requirements

**Status:** No finalized, interoperable PhoneDock protocol exists in the audited source. This document records source-level observations and proposed requirements; it does not define message IDs, an encoding, a port, cryptographic suite, or compatibility promise. See [PROJECT_AUDIT.md](PROJECT_AUDIT.md) for evidence and [SECURITY.md](SECURITY.md) for the security baseline.

## Existing repository findings

| Concern | What source currently does | Limitation |
|---|---|---|
| Discovery | Android registers `_phonedock._tcp` with an ephemeral port in `NsdHelper.kt`/`ConnectionService.kt`; Linux browses `_phonedock._tcp.local.` in `desktop/discovery.py`; Windows uses DNS service browsing for `_phonedock._tcp.local` in `windows/PhoneDock.App/Discovery.cpp`. | No conformance test establishes identical DNS-SD semantics, service metadata, identity, IPv6 behavior, interface handling or compatibility. A discovered service is not trusted. |
| Android TCP listener | `ConnectionService` creates `ServerSocket(0)`, publishes the selected port, accepts sockets, and assigns an active client. | No hello, authentication, encryption, session expiry, capability negotiation or input reader. Listener binding/exposure policy and concurrent-client behavior need review. |
| Current video framing shape | Android's `ByteBuffer` writes four bytes of payload length (default big-endian) followed by one key-frame flag byte, then encoded bytes. Windows reads a network-order length, one flag byte and a payload. Linux `ConnectionManager` parses a big-endian 32-bit size plus a one-byte `type`, treating types 0 and 1 as video. | There is no authoritative field definition, maximum size, codec config/format-change record, timestamp semantics, error handling, heartbeat, endianness test vector or protocol-version marker. Similar shape does not prove compatible behavior. |
| Current input attempt | Linux sends a big-endian length, type 2, then a `>Bff` mouse record. | Android does not read client input and Windows has no corresponding implementation. This is not a working remote-control protocol. |
| PDP constants | `windows/PhoneDock.Common/Public.h` defines `PDP_VERSION_MAJOR 0`, `PDP_VERSION_MINOR 1`, and default port `45124`. | These values are Windows-only declarations and were not found in the Android dynamic-port flow. They are not evidence that PDP v0.1 is implemented or negotiated. |
| Other data | No file-transfer, clipboard, notification, device-management or version-negotiation wire implementation was found. | No format or compatibility behavior should be inferred. |

## Requirements for a future protocol

### Discovery and pairing

- Discovery returns an untrusted candidate with address/service metadata only; it must never grant access.
- Provide a separate, explicit pairing flow that establishes and verifies a stable device identity. The exact pairing ceremony, key type, storage and revocation behavior require a reviewed decision.
- Support address changes without treating a new IP or DNS-SD instance name as a new trusted identity.
- Define timeouts, duplicate/lost service behavior, IPv4/IPv6 policy, interface selection and manual connection semantics.

### Session establishment

A proposed high-level sequence is: discover or manually locate candidate → user approves pairing/trust → authenticate peer → establish protected session → negotiate compatible protocol version and capabilities → enable individually authorized operations. This is a requirement outline, not a finalized exchange. Failure at any authentication/version/capability step must fail closed; unauthenticated discovery data cannot initiate a sensitive operation.

### Messages and capabilities

- Use an explicit versioned envelope and unambiguous field encoding/byte order.
- Define message classes for session/control, media, transfer and diagnostics only as requirements justify them; specify ownership, ordering, fragmentation, acknowledgements, cancellation and errors.
- Define hard per-message and aggregate queue limits before parsing peer-supplied lengths.
- Negotiate only capabilities supported by both peers and their current OS/hardware/permissions; distinguish “supported” from “active” and “permission required.”
- Specify behavior for unsupported messages, duplicate/replayed requests, unknown optional fields, incompatible major versions and compatible minor extensions.
- Provide language-independent test vectors and malformed-input cases before multiple parsers are called interoperable.

### Transport expectations

- Discovery, transport and authentication are distinct layers; a multicast service announcement does not provide trust.
- Direct local transport is the default product goal. Wi-Fi and USB adapters should share the same authorization semantics where practical, while documenting platform-specific setup.
- Define bind address, ports, reconnect policy, timeouts, backpressure, partial reads/writes and how active-client limits are enforced.
- A future browser client must use only transport APIs and permission models actually available in supported browsers; do not assume arbitrary TCP sockets.
- The planned iOS adapter must honor Local Network privacy, Bonjour declarations, and foreground/background lifecycle limits; do not encode an assumption that discovery or a raw socket remains active in the background. Generic iPhone-to-PC USB is not a baseline transport; see the feasibility gate in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md).
- Decide whether media and data share one protected stream or use separate negotiated channels only after profiling and threat-model review.

## Versioning and compatibility policy (proposed)

- Protocol versioning is separate from app/release versioning.
- A session must identify compatible protocol versions before feature data is accepted.
- Major incompatible changes require explicit negotiation/migration or a clear refusal; minor additions must have specified ignore/required-field semantics.
- Document the oldest/newest tested peer versions and run compatibility fixtures for each supported pair.
- Do not publish a compatibility claim based on source resemblance, matching port numbers or successful DNS-SD alone.

## Security considerations

The current experimental path is plain TCP with no pairing or encryption. Anyone able to reach the listener may be accepted by the Android service; the screen stream is not protected by a defined protocol security layer. Linux and Windows parse peer-controlled lengths without a documented bound, and TCP reads may be partial. Do not use this prototype on an untrusted network or expose it to the Internet.

Before protocol implementation, require a threat model, authenticated encryption based on vetted primitives, peer identity and revocation semantics, replay/session handling, parser limits, safe error responses, privacy-preserving logs, and security review. Do not invent a custom cipher or handshake. See [SECURITY.md](SECURITY.md).

## Decisions still open

- Protocol name, wire encoding, major/minor version model, test-vector format and message envelope.
- Pairing/user verification method, stable identity, key algorithm/storage and key rotation/revocation.
- Transport security primitive and library/API per platform; whether media/data share a channel.
- Discovery TXT metadata, dynamic/static port policy, IPv6, multiple interfaces, and manual host/address support.
- Video codec configuration records, timestamps, key-frame recovery, payload caps, flow control and backpressure.
- Input, file-transfer integrity, clipboard, notification and error message models.
- Compatibility/upgrade/support window and behavior when one peer updates before another.

Resolve each through reviewed ADRs and executable conformance tests. Until then, refer to the current stream only as an experimental implementation detail.

# Security and privacy baseline

This document sets requirements and records open review items. It is not a security certification or a claim that current prototypes are safe. The protocol is not finalized; see [PROTOCOL.md](PROTOCOL.md). Current source findings are in [PROJECT_AUDIT.md](PROJECT_AUDIT.md).

## Local-first assumptions

- Core local-device workflows should work directly where the platform and network permit; ordinary pairing/streaming/transfer should not silently require a cloud account or relay.
- Local network traffic is not trusted merely because it is local. Guest Wi-Fi, shared networks, compromised routers, malicious/misconfigured peers, multicast spoofing, address reuse and untrusted USB hosts are in scope for review.
- Discovery advertises candidates, not identity. IP address, DNS-SD instance name, device display name, and port are mutable and unauthenticated.
- Optional cloud/distribution/update features must be disclosed separately, collect only required data, and must not be confused with local transport.

## Current baseline warning

The Android prototype creates an unauthenticated TCP listener and accepts a client; the observed video frame path is not protected by a documented session protocol. No pairing, trusted-device store, authenticated encryption, revocation, or message-length contract was found. Linux and Windows receive unbounded peer-supplied lengths. Treat this as development-only code on a controlled network; do not expose it to the Internet or rely on it for confidential content.

This phase adds documentation and CI/repository safeguards, not a security implementation.

## Required security properties before sensitive product use

### Device trust and authentication

- Show a user-readable peer identity and clear first-pairing approval; reject unknown peers by default.
- Bind trust to cryptographic identity rather than a network address or discovery name.
- Authenticate every session before enabling screen, input, clipboard, notification or file operations.
- Provide per-device revocation, safe key rotation/expiry, and behavior for device reset/reinstall.
- Protect against replay, session confusion, downgrade and cross-protocol use; define failure behavior before implementation.
- Design pairing for nearby/local user presence and consider a user-verifiable out-of-band step. The exact ceremony remains undecided.

### Encrypted sessions and key handling

- Require confidentiality and integrity for sensitive session content over Wi-Fi and any supported USB transport.
- Use maintained platform crypto and standard authenticated protocols; do not design custom cryptography.
- Store private keys/credentials only in appropriate OS-protected storage; never hardcode, commit, print, or put them in ordinary preferences/logs.
- Limit key export, define backup/restore behavior, and clear local trust material on revoke/uninstall according to platform policy.
- Review certificate/pinning or key-continuity decisions for usability, rotation, and recovery. No exact cryptographic suite is selected in this phase.

### File and content transfer

- Restrict writes to a user-approved destination; normalize names and paths; reject traversal, unsafe symlinks, reserved names and unexpected types where applicable.
- Avoid silent overwrites; provide clear conflict policy, cancel behavior, progress, completion state, and privacy-aware transfer history.
- Verify integrity before reporting success; define partial-file cleanup/resume semantics.
- Bound file size, queue length, metadata, decompression, memory, and timeouts. Validate content independently of its displayed name/type.

### Clipboard and notifications

- Keep clipboard sync off until enabled; offer direction/source controls, pause/disable, reasonable size/format limits and loop prevention.
- Treat clipboard and notification content as highly sensitive. Do not log bodies, titles, tokens, or file contents.
- Make notification access explicit, scoped where possible, revocable, and limited to selected apps/categories when the OS permits.
- Do not assume that a platform grants background clipboard/notification access just because another platform does.

### Screen capture and input

- Require platform consent before capture and maintain a visible active state with an immediate stop control.
- Request only platform permissions necessary for the selected feature; explain any accessibility/developer/driver prerequisite.
- Scope input forwarding to an authenticated active session, show when it is available, support cancellation, and avoid enabling it as a side effect of pairing.
- Validate coordinates, event ordering and rate; prevent an untrusted peer from injecting arbitrary input.

## Permission boundaries

- Request permissions just in time and explain why they are needed; denial should leave unrelated features usable.
- Keep mobile UI, foreground/background services, file pickers, notification listeners and accessibility/developer access separate in purpose and lifecycle.
- Re-check capabilities after permission changes, OS updates, display changes, network changes and process restart.
- Review the Android manifest and `android:allowBackup="true"` as persistent sensitive state is introduced. Existing manifest includes internet/network-state/Wi-Fi-state and foreground-service/media-projection permissions; no notification-listener, storage, clipboard-sync or input-injection integration was found.
- Windows driver installation/signing, macOS/iOS privacy prompts, and browser local-network permissions require platform-specific review before those features are advertised.

## Logging and diagnostics policy

- Never log private keys, pairing codes/tokens, authentication headers, clipboard text, notification bodies, file contents, or user-selected private paths by default.
- Prefer structured error codes, coarse timing/size metrics, and redacted device identifiers; bound log retention and rate.
- Make diagnostic export user-triggered, explain included data, and offer review/redaction before sharing.
- Avoid logging IP addresses or stable device identifiers unless operationally necessary; disclose retention and access.
- Do not add telemetry/cloud collection without an explicit privacy design, user disclosure, minimization, retention, and consent review.

## Threat-model work required

For each session/feature, record assets, principals, trust boundaries, attacker capabilities, abuse cases, mitigations, residual risks and tests. Include at least:

- Rogue discovery advertisements, peer impersonation, replay/downgrade and untrusted same-LAN peers.
- Malformed/oversized frames, partial TCP reads, parser differentials, queue exhaustion and denial of service.
- Unauthorized screen viewing/input, consent confusion, session hijacking, stale trust and reconnect after revocation.
- Malicious file names/content, path traversal, overwrite, disk exhaustion and interrupted transfer.
- Clipboard/notification leakage, unintended synchronization loops and log/diagnostic disclosure.
- Permission revocation, process death, device sleep, network changes, USB removal and cleanup failure.
- Compromised updates, dependency supply chain, signing key exposure, release workflow permissions and build artifact provenance.

## Review gate

Before enabling a sensitive feature for users, require: an accepted threat model; protocol/security review; negative tests for unauthorized/malformed requests; platform permission and lifecycle tests; dependency review; privacy/logging review; and a written decision on residual risk. Critical/high unresolved vulnerabilities block release. Record actual evidence and known limits in the feature matrix and release checklist.

## Open security decisions

Pairing ceremony, identity/key format and store, authenticated-encryption protocol/library, protocol version downgrade policy, log retention, optional telemetry policy, Android backup policy, transfer persistence, Windows driver distribution, and release-signing/update model remain undecided. Capture actual decisions as ADRs; do not treat this checklist as a choice of implementation.

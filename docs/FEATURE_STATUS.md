# Feature status and verification evidence

Use this page as the single status vocabulary for feature tables and roadmap checklists. A screen, interface, folder, method stub, successful compile, or demo animation alone is not evidence that a user-facing capability is complete.

## Status vocabulary

| Status | Meaning | Minimum evidence to use it |
|---|---|---|
| **Planned** | Accepted product intent; implementation has not started. | Requirement or roadmap item exists; no implementation claim. |
| **In progress** | Work has started, but the acceptance criteria are not all satisfied. | Link to the active change and state what remains. |
| **Implemented** | Functional code exists, but its behavior has not yet been verified at the required level. | Source path and an explanation of the implemented behavior; explicitly say which tests remain. |
| **Automated tests passed** | The relevant automated unit/integration checks passed. | CI run or reproducible local command, commit, and result. A build with zero tests is not a test pass. |
| **Platform verified** | The capability was exercised on the named supported OS/device/network configuration. | Platform/OS/device, version, test steps, result, and date. Hardware-dependent claims name the physical hardware. |
| **Blocked** | Work cannot proceed because a specific external prerequisite is unavailable or unresolved. | Name the dependency (for example, signing credential, WDK, device, API decision) and an unblock condition. |
| **Deferred** | The feature is intentionally outside the current phase or release. | Link to the roadmap decision/scope and identify the next review point if known. |

`Implemented`, `Automated tests passed`, and `Platform verified` are progressively stronger evidence states. Keep platform evidence scoped: an Android test on one device does not imply all Android versions, and a build does not imply hardware behavior. Use **Partially implemented** when only part of a capability's acceptance criteria is present; this is a descriptive qualifier, not a completion state.

## Audit labels

The repository baseline audit uses the following evidence-oriented labels required for reconnaissance:

- **Implemented and verified** — evidence exists at the relevant automated/platform level.
- **Implemented but not verified** — real behavior is present in source, but has not been exercised.
- **Partially implemented** — a real subset exists; essential behavior or integration is absent.
- **Prototype or mockup** — exploratory UI/scaffolding/stubs, or behavior that should not be represented as a reliable feature.
- **Planned but not found** — product intent exists, but no implementation was found.
- **Blocked by an external requirement** — an implementation or verification task is specifically waiting on an external prerequisite.
- **Unknown** — evidence is insufficient to classify safely.

These audit labels should not be silently translated into “complete.” For example, a screen with a “Transfer” button is a prototype unless a real transfer path and its acceptance evidence exist.

## Evidence entry format

For each meaningful feature, keep a concise row in [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md) or [ROADMAP.md](ROADMAP.md):

| Capability | Status | Source / acceptance criteria | Automated evidence | Platform evidence | Blocker / next step |
|---|---|---|---|---|---|
| Example only—replace before use | Planned | Link to requirement | Not run | Not run | None |

Do not use the example row as an actual product feature. Use explicit `Not run`, `Not available`, or `Not applicable` rather than a blank cell where silence could imply success.

## Pull-request completion rule

A contributor reports separately:

1. implementation status;
2. automated checks actually run and their result;
3. real-device/platform verification actually performed;
4. checks blocked by environment, hardware, credentials, or unresolved decisions;
5. remaining acceptance criteria.

Move a status forward only when its evidence is attached or linked. If a regression occurs, move the status back and record it. See [CONTRIBUTING.md](../CONTRIBUTING.md), [TESTING.md](TESTING.md), and the pull-request template.

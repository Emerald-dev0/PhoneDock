# Changelog

PhoneDock has no verified tagged release history in the checked-out repository. This changelog starts with the recovery phase; it does not reconstruct or invent past releases. Add dated entries for user-visible changes and important security/compatibility changes. Keep unreleased work under `## [Unreleased]` and move it to a versioned section when a maintainer prepares a release.

## [Unreleased]

No release entry has been prepared yet.

## Release policy

- Use stable semantic version tags of the form `vMAJOR.MINOR.PATCH` (for example, `v1.2.3`) only after project versioning is approved and a matching dated changelog section exists.
- The tag-triggered workflow checks CI and creates a **draft source-only GitHub Release**. It does not build, sign, notarize, upload application binaries, or publish the draft.
- A maintainer must review release notes, supported platforms, artifacts/checksums, signing and distribution requirements, then publish manually. Never attach unsigned or placeholder artifacts as production downloads.
- A GitHub Release does not automatically update an installed Android, iOS, Linux, Windows, macOS or web application. Update delivery/rollback is a separate reviewed capability.

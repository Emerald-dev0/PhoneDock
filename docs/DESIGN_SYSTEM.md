# PhoneDock design system proposal

**Status:** Directional proposal for a dedicated design phase. No new visual identity or final logo is approved by this document. Existing platform UIs and assets are recorded separately; do not treat these proposed values as production tokens before review and contrast testing.

## Existing visual evidence

- Android onboarding uses a legacy “Harvst” cream/coral/dark-green palette and custom Compose Canvas illustrations. Its theme also contains a separate neutral/green palette.
- Linux onboarding and main window use the same cream/coral/dark-green family and custom PySide6 illustrations.
- The Android launcher image is the default Android template robot/grid icon; no approved PhoneDock mark, brand asset collection, design token package, or screenshots directory exists.
- Android onboarding copy and illustrations include Windows control, clipboard/file synchronization and second-display claims that are not implemented. Visual/content review must remove or clearly label such claims.

Preserve source illustrations during Phase 0; do not mistake their existence for a complete brand or replace them without a design review.

## Proposed visual direction

Aim for premium, modern, device-oriented clarity: a calm, deep indigo foundation, electric ice-blue interaction accent, soft porcelain light surfaces, and deep ink dark surfaces. Use layered translucent materials sparingly to communicate grouping and depth—not as a direct imitation of Apple's branding or a substitute for accessible contrast.

### Initial palette proposal (not finalized)

| Role | Light proposal | Dark proposal | Use |
|---|---|---|---|
| Primary / indigo | `#293A8B` | `#AAB8FF` | Main actions, selected states, key identity accent; validate text-on-color contrast. |
| Ice-blue accent | `#55C9F3` | `#75D9FF` | Connection/activity highlight and focus accent; do not use alone for small text. |
| Porcelain surface | `#F5F7FB` | — | Main light canvas. |
| Elevated light surface | `#FFFFFF` | — | Cards and dialogs with restrained borders. |
| Deep ink surface | — | `#0C1224` | Main dark canvas. |
| Elevated dark surface | — | `#151E34` | Cards and sheets. |
| Primary text | `#151B2B` | `#F2F5FF` | High-priority text. |
| Secondary text | `#58647A` | `#B6C0D4` | Supporting labels; validate contrast at actual size/weight. |
| Divider/border | `#DDE3EF` | `#2B3650` | Subtle structure; not the only indication of state. |
| Success/warning/error | Semantic tokens to be selected and tested | Semantic tokens to be selected and tested | Never encode meaning by color alone. |

These are exploratory hex values, not an approved brand palette. Verify WCAG contrast for applicable web content and platform accessibility expectations before finalizing; check colors under translucency, dynamic/system appearance, color-blind simulation, high contrast and outdoor brightness.

## Appearance and materials

- **Light:** porcelain canvas, white elevated panels, dark-ink text, indigo primary controls and limited ice-blue emphasis.
- **Dark:** deep ink canvas, distinct raised ink-blue surfaces, light text, controlled accent brightness and visible focus/selection.
- **Layering:** thin borders, low-elevation shadows and restrained translucent overlays should clarify hierarchy. Maintain an opaque fallback when blur/material effects are unsupported, expensive, or inaccessible.
- **Android:** use native Compose/Android materials and APIs supported by the app's actual min/target SDK. A Liquid Glass-inspired treatment may use layered translucent surfaces, subtle highlights and depth; avoid claiming Apple's Liquid Glass API exists on Android or relying on unsupported system APIs. Test blur cost, scroll performance, contrast and fallback behavior.
- **iOS (planned Phase 4):** build with native SwiftUI conventions and Apple materials; use Liquid Glass-inspired styling only where the OS supports it (iOS 26 and later at this research snapshot) and where it improves hierarchy. Prefer system controls, keep content and controls legible, respect increased-contrast/reduced-transparency settings, and provide an accessible standard-material/opaque fallback for earlier or constrained configurations. Do not treat the effect as a feature prerequisite. The real Xcode app is not present; API and verification gates are in [ROADMAP.md](ROADMAP.md).
- **Desktop:** respect Linux desktop theme/session behavior, Windows controls/window conventions, and macOS system materials. Shared brand tokens must not force identical chrome or controls across these environments.
- **Web:** support responsive layouts, keyboard focus, accessible contrast and reduced motion; use browser-safe progressive enhancement.

## Typography and spacing

- Prefer each platform's system font: Android system sans, Apple's system typography on iOS/macOS, system/UI fonts on desktop, and `system-ui` on web. Do not ship a custom font until licensing, performance, script coverage and accessibility have been reviewed.
- Define a small type scale for display/title/body/label/caption and semantic emphasis. Preserve platform text scaling, dynamic type, browser zoom and readable line lengths.
- Proposed spacing basis: 4-point/dp increments with common 4, 8, 12, 16, 24, 32 and 48 values. Validate with responsive layouts and touch density rather than treating these as immutable pixel values.
- Avoid all-caps and letter spacing for long or small labels; use concise, human-readable connection and permission language.

## Logo and iconography

**Concept only:** a distinctive phone silhouette meeting a compact dock/cradle, with one restrained connection line or paired device surfaces. The symbol should remain legible at launcher, toolbar, monochrome and small favicon sizes; avoid generic Wi-Fi arcs as the only identity and avoid imitating Apple product silhouettes or wordmarks.

No genuine PhoneDock logo asset is created in this phase. A dedicated design deliverable should include editable vector source, monochrome and light/dark variants, Android adaptive icon exports, Apple app icon exports, desktop assets and web favicon, with clear licensing/attribution. Replace the Android template icon only after the new asset is reviewed and tested in launcher masks.

Use consistent semantic icon meanings, platform-native affordances and text labels for critical status/actions. Do not use emoji as the only production icon or status indicator.

## Component and interaction principles

- Build components around actual states: idle, discovering, pairing, permission required, connecting, connected, reconnecting, transfer progress, success, error and unavailable capability.
- A component's appearance and enabled state must derive from service state; avoid decorative “live” metrics or controls with TODO/no-op actions.
- Keep destructive operations (revoke, delete, stop transfer) distinct and confirm only when the action is genuinely consequential.
- Show user consent, active screen sharing, clipboard/notification state and transfer destination at the point of action.
- Keep controls visually calm, hierarchy clear, and touch targets large enough for the relevant platform. Use platform navigation conventions.
- Provide focus, pressed, disabled, loading and error states; do not communicate status by color alone.

## Motion

Use motion to explain state changes, continuity and progress; prefer short, reversible transitions. Avoid perpetual decorative animation, flashes and motion that hides status. Respect Android/iOS/desktop/web reduced-motion settings and provide a no-motion equivalent for essential feedback.

## Accessibility and validation

- Test light/dark contrast, large text, dynamic type, browser zoom, focus order/visibility, screen-reader labels, keyboard operation, switch access and non-color status.
- Target platform-recommended touch/focus sizing and WCAG 2.2 AA for web content where applicable; record exceptions rather than asserting untested conformance.
- Maintain textual status for discovery, pairing, capture, transfer and errors; announce meaningful updates without overwhelming assistive technology.
- Validate translucent/blurred surfaces against all backgrounds and allow an opaque surface mode where contrast or motion/processing requirements need it.

## Decisions awaiting the design phase

Final palette/tokens, wordmark/typeface, logo geometry, component library, Android material implementation/version gates, iOS Liquid Glass fallback, desktop title-bar/navigation patterns, motion timings, icon set and localization strategy remain open. Record genuine cross-cutting decisions as ADRs only after review; this page is a proposal, not an approval record.

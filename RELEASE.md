# Shared ScreamXY release checks

Scope: HeartGlance, RainScope, Pacegrain, Werkout, Mampf!, Heischwumm and King's Cup.
The live task list and decisions remain in the Obsidian vault's
`Privat/Development/ScreamXY/ScreamXY.md` and `TODO.md`. This document is the reusable
checklist; app-specific listings and hardware checks stay in each app's release kit.

## Each Apple app

- Public support URL, reachable privacy policy in the app and App Store Connect,
  and **screamcode@gmail.com** in the native contact UI and review metadata.
  This is a public support address, not a replacement for an Apple signing identity.
- Privacy copy must match actual data flows: local data, service providers,
  retention, backups, deletion and permission withdrawal. Review the final app's
  privacy labels, required-reason APIs, SDK manifests and permission purpose strings.
- HealthKit apps: explain the exact read/write access, keep sensitive data out of
  analytics and advertising, disclose cached readings, and avoid medical/live claims.
- Verify a signed Release archive, export-compliance answers, signing capabilities,
  screenshots, accessibility, age-rating answers and App Review access/instructions.
- Treat developer enrollment, App Store records, tip products/agreements, TestFlight
  and real-device evidence as separate gates. Passing CI does not complete them.
- Reassess the recorded EU non-trader decision against the actual activity and
  Apple's current criteria before launch; tips/free pricing alone do not establish
  non-trader status. Never publish a private home address by default.

## Delivery to TestFlight (14 October 2026)

- Feature branches run from Xcode directly on the device. A push to `main` triggers the app's
  Xcode Cloud workflow: Archive action on the release scheme (the `*Stub` scheme for watch-only
  apps), deployment preparation TestFlight (Internal Testing), post-action delivery to the
  internal group. Xcode Cloud signs with cloud-managed certificates; no secrets live in GitHub.
- Xcode Cloud uses its own build number and ignores `CURRENT_PROJECT_VERSION`. After a manual
  Organizer upload, raise the next build number in the product's Xcode Cloud settings.
- `ci_scripts/ci_post_xcodebuild.sh` writes the TestFlight "What to Test" notes from the recent
  commit subjects. The committed, drift-checked Xcode project is what Xcode Cloud builds.
- Xcode Cloud compute comes from the Developer Program's monthly allowance; only `main`
  archives, pull requests stay on the GitHub Actions smoke checks.

## CI cost policy

- Every job has a timeout: portal 3 min, web checks/builds 10 min, web deploy 5 min,
  native checks 10 min.
  Dependency installs and native compiler/test steps have tighter step limits.
- Read-only token permissions for checks. Cancel superseded checks. Production Pages
  deployment keeps `cancel-in-progress: false` so an active deploy can finish.
- Documentation-only edits skip app builds; source, fixtures, lockfiles, migrations,
  localization, manifests and project/workflow configuration still trigger checks.
- Hosted jobs run fast lint, type checks, deterministic unit tests and compilation.
  Extensive browser E2E, simulator/device suites and screenshots run locally by agents
  when changing the relevant code. There are no hosted full-suite opt-ins.
  Per-app `AGENTS.md` files give the local validation commands. Mampf retains its
  fast Mac state/sync/widget regressions without starting a simulator.
- No scheduled heavy suites, live AI/provider corpus calls, production DB tests,
  screenshot generation, paid service tests, signing or App Store uploads in PR CI.
- Failure evidence lives at most 7 days. Pacegrain release bundles are built only
  for release tags/manual runs; publishing still requires a release tag.
- Use standard hosted runners. GitHub currently provides standard hosted Actions
  free for public repositories; private repositories have included usage and billable
  overage. Timeouts reduce exposure but do not set an account spending limit.
- Billing limits are unchanged by request (13 October 2026): use the included minutes
  carefully, with extensive tests local. Verify branch-protection checks in GitHub settings.
  Path-filtered workflows can remain pending when required; use an always-running
  gate with conditional jobs if branch protection requires those checks on docs-only PRs.
- Watch smoke builds use Xcode 26.6 on the standard macOS 26 runner. Local Xcode 27
  simulator and hardware checks cover the newer SDK. Verify runner toolchain availability
  before changing versions; keep meaningful compilation checks enabled.

## App inventory

`apps.json` tracks the seven app slugs, public privacy URLs and native contact files.
`python3 -I scripts/check.py` validates portal coverage, local links and contact text.
With sibling repositories checked out, `python3 -I scripts/check.py --workspace`
also checks native contact sources, agent redirects and security contacts.

## Sources (reviewed 13 October 2026)

- [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) — privacy links, security and HealthKit requirements.
- [Apple App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/) — collection definitions and labels.
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) — public/private billing distinction.
- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — timeout, concurrency and path-filter behavior.
- [Apple EU trader requirements](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements) — assess status against actual activity.

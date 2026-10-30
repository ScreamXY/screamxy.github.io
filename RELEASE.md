# Shared ScreamXY release checks

Scope: PulseGlance, RainScope, Pacegrain, Werkout, Mampf!, Heischwumm and King's Cup.
The live task list and decisions remain in the Obsidian vault's
`Privat/Development/ScreamXY/ScreamXY.md` and `TODO.md`. This document is the reusable
checklist; app-specific listings and hardware checks stay in each app's release kit.

Current draft handoff: [20 October 2026 preparation](RELEASE-PREPARATION-2026-10-20.md).

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
  apps), **Distribution Preparation: App Store Connect**, post-action **TestFlight Internal
  Testing** delivery to the internal group. Enable **Restrict Editing** under General. Apple's
  documentation calls the eligible archive option **TestFlight and App Store**. Xcode Cloud
  signs with cloud-managed certificates; no secrets live in GitHub.
- **TestFlight (Internal Testing Only)** in the Archive action prevents App Store submission
  of that uploaded build. The internal-testing post-action only chooses the tester audience
  and can remain enabled for an App Store-eligible archive. After correcting the Archive
  setting, create a new build with a higher build number; existing internal-only uploads do
  not become eligible. Once processing finishes, verify that the new build is selectable in
  the App Store version's **Add Build** dialog. Internal TestFlight delivery alone does not
  prove release eligibility.
  References (14 October 2026): [Apple workflow configuration](https://developer.apple.com/documentation/xcode/creating-a-workflow-that-builds-your-app-for-distribution)
  and [internal-only build restrictions](https://developer.apple.com/help/app-store-connect/test-a-beta-version/add-internal-testers/).
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

### Change scope

Apply the same rule across every project: run a job when a change can affect its
output or the behavior it checks. Each repository owns its actual path filters.
Exclude only confirmed internal documentation, release materials and unrelated
component inputs. Unknown paths still run. Do not exclude all Markdown or text:
Whetstone imports `skill-template/self-improvement-section.md` into its app,
Werkout uses text corpus fixtures, and this portal publishes support/privacy pages
and font license files. Dependencies, localization, migrations and shared contracts
remain inputs. Mixed documentation/source changes must run the affected jobs.

- Single-product Actions workflows use explicit `paths-ignore` lists. Manual runs
  bypass those lists; release-tag builds retain their existing behavior.
- Mampf's web checks skip confirmed native-only files, while Apple checks skip
  web UI trees. API, shared data, migrations and unknown/configuration paths still
  run the Apple checks. JavaScript/TypeScript in `apple/` remains in web CI scope
  because the root tools include it. Its Vercel ignore command compares against
  the last successful deployment, builds when history is unavailable, and can be
  bypassed with `CI_FORCE_BUILD=1` or the redeploy dialog's ignore-step override.
- `ytmusic-watch` runs one cheap change-selection and secret-scan job on every PR
  and main push, including docs-only changes. Backend, Docker, Go bridge, Swift
  core and the opt-in Watch build run conditionally. Shared contracts, unknown
  inputs and unavailable history run all eligible jobs. Git diffs cover the whole
  push or PR merge base and both sides of renames. The secret scan remains global.
- King's Cup and Heischwumm keep test-only changes in CI but skip Pages deployment
  for their excluded unit/E2E inputs. Shipped assets still deploy.
- Before making a path-filtered workflow a required check, remove its event-level
  path filter and use an always-running gate with conditional jobs. Require the
  gate as well, so a failed change detector cannot produce an apparently green PR.

### Xcode Cloud file conditions

Each Apple repository records the live `branchStartCondition.filesAndFoldersRule`
in `.github/xcode-cloud-paths.json`. Xcode Cloud does **not** read that file
automatically. Its `Main to TestFlight` workflow uses **Do not start a build if
only the following files and folders have changed**, limited to confirmed internal
documentation and release materials. Mixed changes, source, fixtures and build
configuration continue to trigger it; manual start conditions are preserved.
Apple's filename rules match that name at any depth, and folder rules are
recursive. The excluded names (`README.md`, `AGENTS.md`, `CLAUDE.md`, `SECURITY.md`
and the recorded review notes) are internal documentation in the current Apple
projects. Revisit the live rule before bundling a file with one of those names;
never replace these specific names with a blanket Markdown-extension exclusion.

Edit the live workflow through App Store Connect/Xcode and keep the JSON in sync.
When using the API, send all existing automatic **and manual** start conditions:
omitting another condition can clear it. Re-read the workflow after saving and
verify that only the intended file rule changed, including checking archive,
TestFlight, branch, toolchain and manual-start settings.

### Portal deployment

`.github/workflows/deploy.yml` validates and packages the static site, excluding
only internal repository files. Product content, including future nested Markdown,
is retained. Settings → Pages → Source is **GitHub Actions** (checked 30 October
2026), so this workflow is the only deployment and its path filters apply. If the
source is ever set back to **Deploy from a branch**, GitHub's automatic
`pages-build-deployment` deploys every main push again, regardless of these filters.

### Validation of trigger changes

Lint modified workflows with `actionlint`; exercise docs-only, mixed, shipped
content, lockfile, configuration, fixture and unknown-path cases. For component
selection also test multi-commit pushes, PR merge bases, deletion/renames and
missing history. The repository-owned executable regression tests are:

- `ytmusic-watch`: `python3 -m unittest discover -s .github/scripts -p 'test_*.py'`.
- `mampf`: `node --test scripts/vercel-ignore.test.mjs`.

Local filter checks establish routing behavior, not a successful hosted app build
or deployment. Report publication and live execution separately.

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

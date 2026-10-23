# ScreamXY portal

- Plain HTML/CSS, no build step. Preserve root-absolute links and the legacy `#/…` redirect to `/heischwumm/`.
- `/heischwumm/` and `/kingscup/` are served by separate repositories. Never add their build output here.
- Run `python3 -I scripts/check.py` and `git diff --check`. Check layout at 320px, phone, tablet and desktop widths after UI changes.
- Each listed app needs a support page and privacy link. Mampf's privacy policy lives in its web app. Base privacy claims on actual code and update the policy date when its behavior changes.
- `RELEASE.md` is the shared release/CI checklist; app-specific release kits stay in their repositories.

## Shared release and CI rules

- Public support and security contact: `screamcode@gmail.com`. Keep in-app contact details, portal policies and App Store metadata consistent.
- `AGENTS.md` owns the rules. `CLAUDE.md` contains only: `See @AGENTS.md for monorepo documentation and guidelines.`
- Every Actions job needs a finite timeout and minimal permissions. Cancel superseded checks, but let an active production deployment finish.
- Exclude confirmed internal documentation from app builds. Documentation shipped in the product remains a build input. Scope jobs to their component and shared dependencies; unknown paths still run. Keep fixtures, migrations, dependency locks, localization and build configuration in CI scope.
- GitHub runners are for fast lint, type checks, deterministic unit tests and compilation only. Extensive browser E2E, simulator/device suites and screenshots run locally, including when agents code; do not add hosted opt-ins for them. Never run paid AI calls, live provider corpus runs, production database tests or signing/publishing as routine PR checks.
- Keep artifacts short-lived (7 days or less), and release bundles limited to tags/manual runs. Cheap lint, type checks, deterministic tests and compilation remain automatic.
- Release status lives in the Obsidian vault: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Privat/Development/ScreamXY/` (`ScreamXY.md`, `TODO.md`). If unavailable, say so. Distinguish prepared files, published pages, CI results and hardware verification.

## Local validation required for relevant changes

`python3 -I scripts/check.py --workspace`, plus desktop/mobile browser checks for layout and links. The normal portal Actions job runs only the dependency-free content check.

Run the affected suites before committing and report what actually ran. Keep tests
and local scripts even when their hosted jobs are removed. Do not increase a CI
timeout to hide a hang; inspect the failure first.

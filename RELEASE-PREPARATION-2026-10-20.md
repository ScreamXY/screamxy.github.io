# App Store preparation — 20 October 2026

All five version drafts were reopened and verified in App Store Connect. **No review reply, submission, resubmission or app release was made.** Manual release remains selected for every app. Work is on each repository's `main` branch.

| App | Selected build | Prepared / saved | Next release gate |
| --- | --- | --- | --- |
| RainScope | 1.0 (8) | Lighter icon build, correction notes, two Watch screenshots | Installed Watch icon check, owner's review, reply/resubmission |
| Pacegrain | 1.0.0 (5) | Six requested answers, simulator rehearsal and repeatable physical steps | Physical-device recording on latest public OS; three tips still drafts |
| PulseGlance | 1.0 (7) | Updated percentage/quarter-marker listing and notes, two Watch screenshots | Physical Watch legibility, HealthKit/privacy and remaining acceptance checks |
| Werkout | 1.0.0 (2) | EN/DE listing and required screenshots, contact/notes, free/175 regions, age/medical declaration, three tip drafts, unpublished privacy draft | Rights confirmation, provider privacy review, tip screenshots/inclusion, device gates |
| Mampf! | 1.0.0 (2) | DE listing, 8 iPhone/8 iPad/1 Watch screenshots, contact/notes, free/175 regions, three tip drafts, unpublished privacy draft | Rights confirmation, IP/log privacy review, tip screenshots/inclusion, device gates |

## Open the app-specific handoff

- [RainScope checklist](https://github.com/ScreamXY/rainscope/blob/main/docs/app-store/RELEASE-CHECKLIST.md)
- [Pacegrain checklist](https://github.com/ScreamXY/pacegrain/blob/main/docs/app-store/RELEASE-CHECKLIST.md) and [recording rehearsal](https://github.com/ScreamXY/pacegrain/blob/main/docs/app-store/rehearsal/README.md)
- [PulseGlance checklist](https://github.com/ScreamXY/pulseglance/blob/main/docs/app-store/RELEASE-CHECKLIST.md)
- [Werkout preparation](https://github.com/ScreamXY/werkout/blob/main/AppStore/PREPARATION.md)
- [Mampf preparation](https://github.com/ScreamXY/mampf/blob/main/apple/AppStore/PREPARATION.md)

Pacegrain's MP4 is a simulator practice recording, explicitly identified in its README. It is not attached to Apple and does not satisfy the requested physical-device evidence. The guide includes the split/Compare scroll steps not visible in the rehearsal. The original full-resolution capture remains on the Mac's Desktop.

## Filings still needing review

Werkout's old blanket Data Not Collected instruction was incorrect for optional remote parsing. The listing and portal privacy text now distinguish the default local path from provider requests. Its three-category draft is saved, not published; provider security-log retention and purposes need confirmation.

Mampf's draft contains six categories. Five are configured for app functionality, linked to the user, without tracking. The security IP category remains unconfigured until hosting/provider log linkage and retention are checked. The public policy already describes security IP collection and opportunistic cleanup. The source worksheets record both the evidence and the unresolved questions.

Content-rights declarations for Werkout and Mampf remain unset pending the owner's confirmation. No legal agreements, banking/tax records or trader-status decisions were changed. Optional Accessibility Nutrition Labels remain unclaimed until the actual accessibility checks are completed.

Werkout and Mampf each have three created consumables with prices/localizations/notes, but still need a screenshot of their actual tip section and inclusion with the first app review. Pacegrain's existing three products also show Prepare for Submission. Creation and sandbox testing are not product approval.

## Validation and limits

- Character limits checked; saved note lengths: RainScope 1,309, Pacegrain 3,598, PulseGlance 1,441, Werkout 3,030, Mampf 2,977.
- Werkout screenshot generator ran successfully; all 12 new medium iPhone files are opaque RGB PNGs, 1206 × 2622, with preserved source aspect ratio. The existing larger assets were unchanged.
- Rehearsal MP4 decoded successfully and a sampled frame was inspected. No purchase or share was sent during capture.
- Portal workspace/content check and repository whitespace checks passed. No app runtime source or signing configuration changed in this preparation.
- No new physical testing, production database write tests or paid AI calls were performed. Existing open device and parsing-quality gates remain open.

Delivery evidence (commit SHAs and hosted checks) is recorded in the Obsidian release-preparation note. `RELEASE.md` remains the reusable shared checklist.

# screamxy.github.io

The ScreamXY portal: one start page for all apps, plus the support page and
privacy policy App Store Connect asks for. Plain HTML and one stylesheet, no
build step. GitHub Pages serves the `master` branch as is.

| Path                    | What                                               |
| ----------------------- | -------------------------------------------------- |
| `index.html`            | Start page listing every app                       |
| `apps/<app>/`           | Support page (App Store Connect "Support URL")     |
| `apps/<app>/privacy/`   | Privacy policy (App Store Connect "Privacy Policy URL") |
| `legal/`                | Legal notice / Impressum                           |
| `privacy/`              | Privacy notice for this site itself                |
| `scripts/check.py`      | Link and placeholder check, run before publishing  |

Mampf's privacy policy stays in the Mampf web app
(<https://mampf-phi.vercel.app/privacy>); `apps/mampf/` is only the support
page and links there.

The web apps are served by their own repositories' GitHub Pages under this
domain and must not be put here: <https://screamxy.github.io/heischwumm/>
(ScreamXY/heischwumm) and <https://screamxy.github.io/kingscup/>
(ScreamXY/kingscup).

## Editing

- Each iOS app's pages are the source of truth here; the app repos point to
  these URLs from `*Links.swift` and their App Store listings.
- Keep `screamcode@gmail.com` out of committed pages: `python3 -I scripts/check.py`
  fails while a placeholder is left.
- Dates: update the "Last updated" line of a policy whenever its content
  changes.

## History

Until October 2026 this repository held the built Heischwumm app, pushed by
Heischwumm's deploy workflow. The portal's start page redirects old
`#/...` bookmarks to `/heischwumm/`.

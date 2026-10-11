# screamxy.github.io

The ScreamXY portal: one start page for all apps, plus the support page and
privacy policy App Store Connect asks for. Plain HTML and one stylesheet, no
build step. GitHub Pages serves the `master` branch as is.

| Path                                  | What                                                        |
| ------------------------------------- | ----------------------------------------------------------- |
| `index.html`                          | Start page listing every app                                |
| `apps/<app>/`                         | Support page (App Store Connect "Support URL")              |
| `apps/<app>/privacy/`                 | Privacy policy (App Store Connect "Privacy Policy URL")     |
| `legal/`                              | Legal notice / Impressum                                    |
| `privacy/`                            | Privacy notice for this site itself                         |
| `scripts/check.py`                    | Link, contact-address and date check; run before publishing |
| `fonts/`                              | Signika, self-hosted (SIL OFL); no fonts from third parties |
| `favicon.svg`                         | Site icon: `<!>`, a scream in code brackets (screamcode)    |
| `favicon.ico`, `apple-touch-icon.png` | Rendered from `favicon.svg` by `scripts/make_icons.py`      |

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
- The contact address is `CONTACT_EMAIL` in `scripts/check.py`; the check fails
  if any page uses another one. To change it, edit the constant and grep.
- Shared policy sections ("Who is responsible", "Hosting", "Your rights",
  "Changes", and their German forms) use one wording on every page; paste it
  verbatim so drift shows up in `git grep`.
- Stylesheet and home links are root-absolute (`/style.css`, `/`); the user
  site is always served from the domain root.
- Dates: update the "Last updated" line of a policy whenever its content
  changes.

## History

Until October 2026 this repository held the built Heischwumm app, pushed by
Heischwumm's deploy workflow. The portal's start page redirects old
`#/...` bookmarks to `/heischwumm/`.

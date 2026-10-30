#!/usr/bin/env python3
"""Checks the portal before publishing.

- Every internal link resolves to a file in this repository.
- Every mailto: link uses CONTACT_EMAIL, and every page outside the start and
  404 pages names it, so changing the address is one edit here plus a grep.
- Every page has the shared head: viewport and /style.css.
- Every privacy page carries a "last updated" line.
- No path served by another repository's GitHub Pages exists here.
- The app inventory has support/privacy links on the portal.
- With --workspace, sibling repositories have native contacts and agent/security files.

Usage: python3 -I scripts/check.py [--workspace]
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTACT_EMAIL = 'screamcode@gmail.com'
CLAUDE_REDIRECT = 'See @AGENTS.md for monorepo documentation and guidelines.'
# Served by other repositories' GitHub Pages under the same domain.
EXTERNAL_PATHS = ('/heischwumm/', '/kingscup/')
# Redirects from renamed app paths carry neither a contact line nor a policy date.
REDIRECTS = {'apps/heartglance/index.html', 'apps/heartglance/privacy/index.html'}
NO_CONTACT = {'index.html', '404.html'} | REDIRECTS
SHARED_HEAD = ('<meta name="viewport"', 'href="/style.css"')

App = dict[str, str | None]


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def check_inventory(apps: list[App]) -> list[str]:
    problems = []
    home = read(ROOT / 'index.html')
    for app in apps:
        if not (ROOT / 'apps' / str(app['id']) / 'index.html').is_file():
            problems.append(f'{app["id"]}: missing support page')
        for href in (f'apps/{app["id"]}/', str(app['privacy'])):
            if f'href="{href}"' not in home and f'href="{href.lstrip("/")}"' not in home:
                problems.append(f'{app["id"]}: missing portal link {href}')
    return problems


def check_workspace(apps: list[App]) -> list[str]:
    problems = []
    for name in [str(app['id']) for app in apps] + [ROOT.name]:
        repo = ROOT.parent / name
        for filename in ('AGENTS.md', 'CLAUDE.md', 'SECURITY.md'):
            if not (repo / filename).is_file():
                problems.append(f'{name}: missing {filename}')
        claude = repo / 'CLAUDE.md'
        if claude.is_file() and read(claude).strip() != CLAUDE_REDIRECT:
            problems.append(f'{name}: CLAUDE.md must redirect to AGENTS.md')
        security = repo / 'SECURITY.md'
        if security.is_file() and CONTACT_EMAIL not in read(security):
            problems.append(f'{name}: missing security contact')
        if not list((repo / '.github' / 'workflows').glob('*.y*ml')):
            problems.append(f'{name}: no Actions workflows')
    for app in apps:
        if app['native_contact']:
            source = ROOT.parent / str(app['id']) / app['native_contact']
            if not source.is_file() or CONTACT_EMAIL not in read(source):
                problems.append(f'{app["id"]}: missing native contact address')
    return problems


def check_page(page: Path) -> list[str]:
    problems = []
    text = read(page)
    rel = page.relative_to(ROOT).as_posix()

    for email in re.findall(r'href="mailto:([^"]+)"', text):
        if email != CONTACT_EMAIL:
            problems.append(f'{rel}: contact address {email} differs from {CONTACT_EMAIL}')
    if rel not in NO_CONTACT and CONTACT_EMAIL not in text:
        problems.append(f'{rel}: no contact address')
    for marker in SHARED_HEAD:
        if marker not in text:
            problems.append(f'{rel}: head lacks {marker}')
    is_policy = rel.endswith('privacy/index.html') and rel not in REDIRECTS
    if is_policy and not re.search(r'class="meta">(Last updated|Stand):', text):
        problems.append(f"{rel}: no 'last updated' line")

    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        path = href.split('#')[0]
        if path.startswith(EXTERNAL_PATHS):
            continue
        target = ROOT / path.lstrip('/') if path.startswith('/') else page.parent / path
        if path.endswith('/'):
            target = target / 'index.html'
        if not target.exists():
            problems.append(f'{rel}: broken link {href}')
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description='Check the portal before publishing.')
    parser.add_argument('--workspace', action='store_true', help='also check the sibling app repositories')
    args = parser.parse_args()

    apps: list[App] = json.loads(read(ROOT / 'apps.json'))
    pages = sorted(p for p in ROOT.rglob('*.html') if '.git' not in p.parts)

    problems = check_inventory(apps)
    if args.workspace:
        problems += check_workspace(apps)
    for external in EXTERNAL_PATHS:
        if (ROOT / external.strip('/')).exists():
            problems.append(f'{external} belongs to another repository and must not exist here')
    for page in pages:
        problems += check_page(page)

    for problem in problems:
        print(problem)
    print(f'{len(pages)} pages checked, {len(problems)} problem(s)')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())

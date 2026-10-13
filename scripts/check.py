#!/usr/bin/env python3
"""Checks the portal before publishing.

- Every internal link resolves to a file in this repository.
- Every mailto: link uses CONTACT_EMAIL, and every page outside the start and
  404 pages names it, so changing the address is one edit here plus a grep.
- Every privacy page carries a "last updated" line.
- No path served by another repository's GitHub Pages exists here.
- The app inventory has support/privacy links on the portal.
- With --workspace, sibling repositories have native contacts and agent/security files.

Usage: python3 -I scripts/check.py [--workspace]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTACT_EMAIL = "screamcode@gmail.com"
# Served by other repositories' GitHub Pages under the same domain.
EXTERNAL_PATHS = ("/heischwumm/", "/kingscup/")
NO_CONTACT = {"index.html", "404.html"}

problems = []
pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
home = (ROOT / "index.html").read_text(encoding="utf-8")
for app in apps:
    support = ROOT / "apps" / app["id"] / "index.html"
    if not support.is_file():
        problems.append(f"{app['id']}: missing support page")
    for href in (f"apps/{app['id']}/", app["privacy"]):
        if f'href="{href}"' not in home and f'href="{href.lstrip("/")}"' not in home:
            problems.append(f"{app['id']}: missing portal link {href}")

if "--workspace" in sys.argv:
    for name in [app["id"] for app in apps] + [ROOT.name]:
        repo = ROOT.parent / name
        for filename in ("AGENTS.md", "CLAUDE.md", "SECURITY.md"):
            if not (repo / filename).is_file():
                problems.append(f"{name}: missing {filename}")
        claude = repo / "CLAUDE.md"
        if claude.is_file() and claude.read_text().strip() != "See @AGENTS.md for monorepo documentation and guidelines.":
            problems.append(f"{name}: CLAUDE.md must redirect to AGENTS.md")
        security = repo / "SECURITY.md"
        if security.is_file() and CONTACT_EMAIL not in security.read_text():
            problems.append(f"{name}: missing security contact")
        if not list((repo / ".github" / "workflows").glob("*.y*ml")):
            problems.append(f"{name}: no Actions workflows")
    for app in apps:
        if app["native_contact"]:
            source = ROOT.parent / app["id"] / app["native_contact"]
            if not source.is_file() or CONTACT_EMAIL not in source.read_text():
                problems.append(f"{app['id']}: missing native contact address")

for external in EXTERNAL_PATHS:
    if (ROOT / external.strip("/")).exists():
        problems.append(f"{external} belongs to another repository and must not exist here")

for page in pages:
    text = page.read_text(encoding="utf-8")
    rel = page.relative_to(ROOT).as_posix()

    for email in re.findall(r'href="mailto:([^"]+)"', text):
        if email != CONTACT_EMAIL:
            problems.append(f"{rel}: contact address {email} differs from {CONTACT_EMAIL}")
    if rel not in NO_CONTACT and CONTACT_EMAIL not in text:
        problems.append(f"{rel}: no contact address")
    if rel.endswith("privacy/index.html") and not re.search(r'class="meta">(Last updated|Stand):', text):
        problems.append(f"{rel}: no 'last updated' line")

    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = href.split("#")[0]
        if path.startswith(EXTERNAL_PATHS):
            continue
        target = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
        if path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            problems.append(f"{rel}: broken link {href}")

for problem in problems:
    print(problem)
print(f"{len(pages)} pages checked, {len(problems)} problem(s)")
sys.exit(1 if problems else 0)

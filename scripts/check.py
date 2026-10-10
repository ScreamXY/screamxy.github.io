#!/usr/bin/env python3
"""Checks the portal before publishing.

- Every internal link resolves to a file in this repository.
- Every mailto: link uses CONTACT_EMAIL, and every page outside the start and
  404 pages names it, so changing the address is one edit here plus a grep.
- Every privacy page carries a "last updated" line.
- No path served by another repository's GitHub Pages exists here.

Usage: python3 -I scripts/check.py
"""
import os
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

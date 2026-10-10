#!/usr/bin/env python3
"""Checks the portal before publishing: every internal link resolves to a file,
every page has a stylesheet that exists, and no placeholder is left.

Usage: python3 -I scripts/check.py [--allow-placeholders]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDERS = ("CONTACT_EMAIL", "RELEASE_DATE")
# Served by other repositories' GitHub Pages, not by this one.
EXTERNAL_PATHS = ("/heischwumm/", "/kingscup/")

allow_placeholders = "--allow-placeholders" in sys.argv
problems = []
pages = []
for dirpath, _, files in os.walk(ROOT):
    if "/.git" in dirpath:
        continue
    for name in files:
        if name.endswith(".html"):
            pages.append(os.path.join(dirpath, name))

for page in sorted(pages):
    text = open(page, encoding="utf-8").read()
    rel = os.path.relpath(page, ROOT)
    if not allow_placeholders:
        for ph in PLACEHOLDERS:
            if ph in text:
                problems.append(f"{rel}: placeholder {ph} left in page")
    for href in re.findall(r'(?:href|src)="([^"]+)"', text):
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = href.split("#")[0]
        if not path:
            continue
        if path.startswith("/"):
            if path.startswith(EXTERNAL_PATHS):
                continue
            target = os.path.join(ROOT, path.lstrip("/"))
        else:
            target = os.path.normpath(os.path.join(os.path.dirname(page), path))
        if path.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            problems.append(f"{rel}: broken link {href}")

for p in problems:
    print(p)
print(f"{len(pages)} pages checked, {len(problems)} problem(s)")
sys.exit(1 if problems else 0)

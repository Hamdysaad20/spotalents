#!/usr/bin/env python3
"""
DRY Footer Synchronizer for SpotTalents.
Reads the single source of truth from components/footer.html
and synchronizes it across all HTML pages in the project.
"""

import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPONENT_PATH = os.path.join(ROOT_DIR, "components", "footer.html")

TARGET_FILES = [
    "index.html",
    "about/index.html",
    "features/index.html",
    "solution/index.html",
    "pricing/index.html",
    "start/index.html"
]

FOOTER_REGEX = re.compile(
    r"(<!--\s*Footer Component\s*-->\s*)?<section data-wf--footer--variant=\"base\" class=\"section footer\">.*?</section>",
    re.DOTALL
)

def sync_footer():
    if not os.path.exists(COMPONENT_PATH):
        raise FileNotFoundError(f"Component not found at {COMPONENT_PATH}")

    with open(COMPONENT_PATH, "r", encoding="utf-8") as f:
        canonical_footer = f.read().strip()

    updated = []
    for rel_path in TARGET_FILES:
        abs_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(abs_path):
            print(f"[SKIP] File not found: {rel_path}")
            continue

        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not FOOTER_REGEX.search(content):
            print(f"[WARN] No footer section matched in: {rel_path}")
            continue

        new_content = FOOTER_REGEX.sub(canonical_footer, content, count=1)
        if new_content != content:
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated.append(rel_path)
            print(f"[SYNCED] {rel_path}")
        else:
            print(f"[UNCHANGED] {rel_path}")

    print(f"\nDone. {len(updated)}/{len(TARGET_FILES)} files synchronized from {COMPONENT_PATH}.")

if __name__ == "__main__":
    sync_footer()

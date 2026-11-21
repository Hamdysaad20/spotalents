#!/usr/bin/env python3
"""
DRY Component Synchronizer for SpotTalents.
Single source of truth component manager for:
- components/navbar.html
- components/cta.html
- components/footer.html

Synchronizes components across all HTML pages, including the blog system,
ensuring 100% DRY architecture and visual consistency.
"""

import os
import re
import sys
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPONENTS_DIR = os.path.join(ROOT_DIR, "components")

NAVBAR_PATH = os.path.join(COMPONENTS_DIR, "navbar.html")
CTA_PATH = os.path.join(COMPONENTS_DIR, "cta.html")
FOOTER_PATH = os.path.join(COMPONENTS_DIR, "footer.html")

# Regex pattern for Footer (including any legacy duplicated closing tags)
FOOTER_REGEX = re.compile(
    r"(<!--\s*Footer Component\s*-->\s*)?<section[^>]*class=[\"'][^\"']*footer[^\"']*[\"'][^>]*>.*?</section>(?:\s*</div>\s*</div>\s*</div>\s*</section>)*",
    re.DOTALL
)

# Regex pattern for Navbar (including any skip link and looking ahead to main/section/hero)
NAVBAR_REGEX = re.compile(
    r"(?:<!--\s*Skip to Content Bypass Link\s*-->\s*<a[^>]*class=[\"'][^\"']*skip-to-content[^\"']*[\"'][^>]*>.*?</a>\s*)*(<!--\s*(?:Navigation Bar|Navbar)(?:\s*Component)?\s*-->\s*)?<div[^>]*class=[\"'][^\"']*navbar\s+w-nav[^\"']*[\"'][^>]*>.*?(?=<!--\s*(?:Hero|Main|Section|Start|Breadcrumbs|Article)|\s*<main|\s*<section|\s*<article|\s*<div[^>]*class=[\"'][^\"']*(?:hero|section|page-wrap|start-container|content-wrap|about-hero))",
    re.DOTALL
)

# Regex pattern for Call to Action
CTA_REGEX = re.compile(
    r"(<!--\s*(?:Call to Action|CTA)(?:\s*Section|\s*Component)?\s*-->\s*)?<section[^>]*class=[\"'][^\"']*(?:cta|section cta)[^\"']*[\"'][^>]*>.*?</section>",
    re.DOTALL
)

# Regex for blog index ad-hoc CTA
BLOG_INDEX_CTA_REGEX = re.compile(
    r"<!--\s*CTA Section\s*-->\s*<section[^>]*class=[\"'][^\"']*section[^\"']*[\"'][^>]*style=[\"'][^\"']*background-color:\s*#f8f9ef[^\"']*[\"'][^>]*>.*?</section>",
    re.DOTALL
)

def find_target_files():
    """Discover all HTML files in the project, excluding components and node_modules."""
    html_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "components", ".vercel", "scratch")]
        for file in files:
            if file.endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, file), ROOT_DIR)
                html_files.append(rel_path)
    return sorted(html_files)

def sync_footer(content, canonical_footer):
    """Replace any footer with the canonical footer."""
    m = FOOTER_REGEX.search(content)
    if not m:
        return content, False
    if m.group(0).strip() == canonical_footer.strip():
        return content, False
    new_content = content[:m.start()] + canonical_footer + content[m.end():]
    return new_content, True

def sync_navbar(content, canonical_navbar):
    """Replace any navbar with the canonical navbar."""
    m = NAVBAR_REGEX.search(content)
    if not m:
        return content, False
    if m.group(0).strip() == canonical_navbar.strip():
        return content, False
    new_content = content[:m.start()] + canonical_navbar + "\n\n  " + content[m.end():]
    return new_content, True

def sync_cta(content, rel_path, canonical_cta):
    """Sync CTA section. start/index.html is preserved with its custom form CTA."""
    if rel_path == "start/index.html":
        return content, False

    # Check for existing standard CTA
    m = CTA_REGEX.search(content)
    if m:
        if m.group(0).strip() == canonical_cta.strip():
            return content, False
        new_content = content[:m.start()] + canonical_cta + content[m.end():]
        return new_content, True

    # Check for blog index ad-hoc CTA
    m_blog = BLOG_INDEX_CTA_REGEX.search(content)
    if m_blog:
        new_content = content[:m_blog.start()] + canonical_cta + content[m_blog.end():]
        return new_content, True

    # For blog posts that don't have CTA yet, insert right before Footer
    if rel_path.startswith("blog/") and rel_path != "blog/index.html":
        m_foot = FOOTER_REGEX.search(content)
        if m_foot:
            pos = m_foot.start()
            new_content = content[:pos] + canonical_cta + "\n\n  " + content[pos:]
            return new_content, True

    return content, False

def standardize_blog_assets(content, rel_path):
    """Standardize relative asset paths in blog pages to root-relative paths and fix scripts."""
    if not rel_path.startswith("blog/"):
        return content, False

    original = content
    # Replace relative css/lenis/webfont paths
    content = content.replace('href="../css/', 'href="/css/')
    content = content.replace('href="../../css/', 'href="/css/')
    content = content.replace('src="../js/webfont.js"', 'src="/js/webfont.js"')
    content = content.replace('src="../../js/webfont.js"', 'src="/js/webfont.js"')
    content = content.replace('href="../images/6ac26a71c118dcab5930bb0a_Fav', 'href="/images/6ac26a71c118dcab5930bb0a_Fav')
    content = content.replace('href="../../images/6ac26a71c118dcab5930bb0a_Fav', 'href="/images/6ac26a71c118dcab5930bb0a_Fav')

    # Fix script tags at bottom of blog index
    if rel_path == "blog/index.html":
        content = content.replace('<script src="../js/jquery.js" type="text/javascript"></script>', '<script src="/js/jquery-3.5.1.min.dc5e7f18c8.js" type="text/javascript"></script>')
        content = content.replace('<script src="../js/webflow-core.js" type="text/javascript"></script>', '<script src="/js/spotalents.chunk.36b8fb49256177c8.js" type="text/javascript"></script>\n<script src="/js/spotalents.chunk.d5ced0f8a8550fc9.js" type="text/javascript"></script>')
        content = content.replace('<script src="/js/sticky-navbar.js" type="text/javascript"></script>', '')

    # Fix script tags at bottom of blog posts
    elif rel_path.startswith("blog/"):
        content = content.replace('<script src="/js/sticky-navbar.js" type="text/javascript"></script>', '')
        content = content.replace('<script src="../../js/sticky-navbar.js" type="text/javascript"></script>', '')
        content = content.replace('<script src="../js/sticky-navbar.js" type="text/javascript"></script>', '')
        if "spotalents.chunk.36b8fb49256177c8.js" not in content:
            old_script_block = re.search(r'(<script src="(?:\.\./)*js/sticky-navbar\.js" type="text/javascript"></script>)', content)
            if old_script_block:
                new_scripts = (
                    '<script src="/js/jquery-3.5.1.min.dc5e7f18c8.js" type="text/javascript"></script>\n'
                    '<script src="/js/spotalents.chunk.36b8fb49256177c8.js" type="text/javascript"></script>\n'
                    '<script src="/js/spotalents.chunk.d5ced0f8a8550fc9.js" type="text/javascript"></script>'
                )
                content = content[:old_script_block.start()] + new_scripts + content[old_script_block.end():]

    return content, content != original

def sync_all(sync_nav=True, sync_call_to_action=True, sync_foot=True):
    target_files = find_target_files()
    print(f"Target HTML files ({len(target_files)}): {', '.join(target_files)}\n")

    canonical_footer = ""
    if sync_foot and os.path.exists(FOOTER_PATH):
        with open(FOOTER_PATH, "r", encoding="utf-8") as f:
            canonical_footer = f.read().strip()

    canonical_navbar = ""
    if sync_nav and os.path.exists(NAVBAR_PATH):
        with open(NAVBAR_PATH, "r", encoding="utf-8") as f:
            canonical_navbar = f.read().strip()

    canonical_cta = ""
    if sync_call_to_action and os.path.exists(CTA_PATH):
        with open(CTA_PATH, "r", encoding="utf-8") as f:
            canonical_cta = f.read().strip()

    updated_count = 0
    for rel_path in target_files:
        abs_path = os.path.join(ROOT_DIR, rel_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()

        file_changed = False
        changes = []

        if sync_nav and canonical_navbar:
            content, changed = sync_navbar(content, canonical_navbar)
            if changed:
                file_changed = True
                changes.append("navbar")

        if sync_call_to_action and canonical_cta:
            content, changed = sync_cta(content, rel_path, canonical_cta)
            if changed:
                file_changed = True
                changes.append("cta")

        if sync_foot and canonical_footer:
            content, changed = sync_footer(content, canonical_footer)
            if changed:
                file_changed = True
                changes.append("footer")

        content, changed = standardize_blog_assets(content, rel_path)
        if changed:
            file_changed = True
            changes.append("assets")

        if file_changed:
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            updated_count += 1
            print(f"[SYNCED] {rel_path} ({', '.join(changes)})")
        else:
            print(f"[UNCHANGED] {rel_path}")

    print(f"\nDone. {updated_count}/{len(target_files)} files updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize SpotTalents components across all HTML files.")
    parser.add_argument("--footer", action="store_true", help="Sync footer component only")
    parser.add_argument("--navbar", action="store_true", help="Sync navbar component only")
    parser.add_argument("--cta", action="store_true", help="Sync CTA component only")
    args = parser.parse_args()

    if args.footer or args.navbar or args.cta:
        sync_all(sync_nav=args.navbar, sync_call_to_action=args.cta, sync_foot=args.footer)
    else:
        sync_all(sync_nav=True, sync_call_to_action=True, sync_foot=True)

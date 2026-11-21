#!/usr/bin/env python3
"""
SEO & Social Graph Metadata Enhancer for SpotTalents.
- Injects canonical URLs across all pages
- Standardizes og:image and twitter:image to absolute https://spotalents.com URLs
- Injects og:url matching canonical
- Injects rich Schema.org JSON-LD structured data (Organization, WebSite, FAQPage, NewsArticle)
"""

import os
import re
import json
import glob

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://spotalents.com"
DEFAULT_SOCIAL_IMAGE = f"{BASE_URL}/images/6abc120c9cbe81e3c6b4df09_Social%20Share%20%285%29.png"

def get_canonical_url(rel_path):
    if rel_path == "index.html":
        return f"{BASE_URL}/"
    if rel_path == "404.html":
        return None
    clean_path = rel_path.replace("/index.html", "").replace("index.html", "")
    return f"{BASE_URL}/{clean_path}"

def extract_faqs(content):
    cards = re.findall(
        r'<div class=[\"\x27]faq-card-title[\"\x27]>(.*?)</div>.*?<div class=[\"\x27]faq-details-wrap[\"\x27]>(.*?)</div>',
        content,
        re.DOTALL
    )
    faqs = []
    for q, a in cards:
        clean_q = re.sub(r'<[^>]+>', '', q).strip()
        clean_a = re.sub(r'<[^>]+>', '', a).strip()
        if clean_q and clean_a:
            faqs.append({
                "@type": "Question",
                "name": clean_q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": clean_a
                }
            })
    return faqs

def enhance_page(rel_path):
    abs_path = os.path.join(ROOT_DIR, rel_path)
    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()

    canonical = get_canonical_url(rel_path)
    head_end = content.find("</head>")
    if head_end == -1:
        print(f"Skipping {rel_path}: no </head>")
        return

    head = content[:head_end]
    rest = content[head_end:]

    # 1. Canonical Tag
    if canonical:
        if '<link rel="canonical"' in head:
            head = re.sub(r'<link rel=[\"\x27]canonical[\"\x27][^>]*>', f'<link rel="canonical" href="{canonical}">', head)
        else:
            # Insert after <title>
            title_m = re.search(r'(</title>)', head)
            if title_m:
                pos = title_m.end()
                head = head[:pos] + f'\n<link rel="canonical" href="{canonical}">' + head[pos:]
            else:
                head += f'\n<link rel="canonical" href="{canonical}">'

    # 2. og:url Tag
    if canonical:
        if '<meta property="og:url"' in head or '<meta content=' in head and 'property="og:url"' in head:
            head = re.sub(r'<meta[^>]*property=[\"\x27]og:url[\"\x27][^>]*>', f'<meta property="og:url" content="{canonical}">', head)
            head = re.sub(r'<meta[^>]*content=[\"\x27][^\"]*[\"\x27][^>]*property=[\"\x27]og:url[\"\x27][^>]*>', f'<meta property="og:url" content="{canonical}">', head)
        else:
            head += f'\n<meta property="og:url" content="{canonical}">'

    # 3. Determine Social Image
    social_image = DEFAULT_SOCIAL_IMAGE
    if rel_path.startswith("blog/") and rel_path != "blog/index.html":
        # Extract hero image from blog post
        img_m = re.search(r'<figure class=[\"\x27]article-hero-figure[\"\x27]>.*?<img src=[\"\x27]([^\"]+)[\"\x27]', content, re.DOTALL)
        if img_m:
            raw_img = img_m.group(1).replace("../../", "").replace("../", "").lstrip("/")
            social_image = f"{BASE_URL}/{raw_img}"
    elif rel_path == "blog/index.html":
        social_image = f"{BASE_URL}/images/press/aswan_panel_adel_danish_karima_hatem.jpg"

    # 4. Standardize og:image
    og_pattern = re.compile(r'<meta[^>]*property=[\"\x27]og:image[\"\x27][^>]*>|<meta[^>]*content=[\"\x27][^\"]*[\"\x27][^>]*property=[\"\x27]og:image[\"\x27][^>]*>')
    if og_pattern.search(head):
        head = og_pattern.sub(f'<meta property="og:image" content="{social_image}">', head)
    else:
        head += f'\n<meta property="og:image" content="{social_image}">'

    # 5. Standardize twitter:image
    tw_pattern = re.compile(r'<meta[^>]*name=[\"\x27]twitter:image[\"\x27][^>]*>|<meta[^>]*content=[\"\x27][^\"]*[\"\x27][^>]*name=[\"\x27]twitter:image[\"\x27][^>]*>')
    if tw_pattern.search(head):
        head = tw_pattern.sub(f'<meta name="twitter:image" content="{social_image}">', head)
    else:
        head += f'\n<meta name="twitter:image" content="{social_image}">'

    # 6. Schema.org Structured Data
    # Remove any existing JSON-LD scripts to avoid duplication
    head = re.sub(r'<script type=[\"\x27]application/ld\+json[\"\x27]>.*?</script>\s*', '', head, flags=re.DOTALL)

    schemas = []

    # Homepage schemas
    if rel_path == "index.html":
        schemas.append({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Spotalents",
            "url": BASE_URL,
            "logo": f"{BASE_URL}/images/6aa6b281bbff208b543d41a5_Brand%20Logo%20%282%29.svg",
            "description": "AI-Powered Talent Intelligence and Workforce Matching Engine. Contextual matching, evidence confidence, and complete engineering pods built for real-world delivery.",
            "founders": [
                {"@type": "Person", "name": "Hatem Ali"},
                {"@type": "Person", "name": "Hamdy Saad"}
            ],
            "sameAs": [
                "https://www.linkedin.com/company/spotalents"
            ]
        })
        schemas.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Spotalents",
            "url": BASE_URL
        })

    # FAQ schemas for pages that include FAQs
    if rel_path in ("index.html", "pricing/index.html", "solution/index.html", "about/index.html"):
        faqs = extract_faqs(content)
        if faqs:
            schemas.append({
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faqs
            })

    # Blog Post schemas
    if rel_path.startswith("blog/") and rel_path != "blog/index.html":
        h1_m = re.search(r'<h1[^>]*class=[\"\x27]article-headline[\"\x27]>(.*?)</h1>', content, re.DOTALL)
        lead_m = re.search(r'<p[^>]*class=[\"\x27]article-lead[\"\x27]>(.*?)</p>', content, re.DOTALL)
        meta_m = re.search(r'<div[^>]*class=[\"\x27]article-meta-header[\"\x27]>(.*?)</div>', content, re.DOTALL)

        headline = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip() if h1_m else "Spotalents News"
        description = re.sub(r'<[^>]+>', '', lead_m.group(1)).strip() if lead_m else ""
        meta_text = meta_m.group(1).strip() if meta_m else ""

        # Rough ISO date extraction from meta header (e.g. June 2025 -> 2025-06-01)
        date_iso = "2026-10-01"
        if "2025" in meta_text:
            date_iso = "2025-06-15"
        elif "November 2026" in meta_text:
            date_iso = "2026-11-01"
        elif "October 2026" in meta_text:
            date_iso = "2026-10-15"
        elif "September 2026" in meta_text:
            date_iso = "2026-09-01"

        schemas.append({
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": headline,
            "description": description,
            "image": [social_image],
            "datePublished": date_iso,
            "dateModified": date_iso,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": canonical
            },
            "author": {
                "@type": "Organization",
                "name": "Spotalents Newsroom",
                "url": f"{BASE_URL}/blog"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Spotalents",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{BASE_URL}/images/6aa6b281bbff208b543d41a5_Brand%20Logo%20%282%29.svg"
                }
            }
        })

    # Append schemas into head
    if schemas:
        schema_tags = "\n" + "\n".join([
            f'<script type="application/ld+json">\n{json.dumps(s, indent=2, ensure_ascii=False)}\n</script>'
            for s in schemas
        ])
        head += schema_tags + "\n"

    new_content = head + rest
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[ENHANCED SEO] {rel_path} (canonical={bool(canonical)}, og:image={bool(social_image)}, schemas={len(schemas)})")

def main():
    pages = [
        "index.html",
        "about/index.html",
        "features/index.html",
        "solution/index.html",
        "pricing/index.html",
        "start/index.html",
        "blog/index.html",
        "privacy/index.html",
        "terms/index.html",
        "404.html"
    ] + sorted(glob.glob("blog/*/index.html"))

    print(f"Enhancing {len(pages)} pages with comprehensive SEO & Social Metadata...")
    for p in pages:
        enhance_page(p)
    print("All pages successfully enhanced.")

if __name__ == "__main__":
    main()

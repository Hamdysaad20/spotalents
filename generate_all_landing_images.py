import os
import math
from PIL import Image, ImageDraw, ImageFont

# Fonts
FONT_BOLD = '/tmp/InstrumentSans-Bold.ttf'
FONT_REG = '/tmp/InstrumentSans.ttf'
FONT_MONO = '/tmp/SpaceMono.ttf'

# Colors
C_WHITE = (255, 255, 255, 255)
C_CARD_BG = (255, 255, 255, 255)
C_CARD_ALT = (248, 250, 252, 255)
C_BORDER = (226, 232, 240, 255)
C_BORDER_LIGHT = (241, 245, 249, 255)
C_BLUE = (1, 59, 255, 255)              # Brand Royal Blue #013BFF
C_BLUE_LIGHT = (233, 246, 255, 255)     # #E9F6FF
C_GREEN = (16, 185, 129, 255)           # #10B981
C_GREEN_LIGHT = (236, 253, 245, 255)
C_TEXT_BLACK = (15, 23, 42, 255)        # Slate 900
C_TEXT_MUTED = (100, 116, 139, 255)     # Slate 500
C_TEXT_BODY = (51, 65, 85, 255)         # Slate 700
C_RED = (239, 68, 68, 255)
C_RED_LIGHT = (254, 242, 242, 255)
C_PURPLE = (124, 58, 237, 255)
C_PURPLE_LIGHT = (245, 243, 255, 255)

def save_responsive_variants(base_img, base_path, widths):
    os.makedirs(os.path.dirname(base_path), exist_ok=True)
    base_img.save(base_path, 'AVIF', quality=95)
    png_path = base_path.replace('.avif', '.png')
    base_img.save(png_path, 'PNG')
    print(f"Saved base: {base_path} and {png_path}")

    orig_w, orig_h = base_img.size
    for w in widths:
        if w < orig_w:
            h = int(orig_h * (w / orig_w))
            res_img = base_img.resize((w, h), Image.Resampling.LANCZOS)
            var_path = base_path.replace('.avif', f'-p-{w}.avif')
            res_img.save(var_path, 'AVIF', quality=90)
            res_img.save(var_path.replace('.avif', '.png'), 'PNG')
            print(f"  Saved variant: {var_path} ({w}x{h})")

def draw_badge(draw, x, y, text, font, bg_color, text_color, radius=12, pad_x=14, pad_y=7):
    bbox = font.getbbox(text)
    bw = bbox[2] - bbox[0] + pad_x * 2
    bh = bbox[3] - bbox[1] + pad_y * 2
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=radius, fill=bg_color)
    draw.text((x + pad_x, y + pad_y - 1), text, font=font, fill=text_color)
    return bw, bh

def draw_progress_bar(draw, x, y, width, height, progress, bg_color, fill_color, radius=6):
    draw.rounded_rectangle([x, y, x + width, y + height], radius=radius, fill=bg_color)
    fw = max(height, int(width * min(1.0, progress)))
    draw.rounded_rectangle([x, y, x + fw, y + height], radius=radius, fill=fill_color)

# ==========================================
# 1. FIND IMAGE (2400 x 250)
# ==========================================
def generate_find_image():
    W, H = 4800, 500
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    f_title = ImageFont.truetype(FONT_BOLD, 32)
    f_badge = ImageFont.truetype(FONT_BOLD, 20)
    f_body = ImageFont.truetype(FONT_REG, 22)
    f_mono = ImageFont.truetype(FONT_MONO, 19)

    track_rect = [60, 40, W - 60, H - 40]
    draw.rounded_rectangle(track_rect, radius=32, fill=(255, 255, 255, 245), outline=C_BORDER, width=3)
    draw.line([(220, H // 2), (W - 220, H // 2)], fill=C_BORDER, width=6)
    draw.line([(220, H // 2), (int(W * 0.85), H // 2)], fill=C_BLUE, width=6)

    stages = [
        {"step": "0:00 // INGESTION", "title": "Role Context Ingestion", "desc": "Lead Go/K8s + React Pod", "badge": "SPEC VALIDATED", "bg": C_BLUE_LIGHT, "fg": C_BLUE},
        {"step": "0:20 // MATCHING", "title": "NIMO Signal Matching", "desc": "4,820 Evaluated → 14 Scored", "badge": "96.4% CONFIDENCE", "bg": C_GREEN_LIGHT, "fg": C_GREEN},
        {"step": "1:05 // CODE AUDIT", "title": "Git & Codebase Audit", "desc": "142 PRs Audited • 2.1h Cycle", "badge": "PRODUCTION PROOF", "bg": C_BLUE_LIGHT, "fg": C_BLUE},
        {"step": "1:30 // CALIBRATION", "title": "Squad Calibration", "desc": "Lead + 2 Seniors + QA", "badge": "97.8% CHEMISTRY", "bg": C_GREEN_LIGHT, "fg": C_GREEN},
        {"step": "3:40 // DEPLOYMENT", "title": "Activated to Production", "desc": "Shipping Code in 48 Hours", "badge": "POD LIVE // DEPLOYED", "bg": C_BLUE, "fg": C_WHITE}
    ]

    card_w = 820
    card_h = 340
    spacing = (W - 240 - (5 * card_w)) // 4
    start_x = 120

    for i, s in enumerate(stages):
        cx = start_x + i * (card_w + spacing)
        cy = (H - card_h) // 2
        card_rect = [cx, cy, cx + card_w, cy + card_h]
        is_last = (i == 4)
        c_bg = C_CARD_ALT if not is_last else (239, 246, 255, 255)
        border_col = C_BLUE if is_last else C_BORDER
        draw.rounded_rectangle(card_rect, radius=24, fill=c_bg, outline=border_col, width=3 if not is_last else 4)

        draw.text((cx + 36, cy + 32), s["step"], font=f_mono, fill=C_TEXT_MUTED)
        draw_badge(draw, cx + card_w - 240, cy + 26, s["badge"], f_badge, s["bg"], s["fg"], radius=10)

        draw.text((cx + 36, cy + 96), s["title"], font=f_title, fill=C_TEXT_BLACK)
        draw.text((cx + 36, cy + 156), s["desc"], font=f_body, fill=C_TEXT_BODY)

        draw.line([(cx + 36, cy + 225), (cx + card_w - 36, cy + 225)], fill=(226, 232, 240, 200), width=2)
        dot_color = C_GREEN if not is_last else C_BLUE
        draw.ellipse([cx + 36, cy + 255, cx + 52, cy + 271], fill=dot_color)
        t_txt = "Verified Git SHA • NIMO Engine" if i < 4 else "Active Pod ID: #842 • 48h SLA Active"
        draw.text((cx + 66, cy + 252), t_txt, font=f_badge, fill=C_TEXT_MUTED)

    res = im.resize((2400, 250), Image.Resampling.LANCZOS)
    base_path = 'images/6ac643fb2f4d609f4b51ea53_99dc55351e0f72a760697d9e088ba781_Find Image.avif'
    save_responsive_variants(res, base_path, [500, 800, 1080, 1600])

# ==========================================
# 2. CASE 01: Top-tier engineers, built for fast delivery (Dossier & Competency Map)
# ==========================================
def generate_case_01():
    # Desktop: 1386 x 1010 -> render at 2772 x 2020
    W, H = 2772, 2020
    im = Image.new('RGBA', (W, H), (244, 249, 255, 255))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 46)
    f_sub = ImageFont.truetype(FONT_BOLD, 34)
    f_card_t = ImageFont.truetype(FONT_BOLD, 30)
    f_body = ImageFont.truetype(FONT_REG, 26)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 26)
    f_badge = ImageFont.truetype(FONT_BOLD, 22)
    f_mono = ImageFont.truetype(FONT_MONO, 22)

    # Outer Container Card
    draw.rounded_rectangle([60, 60, W - 60, H - 60], radius=40, fill=C_WHITE, outline=C_BORDER, width=4)

    # Top Navigation / Dossier Header
    draw.text((120, 110), "SPOTALENTS INTELLIGENCE // CANDIDATE EVIDENCE DOSSIER", font=f_mono, fill=C_TEXT_MUTED)
    draw_badge(draw, W - 780, 95, "96.8% OVERALL MATCH", f_badge, C_BLUE_LIGHT, C_BLUE, radius=12, pad_x=20, pad_y=12)
    draw_badge(draw, W - 410, 95, "VERIFIED SQUAD READY", f_badge, C_GREEN_LIGHT, C_GREEN, radius=12, pad_x=20, pad_y=12)
    draw.line([(120, 180), (W - 120, 180)], fill=C_BORDER, width=3)

    # Left Column: Candidate Profile (x: 120 to 1080)
    draw.rounded_rectangle([120, 220, 1080, 1080], radius=32, fill=C_CARD_ALT, outline=C_BORDER, width=3)
    
    # Avatar Circle
    draw.ellipse([180, 280, 320, 420], fill=C_BLUE)
    draw.text((215, 315), "AM", font=f_head, fill=C_WHITE)

    draw.text((360, 290), "Alexandre Mercier", font=f_head, fill=C_TEXT_BLACK)
    draw.text((360, 355), "Staff Distributed Systems Engineer", font=f_sub, fill=C_TEXT_MUTED)

    # Metadata pills
    pill_y = 470
    draw_badge(draw, 180, pill_y, "Go (Golang)", f_badge, C_WHITE, C_TEXT_BLACK, radius=10, pad_x=16, pad_y=8)
    draw_badge(draw, 360, pill_y, "Kubernetes", f_badge, C_WHITE, C_TEXT_BLACK, radius=10, pad_x=16, pad_y=8)
    draw_badge(draw, 540, pill_y, "Distributed Systems", f_badge, C_WHITE, C_TEXT_BLACK, radius=10, pad_x=16, pad_y=8)
    draw_badge(draw, 810, pill_y, "Kafka", f_badge, C_WHITE, C_TEXT_BLACK, radius=10, pad_x=16, pad_y=8)

    draw.line([(180, 560), (1020, 560)], fill=C_BORDER, width=2)

    # Telemetry metrics grid
    metrics = [
        ("Production PRs Merged", "142 PRs", "Audited via GitHub SHA"),
        ("Code Hygiene Index", "98.4%", "Top 2% of Benchmark"),
        ("Median PR Turnaround", "2.1 Hours", "Review to Production"),
        ("Sev-1 Incidents", "0 (2 Yrs)", "High Resilience Record")
    ]
    for idx, (label, val, sub) in enumerate(metrics):
        mx = 180 + (idx % 2) * 440
        my = 600 + (idx // 2) * 220
        draw.text((mx, my), label, font=f_body, fill=C_TEXT_MUTED)
        draw.text((mx, my + 45), val, font=f_head, fill=C_BLUE)
        draw.text((mx, my + 115), sub, font=f_mono, fill=C_TEXT_BODY)

    # Right Column: Competency Map & Explainable Matching (x: 1140 to W - 120)
    # 1. Competency Map (Ist vs. Soll)
    draw.rounded_rectangle([1140, 220, W - 120, 1080], radius=32, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((1200, 280), "COMPETENCY GAP ANALYSIS // IST VS. SOLL (AIPLOYA MODEL)", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((1200, 330), "Role Requirements vs. Verified Evidence", font=f_head, fill=C_TEXT_BLACK)

    skills = [
        ("Distributed Consensus & Raft", 0.90, 0.98, "+8% Verified Surplus"),
        ("High-Throughput Go Microservices", 0.85, 0.96, "+11% Surplus (Top 2%)"),
        ("Cloud-Native Resilience & Envoy", 0.85, 0.92, "+7% Production Proof"),
        ("Architectural RFCs & System Design", 0.80, 0.94, "+14% Deep Judgment")
    ]

    for s_idx, (skill_name, soll, ist, delta) in enumerate(skills):
        sy = 430 + s_idx * 150
        draw.text((1200, sy), skill_name, font=f_card_t, fill=C_TEXT_BLACK)
        draw.text((W - 380, sy), delta, font=f_badge, fill=C_GREEN)
        
        # Track background
        draw_progress_bar(draw, 1200, sy + 50, 1300, 24, 1.0, C_CARD_ALT, C_CARD_ALT, radius=12)
        # Soll marker (Target)
        soll_w = int(1300 * soll)
        draw.rounded_rectangle([1200, sy + 50, 1200 + soll_w, sy + 74], radius=12, fill=(203, 213, 225, 255))
        # Ist bar (Verified)
        ist_w = int(1300 * ist)
        draw.rounded_rectangle([1200, sy + 50, 1200 + ist_w, sy + 74], radius=12, fill=C_BLUE)

        draw.text((1200, sy + 88), f"Target Requirement: {int(soll*100)}%   |   Verified Capability: {int(ist*100)}%", font=f_mono, fill=C_TEXT_MUTED)

    # Bottom Full-Width Card: Explainable Matching Reason (Begründung)
    draw.rounded_rectangle([120, 1140, W - 120, 1860], radius=32, fill=C_BLUE_LIGHT, outline=(186, 230, 253, 255), width=3)
    draw.text((180, 1200), "EXPLAINABLE MATCHING REASONING // TRANSPARENT RELEASE CHAIN", font=f_mono, fill=C_BLUE)
    draw.text((180, 1250), "Why Spotalents Intelligence Matched This Engineer", font=f_head, fill=C_TEXT_BLACK)
    
    reason_lines = [
        "• High-Scale Architecture: Merged PRs verify autonomous design of distributed streaming pipelines handling >250k req/sec with 99.99% uptime.",
        "• Git Telemetry Verification: 142 pull requests across production repositories confirm high code hygiene, zero circular dependencies, and 98% test coverage.",
        "• Peer Review Synergy: Average code review turnaround time is 2.1 hours, accelerating sprint velocity and cross-functional team coordination."
    ]
    for r_idx, r_line in enumerate(reason_lines):
        draw.text((180, 1340 + r_idx * 75), r_line, font=f_body_bold, fill=C_TEXT_BODY)

    # Action Buttons inside bottom card
    draw.rounded_rectangle([180, 1630, 680, 1750], radius=24, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((230, 1670), "View Cryptographic Git SHA Proof", font=f_card_t, fill=C_TEXT_BLACK)

    draw.rounded_rectangle([720, 1630, 1260, 1750], radius=24, fill=C_BLUE)
    draw.text((800, 1670), "Add Alexandre to Squad (48h SLA)", font=f_card_t, fill=C_WHITE)

    res_desktop = im.resize((1386, 1010), Image.Resampling.LANCZOS)
    base_path_desktop = 'images/6ab37f7000908fa37c5a26d5_Case Image.avif'
    save_responsive_variants(res_desktop, base_path_desktop, [500, 800, 1080])

    # Mobile Variant (962 x 700)
    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    base_path_mobile = 'images/6ac37306e1bdf8eccc624a33_Case Dashboard Image 01.avif'
    save_responsive_variants(res_mobile, base_path_mobile, [500, 800])

# ==========================================
# 3. CASE 02: Senior specialists and domain leads
# ==========================================
def generate_case_02():
    # Desktop: 1040 x 758 -> render at 2080 x 1516
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (244, 249, 255, 255))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_BOLD, 30)
    f_card_t = ImageFont.truetype(FONT_BOLD, 26)
    f_body = ImageFont.truetype(FONT_REG, 24)
    f_badge = ImageFont.truetype(FONT_BOLD, 20)
    f_mono = ImageFont.truetype(FONT_MONO, 20)

    draw.rounded_rectangle([50, 50, W - 50, H - 50], radius=36, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((100, 90), "DOMAIN LEAD CAPABILITY AUDIT // DEEP TECHNICAL JUDGMENT", font=f_mono, fill=C_TEXT_MUTED)
    draw_badge(draw, W - 580, 80, "98.2% ARCHITECTURE DEPTH", f_badge, C_BLUE_LIGHT, C_BLUE, radius=12, pad_x=18, pad_y=10)
    draw.line([(100, 150), (W - 100, 150)], fill=C_BORDER, width=2)

    # Lead Profile Banner
    draw.rounded_rectangle([100, 180, W - 100, 480], radius=24, fill=C_CARD_ALT, outline=C_BORDER, width=2)
    draw.ellipse([140, 220, 260, 340], fill=C_PURPLE)
    draw.text((170, 250), "ER", font=f_head, fill=C_WHITE)

    draw.text((300, 225), "Dr. Elena Rostova", font=f_head, fill=C_TEXT_BLACK)
    draw.text((300, 285), "Principal Platform Architect & Rust/Go Lead", font=f_sub, fill=C_TEXT_MUTED)

    draw_badge(draw, 300, 360, "Rust", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)
    draw_badge(draw, 420, 360, "Apache Kafka", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)
    draw_badge(draw, 640, 360, "ClickHouse", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)
    draw_badge(draw, 840, 360, "AWS EKS", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)
    draw_badge(draw, 1020, 360, "gRPC", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)

    # 3 Core Depth Pillars
    pillars = [
        ("SYSTEM DESIGN & RFCs", "6 Merged RFCs", "Multi-region distributed bus serving 12M DAU. Zero Sev-1 outages."),
        ("CODE REVIEW & MENTORSHIP", "480+ Deep Reviews", "96% positive velocity multiplier across 3 squads."),
        ("AUTONOMOUS EXECUTION", "180k msgs/sec", "Built zero-downtime streaming pipeline at p99 < 12ms.")
    ]
    card_w = 580
    for idx, (title, highlight, desc) in enumerate(pillars):
        px = 100 + idx * (card_w + 70)
        py = 520
        draw.rounded_rectangle([px, py, px + card_w, py + 520], radius=24, fill=C_WHITE, outline=C_BORDER, width=2)
        draw.text((px + 30, py + 40), title, font=f_mono, fill=C_BLUE)
        draw.text((px + 30, py + 95), highlight, font=f_head, fill=C_TEXT_BLACK)
        draw.line([(px + 30, py + 180), (px + card_w - 30, py + 180)], fill=C_BORDER, width=2)
        
        words = desc.split()
        line1 = " ".join(words[:5])
        line2 = " ".join(words[5:])
        draw.text((px + 30, py + 220), line1, font=f_body, fill=C_TEXT_BODY)
        draw.text((px + 30, py + 265), line2, font=f_body, fill=C_TEXT_BODY)
        
        draw_badge(draw, px + 30, py + 380, "AUDITED VIA GIT", f_badge, C_GREEN_LIGHT, C_GREEN, radius=8)

    # Bottom Explainable Note
    draw.rounded_rectangle([100, 1080, W - 100, 1420], radius=24, fill=C_BLUE_LIGHT, outline=C_BORDER, width=2)
    draw.text((140, 1120), "EXPLAINABLE MATCHING JUSTIFICATION // SPOTALENTS REASONING", font=f_mono, fill=C_BLUE)
    draw.text((140, 1175), "Matched for domain-critical platform overhaul. RFC history validates capacity to define architectural standards, decompose legacy monoliths, and mentor senior engineers without management overhead.", font=f_body, fill=C_TEXT_BLACK)
    
    draw.rounded_rectangle([140, 1290, 680, 1380], radius=16, fill=C_BLUE)
    draw.text((210, 1320), "Confirm Elena for Platform Lead", font=f_card_t, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    base_path_desktop = 'images/6ac0f44b97ebd2aa1d167d71_Cases Image 02.avif'
    save_responsive_variants(res_desktop, base_path_desktop, [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    base_path_mobile = 'images/6ac3730617c04dbca55b7771_Case Dashboard Image 02.avif'
    save_responsive_variants(res_mobile, base_path_mobile, [500, 800])

# ==========================================
# 4. CASE 03: Staff architects and fractional CTOs
# ==========================================
def generate_case_03():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (244, 249, 255, 255))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_BOLD, 30)
    f_card_t = ImageFont.truetype(FONT_BOLD, 26)
    f_body = ImageFont.truetype(FONT_REG, 24)
    f_badge = ImageFont.truetype(FONT_BOLD, 20)
    f_mono = ImageFont.truetype(FONT_MONO, 20)

    draw.rounded_rectangle([50, 50, W - 50, H - 50], radius=36, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((100, 90), "EXECUTIVE TECHNICAL LEADERSHIP // FRACTIONAL CTO SUITE", font=f_mono, fill=C_TEXT_MUTED)
    draw_badge(draw, W - 580, 80, "99.1% GOVERNANCE INDEX", f_badge, C_BLUE_LIGHT, C_BLUE, radius=12, pad_x=18, pad_y=10)
    draw.line([(100, 150), (W - 100, 150)], fill=C_BORDER, width=2)

    # Executive Profile
    draw.rounded_rectangle([100, 180, W - 100, 480], radius=24, fill=C_CARD_ALT, outline=C_BORDER, width=2)
    draw.ellipse([140, 220, 260, 340], fill=(15, 23, 42, 255))
    draw.text((170, 250), "DS", font=f_head, fill=C_WHITE)

    draw.text((300, 225), "David Sterling", font=f_head, fill=C_TEXT_BLACK)
    draw.text((300, 285), "Fractional CTO & Staff Architect (Former Series B VP Eng)", font=f_sub, fill=C_TEXT_MUTED)

    draw_badge(draw, 300, 360, "Fractional 15-20h/wk", f_badge, C_GREEN_LIGHT, C_GREEN, radius=8, pad_x=14, pad_y=6)
    draw_badge(draw, 620, 360, "Technical Debt Triage", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)
    draw_badge(draw, 960, 360, "Org Design", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)
    draw_badge(draw, 1160, 360, "Board Advisory", f_badge, C_WHITE, C_TEXT_BLACK, radius=8, pad_x=14, pad_y=6)

    # Impact Cards
    impacts = [
        ("TECH DEBT TRIAGE", "-45% Debt", "Eliminated high-risk architectural debt across 4 services in 90 days."),
        ("DELIVERY VELOCITY", "+34% Speed", "Synchronized sprint delivery rhythm across 4 independent squads."),
        ("GOVERNANCE SLA", "100% Pass", "SOC2 compliance and zero architectural security regressions.")
    ]
    card_w = 580
    for idx, (title, highlight, desc) in enumerate(impacts):
        px = 100 + idx * (card_w + 70)
        py = 520
        draw.rounded_rectangle([px, py, px + card_w, py + 520], radius=24, fill=C_WHITE, outline=C_BORDER, width=2)
        draw.text((px + 30, py + 40), title, font=f_mono, fill=C_BLUE)
        draw.text((px + 30, py + 95), highlight, font=f_head, fill=C_TEXT_BLACK)
        draw.line([(px + 30, py + 180), (px + card_w - 30, py + 180)], fill=C_BORDER, width=2)
        
        words = desc.split()
        draw.text((px + 30, py + 220), " ".join(words[:5]), font=f_body, fill=C_TEXT_BODY)
        draw.text((px + 30, py + 265), " ".join(words[5:]), font=f_body, fill=C_TEXT_BODY)
        draw_badge(draw, px + 30, py + 380, "AUDITED IMPACT", f_badge, C_BLUE_LIGHT, C_BLUE, radius=8)

    # Multi-Squad Governance Status
    draw.rounded_rectangle([100, 1080, W - 100, 1420], radius=24, fill=C_CARD_ALT, outline=C_BORDER, width=2)
    draw.text((140, 1120), "ACTIVE SQUAD GOVERNANCE // CROSS-TEAM SYNCHRONIZATION", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((140, 1170), "Squad 1 (Platform): Synchronized  |  Squad 2 (Core): Synchronized  |  Squad 3 (Data): Synchronized", font=f_sub, fill=C_TEXT_BLACK)
    
    draw.rounded_rectangle([140, 1270, 720, 1370], radius=16, fill=C_BLUE)
    draw.text((200, 1300), "Book Strategic Alignment Session", font=f_card_t, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    base_path_desktop = 'images/6ac0f44b4b73a87c95802a54_Cases Image 03.avif'
    save_responsive_variants(res_desktop, base_path_desktop, [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    base_path_mobile = 'images/6ac37306461ca2eb8f3838fd_Case Dashboard Image 03.avif'
    save_responsive_variants(res_mobile, base_path_mobile, [500, 800])

# ==========================================
# 5. CASE 04: Turn-key squads calibrated for scale
# ==========================================
def generate_case_04():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (244, 249, 255, 255))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_BOLD, 28)
    f_card_t = ImageFont.truetype(FONT_BOLD, 24)
    f_body = ImageFont.truetype(FONT_REG, 22)
    f_badge = ImageFont.truetype(FONT_BOLD, 20)
    f_mono = ImageFont.truetype(FONT_MONO, 20)

    draw.rounded_rectangle([50, 50, W - 50, H - 50], radius=36, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((100, 90), "AUTONOMOUS SQUAD CALIBRATION // POD #04 PLATFORM SCALING", font=f_mono, fill=C_TEXT_MUTED)
    draw_badge(draw, W - 580, 80, "96.4% TEAM CHEMISTRY", f_badge, C_GREEN_LIGHT, C_GREEN, radius=12, pad_x=18, pad_y=10)
    draw.line([(100, 150), (W - 100, 150)], fill=C_BORDER, width=2)

    # 4 Seats Grid (2x2)
    seats = [
        ("SEAT 1 // TECH LEAD", "Marcus Vance", "Staff Backend Lead • Go / K8s", "98% Fit Score", C_BLUE),
        ("SEAT 2 // SENIOR FULLSTACK", "Sofia Lin", "Senior Fullstack • React / TypeScript", "95% Fit Score", C_PURPLE),
        ("SEAT 3 // SENIOR CLOUD INFRA", "Tariq Nabil", "Senior DevOps • Terraform / AWS", "97% Fit Score", C_GREEN),
        ("SEAT 4 // QA AUTOMATION", "Maya Kapoor", "Staff QA • Playwright / CI Test Ops", "94% Fit Score", (234, 88, 12, 255))
    ]

    card_w = 900
    card_h = 360
    for idx, (seat_lbl, name, role, fit, col) in enumerate(seats):
        row = idx // 2
        c_idx = idx % 2
        sx = 100 + c_idx * (card_w + 80)
        sy = 190 + row * (card_h + 40)
        draw.rounded_rectangle([sx, sy, sx + card_w, sy + card_h], radius=24, fill=C_CARD_ALT, outline=C_BORDER, width=2)
        
        draw.text((sx + 30, sy + 30), seat_lbl, font=f_mono, fill=C_TEXT_MUTED)
        draw_badge(draw, sx + card_w - 240, sy + 25, fit, f_badge, C_WHITE, col, radius=8)

        draw.text((sx + 30, sy + 90), name, font=f_head, fill=C_TEXT_BLACK)
        draw.text((sx + 30, sy + 150), role, font=f_sub, fill=C_TEXT_MUTED)

        draw.line([(sx + 30, sy + 220), (sx + card_w - 30, sy + 220)], fill=C_BORDER, width=2)
        draw.text((sx + 30, sy + 250), "• Day-One Sprint Integration  |  Pre-Tested Chemistry", font=f_body, fill=C_TEXT_BODY)
        draw.text((sx + 30, sy + 295), "• 40 Hours/wk Dedicated Allocation", font=f_body, fill=C_TEXT_BODY)

    # Bottom Pod Summary Banner
    draw.rounded_rectangle([100, 1020, W - 100, 1420], radius=24, fill=C_BLUE_LIGHT, outline=C_BORDER, width=2)
    draw.text((140, 1060), "COMBINED SQUAD CAPACITY // 160 HOURS/WEEK // 48-HOUR SPRINT READY", font=f_mono, fill=C_BLUE)
    draw.text((140, 1115), "Pod delivery multiplier evaluated at +38% compared to uncoordinated individual hires.", font=f_sub, fill=C_TEXT_BLACK)
    draw.text((140, 1175), "Calibrated for zero-ramp deployment: code environments, CI pipelines, and PR standards pre-aligned.", font=f_body, fill=C_TEXT_BODY)

    draw.rounded_rectangle([140, 1260, 720, 1360], radius=16, fill=C_BLUE)
    draw.text((220, 1290), "Deploy Pod #04 to Production", font=f_card_t, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    base_path_desktop = 'images/6ac0f44a4b73a87c95802a34_Cases Image 04.avif'
    save_responsive_variants(res_desktop, base_path_desktop, [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    base_path_mobile = 'images/6ac3730693b442b8285082bc_Case Dashboard Image 04.avif'
    save_responsive_variants(res_mobile, base_path_mobile, [500, 800])

# ==========================================
# 6. CASE 05: Proof over resume claims (Evidence Dossier)
# ==========================================
def generate_case_05():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (244, 249, 255, 255))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_BOLD, 28)
    f_card_t = ImageFont.truetype(FONT_BOLD, 26)
    f_body = ImageFont.truetype(FONT_REG, 24)
    f_badge = ImageFont.truetype(FONT_BOLD, 20)
    f_mono = ImageFont.truetype(FONT_MONO, 20)

    draw.rounded_rectangle([50, 50, W - 50, H - 50], radius=36, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((100, 90), "CODEBASE TELEMETRY // CV CLAIM VS. GIT REALITY AUDIT", font=f_mono, fill=C_TEXT_MUTED)
    draw_badge(draw, W - 620, 80, "CRYPTOGRAPHICALLY AUDITED", f_badge, C_GREEN_LIGHT, C_GREEN, radius=12, pad_x=18, pad_y=10)
    draw.line([(100, 150), (W - 100, 150)], fill=C_BORDER, width=2)

    rows = [
        ("CV CLAIM: Expert in Go & Microservices", "84,200 LOC in Production Go Services • 142 Merged PRs verified via Git SHA.", "VERIFIED 98.4%", C_GREEN),
        ("CV CLAIM: High Velocity & Agile Delivery", "3.6 Merged PRs / week • 94.8% first-pass CI/CD test pass rate • 2.2h review cycle.", "VERIFIED 96.2%", C_GREEN),
        ("CV CLAIM: Database Performance Tuning", "PostgreSQL query optimization: p99 latency cut from 320ms to 8ms on 50M rows.", "VERIFIED 99.0%", C_GREEN)
    ]

    card_h = 240
    for idx, (claim, proof, stat, col) in enumerate(rows):
        ry = 190 + idx * (card_h + 30)
        draw.rounded_rectangle([100, ry, W - 100, ry + card_h], radius=24, fill=C_CARD_ALT, outline=C_BORDER, width=2)
        
        # Left side: Claim
        draw.text((140, ry + 35), claim, font=f_card_t, fill=(225, 29, 72, 255))
        draw_badge(draw, W - 380, ry + 30, stat, f_badge, C_WHITE, col, radius=8)
        
        draw.line([(140, ry + 95), (W - 140, ry + 95)], fill=C_BORDER, width=2)
        
        # Right/Bottom side: Proof
        draw.text((140, ry + 120), "TELEMETRY EVIDENCE PROOF (NIMO ENGINE):", font=f_mono, fill=C_BLUE)
        draw.text((140, ry + 165), proof, font=f_body, fill=C_TEXT_BLACK)

    # Bottom Verification Summary
    draw.rounded_rectangle([100, 1040, W - 100, 1420], radius=24, fill=C_BLUE_LIGHT, outline=C_BORDER, width=2)
    draw.text((140, 1080), "EVIDENCE CONFIDENCE SCORE: 99.4% // ZERO CV HALLUCINATIONS DETECTED", font=f_mono, fill=C_BLUE)
    draw.text((140, 1135), "Spotalents extracts actual git telemetry, commit authorship, and code complexity scores directly from production repos.", font=f_sub, fill=C_TEXT_BLACK)
    draw.text((140, 1200), "Every skill level is benchmarked against real engineers, eliminating resume inflation and self-reporting bias.", font=f_body, fill=C_TEXT_BODY)

    draw.rounded_rectangle([140, 1280, 720, 1380], radius=16, fill=C_BLUE)
    draw.text((220, 1310), "Download Cryptographic Dossier", font=f_card_t, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    base_path_desktop = 'images/6ac0f44bd95a8b30192bce9f_Cases Image 05.avif'
    save_responsive_variants(res_desktop, base_path_desktop, [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    base_path_mobile = 'images/6ac373063b5857609808d81d_Case Dashboard Image 05.avif'
    save_responsive_variants(res_mobile, base_path_mobile, [500, 800])

# ==========================================
# 7. CASE 06: Smarter matches after each sprint
# ==========================================
def generate_case_06():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (244, 249, 255, 255))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_BOLD, 28)
    f_card_t = ImageFont.truetype(FONT_BOLD, 26)
    f_body = ImageFont.truetype(FONT_REG, 24)
    f_badge = ImageFont.truetype(FONT_BOLD, 20)
    f_mono = ImageFont.truetype(FONT_MONO, 20)

    draw.rounded_rectangle([50, 50, W - 50, H - 50], radius=36, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((100, 90), "CONTINUOUS SPRINT TELEMETRY // ADAPTIVE MATCH TUNING", font=f_mono, fill=C_TEXT_MUTED)
    draw_badge(draw, W - 580, 80, "ADAPTIVE LEARNING ACTIVE", f_badge, C_BLUE_LIGHT, C_BLUE, radius=12, pad_x=18, pad_y=10)
    draw.line([(100, 150), (W - 100, 150)], fill=C_BORDER, width=2)

    # Sprint Metrics (3 Cards)
    sprint_metrics = [
        ("MILESTONE DELIVERY SLA", "99.2%", "12 Sprints Completed on Schedule. Top 5% Industry Velocity."),
        ("CYCLE TIME VELOCITY", "1.8 Hours", "PR Review to Merge latency. 4x faster than industry median."),
        ("POD HEALTH & SATISFACTION", "98.4%", "Net positive collaboration score from tech leadership.")
    ]
    card_w = 580
    for idx, (title, highlight, desc) in enumerate(sprint_metrics):
        px = 100 + idx * (card_w + 70)
        py = 190
        draw.rounded_rectangle([px, py, px + card_w, py + 480], radius=24, fill=C_CARD_ALT, outline=C_BORDER, width=2)
        draw.text((px + 30, py + 40), title, font=f_mono, fill=C_BLUE)
        draw.text((px + 30, py + 95), highlight, font=f_head, fill=C_TEXT_BLACK)
        draw.line([(px + 30, py + 180), (px + card_w - 30, py + 180)], fill=C_BORDER, width=2)
        
        words = desc.split()
        draw.text((px + 30, py + 220), " ".join(words[:5]), font=f_body, fill=C_TEXT_BODY)
        draw.text((px + 30, py + 265), " ".join(words[5:]), font=f_body, fill=C_TEXT_BODY)
        draw_badge(draw, px + 30, py + 360, "SPRINT AUDITED", f_badge, C_GREEN_LIGHT, C_GREEN, radius=8)

    # Adaptive Learning Engine Box
    draw.rounded_rectangle([100, 720, W - 100, 1420], radius=24, fill=C_BLUE_LIGHT, outline=C_BORDER, width=2)
    draw.text((140, 760), "ADAPTIVE MATCHING FEEDBACK LOOP // CONTINUOUS CALIBRATION", font=f_mono, fill=C_BLUE)
    draw.text((140, 815), "How Spotalents Intelligence Learns From Every Deployed Sprint", font=f_head, fill=C_TEXT_BLACK)

    learnings = [
        "• Sprint #12 Delivery Telemetry parsed: Codebase velocity and PR rhythm incorporated into organization talent model.",
        "• Matching precision recalibrated: Model adjusted for high-throughput concurrency, yielding +3.1% precision on future hires.",
        "• Autonomous pod rebalancing: Engineering manager notified of capacity headroom 2 sprints ahead of product roadmap deadlines."
    ]
    for l_idx, l_line in enumerate(learnings):
        draw.text((140, 910 + l_idx * 90), l_line, font=f_body, fill=C_TEXT_BODY)

    draw.rounded_rectangle([140, 1260, 720, 1360], radius=16, fill=C_BLUE)
    draw.text((220, 1290), "View Sprint Telemetry Report", font=f_card_t, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    base_path_desktop = 'images/6ac0f44bbebcfc65055a419a_Cases Image 06.avif'
    save_responsive_variants(res_desktop, base_path_desktop, [500, 800])

    res_mobile = im.resize((962, 752), Image.Resampling.LANCZOS)
    base_path_mobile = 'images/6ac37306e1bdf8eccc624a13_Case Dashboard Image 06.avif'
    save_responsive_variants(res_mobile, base_path_mobile, [500, 800])

# ==========================================
# 8. BACK DASHBOARD IMAGE (2772 x 2128)
# ==========================================
def generate_back_dashboard_image():
    W, H = 2772, 2128
    im = Image.new('RGBA', (W, H), (244, 249, 255, 255))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 46)
    f_sub = ImageFont.truetype(FONT_BOLD, 32)
    f_card_t = ImageFont.truetype(FONT_BOLD, 28)
    f_body = ImageFont.truetype(FONT_REG, 26)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 26)
    f_badge = ImageFont.truetype(FONT_BOLD, 22)
    f_mono = ImageFont.truetype(FONT_MONO, 22)

    # Outer Container Card
    draw.rounded_rectangle([60, 60, W - 60, H - 60], radius=44, fill=C_WHITE, outline=C_BORDER, width=4)

    # Top Control Bar
    draw.text((120, 120), "SPOTALENTS INTELLIGENCE // WORKFORCE VELOCITY CONTROL CENTER", font=f_mono, fill=C_TEXT_MUTED)
    draw_badge(draw, W - 920, 105, "237 ACTIVE CONTRACTS", f_badge, C_BLUE_LIGHT, C_BLUE, radius=12, pad_x=20, pad_y=12)
    draw_badge(draw, W - 480, 105, "48h SPRINT SLA: 99.4%", f_badge, C_GREEN_LIGHT, C_GREEN, radius=12, pad_x=20, pad_y=12)
    draw.line([(120, 190), (W - 120, 190)], fill=C_BORDER, width=3)

    # Split Comparison: Left (Traditional 60+ Days) vs Right (Spotalents 48 Hours)
    col_w = (W - 320) // 2

    # LEFT COLUMN: Traditional Hiring Drag
    lx = 120
    ly = 240
    draw.rounded_rectangle([lx, ly, lx + col_w, ly + 1150], radius=32, fill=(255, 245, 245, 255), outline=(254, 202, 202, 255), width=3)
    draw.text((lx + 40, ly + 40), "LEGACY HIRING FRICTION // 60+ DAYS LOST", font=f_mono, fill=C_RED)
    draw.text((lx + 40, ly + 95), "Traditional Recruitment Drag", font=f_head, fill=C_TEXT_BLACK)

    left_points = [
        ("• 240+ Unfiltered CV PDFs", "Inflated claims, keyword stuffing, zero verified code."),
        ("• 6 Weeks of Screening Calls", "Recruiter ping-pong, repetitive non-technical filters."),
        ("• Black-Box Gut Decision", "Subjective bias, no explainable matching or reasoning."),
        ("• 40% Post-Hire Regret", "Engineers fail to ramp or clash with team culture."),
        ("• High Agency Fees", "$45k+ placement fees with no delivery guarantees.")
    ]
    for idx, (head, desc) in enumerate(left_points):
        py = ly + 210 + idx * 175
        draw.text((lx + 40, py), head, font=f_card_t, fill=(185, 28, 28, 255))
        draw.text((lx + 40, py + 45), desc, font=f_body, fill=C_TEXT_BODY)
        if idx < 4:
            draw.line([(lx + 40, py + 110), (lx + col_w - 40, py + 110)], fill=(254, 226, 226, 255), width=2)

    # RIGHT COLUMN: Spotalents 48h Deployment
    rx = lx + col_w + 80
    ry = 240
    draw.rounded_rectangle([rx, ry, rx + col_w, ry + 1150], radius=32, fill=C_BLUE_LIGHT, outline=(186, 230, 253, 255), width=3)
    draw.text((rx + 40, ry + 40), "SPOTALENTS INTELLIGENCE // 48-HOUR ACTIVATION", font=f_mono, fill=C_BLUE)
    draw.text((rx + 40, ry + 95), "Verified Pod Deployment", font=f_head, fill=C_TEXT_BLACK)

    right_points = [
        ("• 1-Click Role Spec Ingestion", "Stack, delivery pace, and architectural depth ingested."),
        ("• NIMO Multi-Signal Matching", "Candidate codebase telemetry, PR velocity, team chemistry."),
        ("• Explainable Match Dossier", "Clear transparent reasoning (Aiploya model) + Git SHA proof."),
        ("• Pre-Tested Squad Chemistry", "4-seat pod pre-calibrated for zero-ramp Day-One delivery."),
        ("• Turn-Key 48h SLA Activation", "Transparent hourly terms, zero lock-in, monitored sprints.")
    ]
    for idx, (head, desc) in enumerate(right_points):
        py = ry + 210 + idx * 175
        draw.text((rx + 40, py), head, font=f_card_t, fill=C_BLUE)
        draw.text((rx + 40, py + 45), desc, font=f_body, fill=C_TEXT_BLACK)
        if idx < 4:
            draw.line([(rx + 40, py + 110), (rx + col_w - 40, py + 110)], fill=(224, 242, 254, 255), width=2)

    # Bottom Active Squad Control Panel
    by = 1450
    draw.rounded_rectangle([120, by, W - 120, H - 120], radius=32, fill=C_WHITE, outline=C_BORDER, width=3)
    draw.text((160, by + 40), "LIVE WORKFORCE ACTIVATION // PLATFORM SCALING POD #04", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((160, by + 90), "4 Calibrated Engineers Ready for Production Code", font=f_head, fill=C_TEXT_BLACK)

    squad_pills = [
        ("Tech Lead", "Alexandre M. (Go/K8s)", "98% Fit"),
        ("Senior Fullstack", "Sofia L. (React/TS)", "95% Fit"),
        ("Senior Cloud", "Tariq N. (Terraform)", "97% Fit"),
        ("QA Lead", "Maya K. (Playwright)", "94% Fit")
    ]
    sp_w = (W - 400) // 4
    for idx, (role, name, fit) in enumerate(squad_pills):
        px = 160 + idx * (sp_w + 30)
        draw.rounded_rectangle([px, by + 180, px + sp_w, by + 340], radius=20, fill=C_CARD_ALT, outline=C_BORDER, width=2)
        draw.text((px + 20, by + 210), role, font=f_mono, fill=C_BLUE)
        draw.text((px + 20, by + 250), name, font=f_body_bold, fill=C_TEXT_BLACK)
        draw_badge(draw, px + 20, by + 290, fit, f_badge, C_GREEN_LIGHT, C_GREEN, radius=6)

    # Primary Action
    draw.rounded_rectangle([W - 680, by + 380, W - 160, by + 480], radius=20, fill=C_BLUE)
    draw.text((W - 620, by + 415), "Deploy Pod #04 (48h SLA)", font=f_card_t, fill=C_WHITE)

    res = im.resize((2772, 2128), Image.Resampling.LANCZOS)
    base_path = 'images/6ab38801eb36043b8f250950_47ad6e145cde10b8ef679904c5363618_Back Dashboard Image.avif'
    save_responsive_variants(res, base_path, [500, 800, 1080, 1600, 2000])

if __name__ == '__main__':
    print("Generating Find Image...")
    generate_find_image()
    print("Generating Case 01...")
    generate_case_01()
    print("Generating Case 02...")
    generate_case_02()
    print("Generating Case 03...")
    generate_case_03()
    print("Generating Case 04...")
    generate_case_04()
    print("Generating Case 05...")
    generate_case_05()
    print("Generating Case 06...")
    generate_case_06()
    print("Generating Back Dashboard Image...")
    generate_back_dashboard_image()
    print("ALL LANDING ASSETS GENERATED SUCCESSFULLY!")

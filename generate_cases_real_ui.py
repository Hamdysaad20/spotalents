import os
import math
from PIL import Image, ImageDraw, ImageFont

# Fonts
FONT_BOLD = '/tmp/InstrumentSans-Bold.ttf'
FONT_REG = '/tmp/InstrumentSans.ttf'
FONT_MONO = '/tmp/SpaceMono.ttf'

# Colors
C_WINDOW_BG = (248, 250, 252, 255)      # Slate 50 window chrome
C_WHITE = (255, 255, 255, 255)
C_CARD_BG = (255, 255, 255, 255)
C_CARD_ALT = (248, 250, 252, 255)
C_BORDER = (226, 232, 240, 255)         # Slate 200
C_BORDER_LIGHT = (241, 245, 249, 255)
C_BLUE = (1, 59, 255, 255)              # Spotalents Royal Blue #013BFF
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
C_DOT_RED = (255, 95, 86, 255)
C_DOT_YELLOW = (255, 189, 46, 255)
C_DOT_GREEN = (39, 201, 63, 255)

def save_responsive_variants(base_img, base_path, widths):
    os.makedirs(os.path.dirname(base_path), exist_ok=True)
    base_img.save(base_path, 'AVIF', quality=95)
    png_path = base_path.replace('.avif', '.png')
    base_img.save(png_path, 'PNG')
    print(f"Saved: {base_path}")

    orig_w, orig_h = base_img.size
    for w in widths:
        if w < orig_w:
            h = int(orig_h * (w / orig_w))
            res_img = base_img.resize((w, h), Image.Resampling.LANCZOS)
            var_path = base_path.replace('.avif', f'-p-{w}.avif')
            res_img.save(var_path, 'AVIF', quality=90)
            res_img.save(var_path.replace('.avif', '.png'), 'PNG')

def draw_window_frame(draw, W, H, url_text, f_mono):
    # Window Chrome background
    draw.rounded_rectangle([0, 0, W, H], radius=36, fill=C_WINDOW_BG, outline=C_BORDER, width=3)
    
    # Top window title bar
    bar_h = 100
    draw.rounded_rectangle([0, 0, W, bar_h], radius=36, fill=(241, 245, 249, 255))
    draw.rectangle([0, bar_h - 30, W, bar_h], fill=(241, 245, 249, 255))
    draw.line([(0, bar_h), (W, bar_h)], fill=C_BORDER, width=2)

    # 3 Window dots
    draw.ellipse([40, 38, 64, 62], fill=C_DOT_RED)
    draw.ellipse([78, 38, 102, 62], fill=C_DOT_YELLOW)
    draw.ellipse([116, 38, 140, 62], fill=C_DOT_GREEN)

    # Browser URL Pill
    url_w = 900
    url_x = (W - url_w) // 2
    url_y = 22
    draw.rounded_rectangle([url_x, url_y, url_x + url_w, url_y + 56], radius=28, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((url_x + 30, url_y + 16), url_text, font=f_mono, fill=C_TEXT_MUTED)

    # Environment Badge (Top right)
    env_text = "NIMO ENGINE v2.4 // PROD"
    draw.rounded_rectangle([W - 380, 24, W - 40, 78], radius=16, fill=C_GREEN_LIGHT, outline=(167, 243, 208, 255), width=2)
    draw.text((W - 355, 38), env_text, font=f_mono, fill=C_GREEN)

def draw_sidebar(draw, start_y, end_y, active_item_idx, f_bold, f_reg, f_mono):
    side_w = 460
    draw.rectangle([0, start_y, side_w, end_y], fill=(248, 250, 252, 255))
    draw.line([(side_w, start_y), (side_w, end_y)], fill=C_BORDER, width=2)

    # Logo
    draw.rounded_rectangle([40, start_y + 40, 100, start_y + 100], radius=16, fill=C_BLUE)
    draw.text((54, start_y + 48), "SP", font=f_bold, fill=C_WHITE)
    draw.text((120, start_y + 46), "Spotalents", font=f_bold, fill=C_TEXT_BLACK)
    draw.text((120, start_y + 82), "Intelligence SaaS", font=f_mono, fill=C_TEXT_MUTED)

    draw.line([(40, start_y + 130), (side_w - 40, start_y + 130)], fill=C_BORDER, width=2)

    # Nav items
    navs = [
        "Dashboard Overview",
        "Explainable Matching",
        "Competency Mapping",
        "Code Telemetry",
        "Squad Assembly",
        "Sprint Intelligence"
    ]
    for idx, nav in enumerate(navs):
        ny = start_y + 160 + idx * 75
        is_active = (idx == active_item_idx)
        if is_active:
            draw.rounded_rectangle([30, ny, side_w - 30, ny + 60], radius=14, fill=C_BLUE_LIGHT)
            draw.text((55, ny + 16), nav, font=f_bold, fill=C_BLUE)
            draw.rounded_rectangle([30, ny + 12, 36, ny + 48], radius=3, fill=C_BLUE)
        else:
            draw.text((55, ny + 16), nav, font=f_reg, fill=C_TEXT_BODY)

    # Workspace status at bottom
    wy = end_y - 120
    draw.rounded_rectangle([30, wy, side_w - 30, wy + 90], radius=16, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.ellipse([50, wy + 32, 74, wy + 56], fill=C_GREEN)
    draw.text((88, wy + 20), "Fintech Core Pod #04", font=f_bold, fill=C_TEXT_BLACK)
    draw.text((88, wy + 52), "Active 48h Sprint SLA", font=f_mono, fill=C_TEXT_MUTED)

def draw_badge(draw, x, y, text, font, bg_color, text_color, radius=10, pad_x=14, pad_y=6):
    bbox = font.getbbox(text)
    bw = bbox[2] - bbox[0] + pad_x * 2
    bh = bbox[3] - bbox[1] + pad_y * 2
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=radius, fill=bg_color)
    draw.text((x + pad_x, y + pad_y - 1), text, font=font, fill=text_color)
    return bw, bh

# ==========================================
# 1. CASE 01: Top-tier engineers, built for fast delivery (Match Dossier Snapshot)
# ==========================================
def render_case_01():
    W, H = 2772, 2020
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 38)
    f_title = ImageFont.truetype(FONT_BOLD, 28)
    f_sub = ImageFont.truetype(FONT_BOLD, 24)
    f_body = ImageFont.truetype(FONT_REG, 22)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 22)
    f_badge = ImageFont.truetype(FONT_BOLD, 18)
    f_mono = ImageFont.truetype(FONT_MONO, 18)
    f_mono_large = ImageFont.truetype(FONT_MONO, 22)

    draw_window_frame(draw, W, H, "🔒 app.spotalents.com/intelligence/dossier/alexandre-mercier", f_mono_large)
    draw_sidebar(draw, 100, H, 1, f_title, f_body, f_mono)

    content_x = 490
    content_w = W - content_x - 30

    # Top Content Header Bar
    draw.rounded_rectangle([content_x, 120, W - 30, 220], radius=20, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((content_x + 40, 145), "CANDIDATE INTELLIGENCE DOSSIER // MATCH #0842", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((content_x + 40, 172), "Autonomous Capability & Code Telemetry Audit", font=f_title, fill=C_TEXT_BLACK)
    
    draw_badge(draw, W - 620, 145, "96.8% OVERALL MATCH", f_badge, C_BLUE_LIGHT, C_BLUE, radius=12, pad_x=18, pad_y=10)
    draw_badge(draw, W - 320, 145, "AVAILABLE IN 48H", f_badge, C_GREEN_LIGHT, C_GREEN, radius=12, pad_x=18, pad_y=10)

    # Candidate Profile Hero (Left block)
    card_y = 250
    draw.rounded_rectangle([content_x, card_y, content_x + 900, card_y + 820], radius=24, fill=C_WHITE, outline=C_BORDER, width=2)
    
    # Avatar Circle
    draw.ellipse([content_x + 40, card_y + 40, content_x + 160, card_y + 160], fill=C_BLUE)
    draw.text((content_x + 75, card_y + 70), "AM", font=f_head, fill=C_WHITE)

    draw.text((content_x + 190, card_y + 50), "Alexandre Mercier", font=f_head, fill=C_TEXT_BLACK)
    draw.text((content_x + 190, card_y + 105), "Staff Distributed Systems Engineer", font=f_sub, fill=C_TEXT_MUTED)
    draw.text((content_x + 190, card_y + 140), "Staff Level (L6) • €115 / Hour • Verified Contractor", font=f_mono, fill=C_BLUE)

    draw.line([(content_x + 40, card_y + 190), (content_x + 860, card_y + 190)], fill=C_BORDER, width=2)

    # Tech Stack Pills
    pills = ["Go (Golang)", "Kubernetes", "Distributed Systems", "Apache Kafka", "Envoy Proxy", "PostgreSQL"]
    px = content_x + 40
    py = card_y + 215
    for p in pills:
        bw, bh = draw_badge(draw, px, py, p, f_badge, (241, 245, 249, 255), C_TEXT_BLACK, radius=8, pad_x=14, pad_y=8)
        px += bw + 12
        if px > content_x + 800:
            px = content_x + 40
            py += bh + 12

    draw.line([(content_x + 40, card_y + 360), (content_x + 860, card_y + 360)], fill=C_BORDER, width=2)

    # Verified Metrics Grid
    v_metrics = [
        ("Merged PRs Audited", "142 PRs", "Verified via Git SHA"),
        ("Code Hygiene Index", "98.4%", "Top 2% Benchmark"),
        ("Review Turnaround", "2.1 Hours", "Median PR Velocity"),
        ("Sev-1 Incidents", "0 (24 Mo)", "Production Resilience")
    ]
    for m_i, (lbl, val, sub) in enumerate(v_metrics):
        mx = content_x + 50 + (m_i % 2) * 410
        my = card_y + 400 + (m_i // 2) * 190
        draw.text((mx, my), lbl, font=f_body, fill=C_TEXT_MUTED)
        draw.text((mx, my + 35), val, font=f_head, fill=C_BLUE)
        draw.text((mx, my + 90), sub, font=f_mono, fill=C_TEXT_BODY)

    # Right Block: Aiploya Ist vs. Soll Competency Matrix
    right_x = content_x + 930
    draw.rounded_rectangle([right_x, card_y, W - 30, card_y + 820], radius=24, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((right_x + 40, card_y + 40), "COMPETENCY MATRIX // IST VS. SOLL (AIPLOYA MODEL)", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((right_x + 40, card_y + 75), "Target Role Requirements vs. Audited Evidence", font=f_title, fill=C_TEXT_BLACK)

    skills = [
        ("Distributed Consensus (Raft / Paxos)", 0.90, 0.98, "+8% Verified Surplus"),
        ("Go Concurrency & Memory Profiling", 0.85, 0.96, "+11% Surplus (Top 2%)"),
        ("Cloud-Native Resilience (Envoy / K8s)", 0.85, 0.92, "+7% Production Proof"),
        ("Architectural RFCs & System Design", 0.80, 0.94, "+14% Deep Judgment")
    ]
    track_w = 1200
    for s_i, (sk_name, soll, ist, delta) in enumerate(skills):
        sy = card_y + 150 + s_i * 155
        draw.text((right_x + 40, sy), sk_name, font=f_body_bold, fill=C_TEXT_BLACK)
        draw.text((right_x + track_w - 180, sy), delta, font=f_badge, fill=C_GREEN)
        
        # Track Background
        draw.rounded_rectangle([right_x + 40, sy + 38, right_x + 40 + track_w, sy + 62], radius=12, fill=C_CARD_ALT)
        # Soll marker
        soll_w = int(track_w * soll)
        draw.rounded_rectangle([right_x + 40, sy + 38, right_x + 40 + soll_w, sy + 62], radius=12, fill=(203, 213, 225, 255))
        # Ist bar
        ist_w = int(track_w * ist)
        draw.rounded_rectangle([right_x + 40, sy + 38, right_x + 40 + ist_w, sy + 62], radius=12, fill=C_BLUE)

        draw.text((right_x + 40, sy + 75), f"Target Requirement (Soll): {int(soll*100)}%   |   Audited Capability (Ist): {int(ist*100)}%", font=f_mono, fill=C_TEXT_MUTED)

    # Bottom Full-Width Card: Explainable Matching Rationale & Commit Telemetry
    bot_y = card_y + 850
    draw.rounded_rectangle([content_x, bot_y, W - 30, H - 40], radius=24, fill=C_BLUE_LIGHT, outline=(186, 230, 253, 255), width=2)
    draw.text((content_x + 40, bot_y + 35), "EXPLAINABLE MATCHING REASONING // VERIFIED RELEASE CHAIN", font=f_mono, fill=C_BLUE)
    draw.text((content_x + 40, bot_y + 70), "Why NIMO Matched Alexandre for This Specific Pod", font=f_title, fill=C_TEXT_BLACK)

    reasons = [
        "• High-Scale Architecture: Analysis of merged production PRs confirms autonomous design of event pipelines handling >250k req/s at p99 < 8ms.",
        "• Git Telemetry Verification: 142 pull requests across production repos confirm high code hygiene, zero circular dependencies, and 98% test coverage.",
        "• Peer Review Velocity: Average code review turnaround is 2.1 hours, accelerating sprint rhythm and unblocking junior/mid engineers."
    ]
    for r_i, r_text in enumerate(reasons):
        draw.text((content_x + 40, bot_y + 135 + r_i * 65), r_text, font=f_body, fill=C_TEXT_BODY)

    # Action Buttons
    draw.rounded_rectangle([content_x + 40, bot_y + 350, content_x + 520, bot_y + 440], radius=18, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((content_x + 85, bot_y + 380), "View Cryptographic Git SHA Proof", font=f_body_bold, fill=C_TEXT_BLACK)

    draw.rounded_rectangle([content_x + 550, bot_y + 350, content_x + 1050, bot_y + 440], radius=18, fill=C_BLUE)
    draw.text((content_x + 600, bot_y + 380), "Approve & Add to Pod #04 (48h SLA)", font=f_body_bold, fill=C_WHITE)

    # Downsample and save desktop & mobile
    res_desktop = im.resize((1386, 1010), Image.Resampling.LANCZOS)
    save_responsive_variants(res_desktop, 'images/6ab37f7000908fa37c5a26d5_Case Image.avif', [500, 800, 1080])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    save_responsive_variants(res_mobile, 'images/6ac37306e1bdf8eccc624a33_Case Dashboard Image 01.avif', [500, 800])

# ==========================================
# 2. CASE 02: Senior specialists and domain leads (Architectural Audit Snapshot)
# ==========================================
def render_case_02():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 36)
    f_title = ImageFont.truetype(FONT_BOLD, 26)
    f_sub = ImageFont.truetype(FONT_BOLD, 22)
    f_body = ImageFont.truetype(FONT_REG, 20)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 20)
    f_badge = ImageFont.truetype(FONT_BOLD, 17)
    f_mono = ImageFont.truetype(FONT_MONO, 17)
    f_mono_large = ImageFont.truetype(FONT_MONO, 20)

    draw_window_frame(draw, W, H, "🔒 app.spotalents.com/architecture/audit/elena-rostova", f_mono_large)
    draw_sidebar(draw, 100, H, 2, f_title, f_body, f_mono)

    cx = 490
    draw.rounded_rectangle([cx, 120, W - 30, 210], radius=18, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((cx + 35, 140), "DOMAIN LEAD CAPABILITY AUDIT // SYSTEM DESIGN BENCHMARK", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((cx + 35, 168), "Principal Architectural Depth & Mentorship Record", font=f_title, fill=C_TEXT_BLACK)
    draw_badge(draw, W - 480, 140, "98.2% ARCHITECTURE DEPTH", f_badge, C_BLUE_LIGHT, C_BLUE, radius=10, pad_x=16, pad_y=8)

    # Lead Profile Banner
    draw.rounded_rectangle([cx, 230, W - 30, 520], radius=20, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.ellipse([cx + 35, 265, cx + 155, 385], fill=C_PURPLE)
    draw.text((cx + 65, 300), "ER", font=f_head, fill=C_WHITE)

    draw.text((cx + 185, 275), "Dr. Elena Rostova", font=f_head, fill=C_TEXT_BLACK)
    draw.text((cx + 185, 325), "Principal Platform Architect & Rust/Go Lead", font=f_sub, fill=C_TEXT_MUTED)
    draw.text((cx + 185, 360), "Principal Level (L7) • Distributed Systems & RFC Author", font=f_mono, fill=C_PURPLE)

    pills = ["Rust", "Apache Kafka", "ClickHouse", "AWS EKS", "gRPC", "High-Scale Concurrency"]
    px = cx + 35
    py = 430
    for p in pills:
        bw, bh = draw_badge(draw, px, py, p, f_badge, (241, 245, 249, 255), C_TEXT_BLACK, radius=8)
        px += bw + 12

    # 3 Deep Pillars
    pillars = [
        ("SYSTEM DESIGN & RFCs", "6 Merged RFCs", "Multi-region distributed bus serving 12M DAU. Zero Sev-1 outages."),
        ("CODE REVIEW & MENTORSHIP", "480+ Deep Reviews", "96% positive velocity multiplier across 3 squads."),
        ("AUTONOMOUS SCALE", "180k msgs/sec", "Built zero-downtime streaming pipeline at p99 < 12ms.")
    ]
    card_w = (W - cx - 70) // 3
    for idx, (head, stat, desc) in enumerate(pillars):
        px = cx + idx * (card_w + 20)
        py = 545
        draw.rounded_rectangle([px, py, px + card_w, py + 480], radius=20, fill=C_CARD_ALT, outline=C_BORDER, width=2)
        draw.text((px + 25, py + 30), head, font=f_mono, fill=C_BLUE)
        draw.text((px + 25, py + 75), stat, font=f_head, fill=C_TEXT_BLACK)
        draw.line([(px + 25, py + 145), (px + card_w - 25, py + 145)], fill=C_BORDER, width=2)
        
        words = desc.split()
        draw.text((px + 25, py + 180), " ".join(words[:4]), font=f_body, fill=C_TEXT_BODY)
        draw.text((px + 25, py + 220), " ".join(words[4:]), font=f_body, fill=C_TEXT_BODY)
        draw_badge(draw, px + 25, py + 390, "AUDITED VIA GIT", f_badge, C_GREEN_LIGHT, C_GREEN, radius=8)

    # Bottom Explainable Note
    bot_y = 1050
    draw.rounded_rectangle([cx, bot_y, W - 30, H - 35], radius=20, fill=C_BLUE_LIGHT, outline=(186, 230, 253, 255), width=2)
    draw.text((cx + 35, bot_y + 30), "NIMO EXPLAINABLE REASONING // ARCHITECTURAL MATURITY", font=f_mono, fill=C_BLUE)
    draw.text((cx + 35, bot_y + 70), "Elena matched for complex distributed platform overhaul. RFC history validates capacity to define architectural standards, decompose legacy monoliths, and guide senior engineers autonomously.", font=f_body, fill=C_TEXT_BLACK)
    
    draw.rounded_rectangle([cx + 35, bot_y + 260, cx + 550, bot_y + 350], radius=16, fill=C_BLUE)
    draw.text((cx + 80, bot_y + 290), "Confirm Elena for Platform Lead", font=f_body_bold, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    save_responsive_variants(res_desktop, 'images/6ac0f44b97ebd2aa1d167d71_Cases Image 02.avif', [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    save_responsive_variants(res_mobile, 'images/6ac3730617c04dbca55b7771_Case Dashboard Image 02.avif', [500, 800])

# ==========================================
# 3. CASE 03: Staff architects and fractional CTOs (Executive Leadership Snapshot)
# ==========================================
def render_case_03():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 36)
    f_title = ImageFont.truetype(FONT_BOLD, 26)
    f_sub = ImageFont.truetype(FONT_BOLD, 22)
    f_body = ImageFont.truetype(FONT_REG, 20)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 20)
    f_badge = ImageFont.truetype(FONT_BOLD, 17)
    f_mono = ImageFont.truetype(FONT_MONO, 17)
    f_mono_large = ImageFont.truetype(FONT_MONO, 20)

    draw_window_frame(draw, W, H, "🔒 app.spotalents.com/executive/david-sterling", f_mono_large)
    draw_sidebar(draw, 100, H, 0, f_title, f_body, f_mono)

    cx = 490
    draw.rounded_rectangle([cx, 120, W - 30, 210], radius=18, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((cx + 35, 140), "EXECUTIVE TECHNICAL LEADERSHIP // FRACTIONAL CTO SUITE", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((cx + 35, 168), "Strategic Roadmap Governance & Architecture Triage", font=f_title, fill=C_TEXT_BLACK)
    draw_badge(draw, W - 480, 140, "99.1% GOVERNANCE INDEX", f_badge, C_BLUE_LIGHT, C_BLUE, radius=10, pad_x=16, pad_y=8)

    # Executive Profile Banner
    draw.rounded_rectangle([cx, 230, W - 30, 520], radius=20, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.ellipse([cx + 35, 265, cx + 155, 385], fill=(15, 23, 42, 255))
    draw.text((cx + 65, 300), "DS", font=f_head, fill=C_WHITE)

    draw.text((cx + 185, 275), "David Sterling", font=f_head, fill=C_TEXT_BLACK)
    draw.text((cx + 185, 325), "Fractional CTO & Staff Architect (Series B Tech Veteran)", font=f_sub, fill=C_TEXT_MUTED)
    draw.text((cx + 185, 360), "15-20 Hours / Week • Dedicated Architecture Advisory", font=f_mono, fill=C_GREEN)

    pills = ["Technical Debt Triage", "SOC2 Architecture", "Org Design", "Board Advisory", "Cost Optimization"]
    px = cx + 35
    py = 430
    for p in pills:
        bw, bh = draw_badge(draw, px, py, p, f_badge, (241, 245, 249, 255), C_TEXT_BLACK, radius=8)
        px += bw + 12

    # 3 Strategic Scorecards
    scorecards = [
        ("TECH DEBT VELOCITY", "-45% Debt", "Eliminated high-risk architectural debt across 4 services in 90 days."),
        ("TEAM VELOCITY", "+34% Speed", "Synchronized sprint delivery rhythm across 4 independent squads."),
        ("ARCHITECTURE SLA", "100% Pass", "SOC2 compliance and zero architectural security regressions.")
    ]
    card_w = (W - cx - 70) // 3
    for idx, (head, stat, desc) in enumerate(scorecards):
        px = cx + idx * (card_w + 20)
        py = 545
        draw.rounded_rectangle([px, py, px + card_w, py + 480], radius=20, fill=C_CARD_ALT, outline=C_BORDER, width=2)
        draw.text((px + 25, py + 30), head, font=f_mono, fill=C_BLUE)
        draw.text((px + 25, py + 75), stat, font=f_head, fill=C_TEXT_BLACK)
        draw.line([(px + 25, py + 145), (px + card_w - 25, py + 145)], fill=C_BORDER, width=2)
        
        words = desc.split()
        draw.text((px + 25, py + 180), " ".join(words[:4]), font=f_body, fill=C_TEXT_BODY)
        draw.text((px + 25, py + 220), " ".join(words[4:]), font=f_body, fill=C_TEXT_BODY)
        draw_badge(draw, px + 25, py + 390, "AUDITED IMPACT", f_badge, C_BLUE_LIGHT, C_BLUE, radius=8)

    # Multi-Squad Alignment Tracker
    bot_y = 1050
    draw.rounded_rectangle([cx, bot_y, W - 30, H - 35], radius=20, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((cx + 35, bot_y + 30), "MULTI-SQUAD ARCHITECTURAL SYNCHRONIZATION // LIVE GOVERNANCE", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((cx + 35, bot_y + 70), "Squad 1 (Platform): Synchronized [✓]   |   Squad 2 (Core): Synchronized [✓]   |   Squad 3 (Data): Synchronized [✓]", font=f_sub, fill=C_TEXT_BLACK)
    
    draw.rounded_rectangle([cx + 35, bot_y + 260, cx + 550, bot_y + 350], radius=16, fill=C_BLUE)
    draw.text((cx + 80, bot_y + 290), "Book Strategic Roadmap Alignment", font=f_body_bold, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    save_responsive_variants(res_desktop, 'images/6ac0f44b4b73a87c95802a54_Cases Image 03.avif', [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    save_responsive_variants(res_mobile, 'images/6ac37306461ca2eb8f3838fd_Case Dashboard Image 03.avif', [500, 800])

# ==========================================
# 4. CASE 04: Turn-key squads calibrated for scale (Squad Builder Snapshot)
# ==========================================
def render_case_04():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 36)
    f_title = ImageFont.truetype(FONT_BOLD, 26)
    f_sub = ImageFont.truetype(FONT_BOLD, 22)
    f_body = ImageFont.truetype(FONT_REG, 20)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 20)
    f_badge = ImageFont.truetype(FONT_BOLD, 17)
    f_mono = ImageFont.truetype(FONT_MONO, 17)
    f_mono_large = ImageFont.truetype(FONT_MONO, 20)

    draw_window_frame(draw, W, H, "🔒 app.spotalents.com/pods/platform-scaling-04", f_mono_large)
    draw_sidebar(draw, 100, H, 4, f_title, f_body, f_mono)

    cx = 490
    draw.rounded_rectangle([cx, 120, W - 30, 210], radius=18, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((cx + 35, 140), "AUTONOMOUS SQUAD CALIBRATION // POD #04 PLATFORM SCALING", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((cx + 35, 168), "Pre-Matched Engineering Squad with Day-One Cadence", font=f_title, fill=C_TEXT_BLACK)
    draw_badge(draw, W - 480, 140, "96.4% TEAM CHEMISTRY", f_badge, C_GREEN_LIGHT, C_GREEN, radius=10, pad_x=16, pad_y=8)

    # 4 Seats Grid (2x2)
    seats = [
        ("SEAT 1 // TECH LEAD", "Marcus Vance", "Staff Backend Lead • Go / K8s", "98% Fit Score", C_BLUE),
        ("SEAT 2 // SENIOR FULLSTACK", "Sofia Lin", "Senior Fullstack • React / TypeScript", "95% Fit Score", C_PURPLE),
        ("SEAT 3 // SENIOR CLOUD INFRA", "Tariq Nabil", "Senior DevOps • Terraform / AWS", "97% Fit Score", C_GREEN),
        ("SEAT 4 // QA AUTOMATION", "Maya Kapoor", "Staff QA • Playwright / CI Ops", "94% Fit Score", (234, 88, 12, 255))
    ]
    card_w = (W - cx - 50) // 2
    card_h = 360
    for idx, (lbl, name, role, fit, col) in enumerate(seats):
        row = idx // 2
        col_idx = idx % 2
        sx = cx + col_idx * (card_w + 20)
        sy = 230 + row * (card_h + 20)
        draw.rounded_rectangle([sx, sy, sx + card_w, sy + card_h], radius=20, fill=C_WHITE, outline=C_BORDER, width=2)
        
        draw.text((sx + 30, sy + 25), lbl, font=f_mono, fill=C_TEXT_MUTED)
        draw_badge(draw, sx + card_w - 200, sy + 20, fit, f_badge, C_WHITE, col, radius=8)

        draw.text((sx + 30, sy + 75), name, font=f_head, fill=C_TEXT_BLACK)
        draw.text((sx + 30, sy + 125), role, font=f_sub, fill=C_TEXT_MUTED)
        draw.line([(sx + 30, sy + 185), (sx + card_w - 30, sy + 185)], fill=C_BORDER, width=2)
        
        draw.text((sx + 30, sy + 220), "• Day-One Sprint Integration  |  Pre-Tested Chemistry", font=f_body, fill=C_TEXT_BODY)
        draw.text((sx + 30, sy + 265), "• 40 Hours/wk Dedicated Allocation", font=f_body, fill=C_TEXT_BODY)

    # Bottom Pod Summary Banner
    bot_y = 1010
    draw.rounded_rectangle([cx, bot_y, W - 30, H - 35], radius=20, fill=C_BLUE_LIGHT, outline=(186, 230, 253, 255), width=2)
    draw.text((cx + 35, bot_y + 30), "COMBINED SQUAD CAPACITY // 160 HOURS/WEEK // 48-HOUR SPRINT READY", font=f_mono, fill=C_BLUE)
    draw.text((cx + 35, bot_y + 70), "Pod delivery multiplier evaluated at +38% compared to uncoordinated individual hires. Code environments, CI pipelines, and PR standards pre-aligned.", font=f_body, fill=C_TEXT_BLACK)
    
    draw.rounded_rectangle([cx + 35, bot_y + 260, cx + 550, bot_y + 350], radius=16, fill=C_BLUE)
    draw.text((cx + 80, bot_y + 290), "Deploy Pod #04 to Production", font=f_body_bold, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    save_responsive_variants(res_desktop, 'images/6ac0f44a4b73a87c95802a34_Cases Image 04.avif', [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    save_responsive_variants(res_mobile, 'images/6ac3730693b442b8285082bc_Case Dashboard Image 04.avif', [500, 800])

# ==========================================
# 5. CASE 05: Proof over resume claims (Evidence Inspector Snapshot)
# ==========================================
def render_case_05():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 36)
    f_title = ImageFont.truetype(FONT_BOLD, 26)
    f_sub = ImageFont.truetype(FONT_BOLD, 22)
    f_body = ImageFont.truetype(FONT_REG, 20)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 20)
    f_badge = ImageFont.truetype(FONT_BOLD, 17)
    f_mono = ImageFont.truetype(FONT_MONO, 17)
    f_mono_large = ImageFont.truetype(FONT_MONO, 20)

    draw_window_frame(draw, W, H, "🔒 app.spotalents.com/evidence/verify/candidate-7712", f_mono_large)
    draw_sidebar(draw, 100, H, 3, f_title, f_body, f_mono)

    cx = 490
    draw.rounded_rectangle([cx, 120, W - 30, 210], radius=18, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((cx + 35, 140), "CODEBASE TELEMETRY // CV CLAIM VS. GIT REALITY AUDIT", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((cx + 35, 168), "Cryptographically Audited Evidence Engine", font=f_title, fill=C_TEXT_BLACK)
    draw_badge(draw, W - 520, 140, "CRYPTOGRAPHICALLY AUDITED", f_badge, C_GREEN_LIGHT, C_GREEN, radius=10, pad_x=16, pad_y=8)

    rows = [
        ("CV RESUME CLAIM: Expert in Go microservices & cloud scalability", "84,200 LOC in Production Go Services • 142 Merged PRs verified via Git SHA.", "VERIFIED 98.4%", C_GREEN),
        ("CV RESUME CLAIM: High velocity contributor with strong test standards", "3.6 Merged PRs / week • 94.8% first-pass CI/CD test pass rate • 2.2h review cycle.", "VERIFIED 96.2%", C_GREEN),
        ("CV RESUME CLAIM: Database query & performance tuning specialist", "PostgreSQL query optimization: p99 latency cut from 320ms to 8ms on 50M rows in prod.", "VERIFIED 99.0%", C_GREEN)
    ]
    card_h = 230
    for idx, (claim, proof, stat, col) in enumerate(rows):
        ry = 230 + idx * (card_h + 20)
        draw.rounded_rectangle([cx, ry, W - 30, ry + card_h], radius=20, fill=C_WHITE, outline=C_BORDER, width=2)
        
        draw.text((cx + 30, ry + 25), claim, font=f_sub, fill=(225, 29, 72, 255))
        draw_badge(draw, W - 320, ry + 20, stat, f_badge, C_WHITE, col, radius=8)
        draw.line([(cx + 30, ry + 80), (W - 60, ry + 80)], fill=C_BORDER, width=2)
        
        draw.text((cx + 30, ry + 105), "TELEMETRY EVIDENCE PROOF (NIMO ENGINE):", font=f_mono, fill=C_BLUE)
        draw.text((cx + 30, ry + 145), proof, font=f_body, fill=C_TEXT_BLACK)

    # Bottom Summary
    bot_y = 1000
    draw.rounded_rectangle([cx, bot_y, W - 30, H - 35], radius=20, fill=C_BLUE_LIGHT, outline=(186, 230, 253, 255), width=2)
    draw.text((cx + 35, bot_y + 30), "EVIDENCE CONFIDENCE SCORE: 99.4% // ZERO CV HALLUCINATIONS DETECTED", font=f_mono, fill=C_BLUE)
    draw.text((cx + 35, bot_y + 70), "Spotalents extracts actual git telemetry, commit authorship, and code complexity scores directly from production repos, eliminating resume inflation and self-reporting bias.", font=f_body, fill=C_TEXT_BLACK)
    
    draw.rounded_rectangle([cx + 35, bot_y + 260, cx + 550, bot_y + 350], radius=16, fill=C_BLUE)
    draw.text((cx + 80, bot_y + 290), "Download Cryptographic Dossier (PDF)", font=f_body_bold, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    save_responsive_variants(res_desktop, 'images/6ac0f44bd95a8b30192bce9f_Cases Image 05.avif', [500, 800])

    res_mobile = im.resize((962, 700), Image.Resampling.LANCZOS)
    save_responsive_variants(res_mobile, 'images/6ac373063b5857609808d81d_Case Dashboard Image 05.avif', [500, 800])

# ==========================================
# 6. CASE 06: Smarter matches after each sprint (Sprint Telemetry Snapshot)
# ==========================================
def render_case_06():
    W, H = 2080, 1516
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 36)
    f_title = ImageFont.truetype(FONT_BOLD, 26)
    f_sub = ImageFont.truetype(FONT_BOLD, 22)
    f_body = ImageFont.truetype(FONT_REG, 20)
    f_body_bold = ImageFont.truetype(FONT_BOLD, 20)
    f_badge = ImageFont.truetype(FONT_BOLD, 17)
    f_mono = ImageFont.truetype(FONT_MONO, 17)
    f_mono_large = ImageFont.truetype(FONT_MONO, 20)

    draw_window_frame(draw, W, H, "🔒 app.spotalents.com/telemetry/pods/pod-04/sprint-12", f_mono_large)
    draw_sidebar(draw, 100, H, 5, f_title, f_body, f_mono)

    cx = 490
    draw.rounded_rectangle([cx, 120, W - 30, 210], radius=18, fill=C_WHITE, outline=C_BORDER, width=2)
    draw.text((cx + 35, 140), "CONTINUOUS SPRINT TELEMETRY // ADAPTIVE MATCH TUNING", font=f_mono, fill=C_TEXT_MUTED)
    draw.text((cx + 35, 168), "Live Sprint Performance & Adaptive Model Recalibration", font=f_title, fill=C_TEXT_BLACK)
    draw_badge(draw, W - 480, 140, "ADAPTIVE LEARNING ACTIVE", f_badge, C_BLUE_LIGHT, C_BLUE, radius=10, pad_x=16, pad_y=8)

    # 3 Sprint Telemetry Cards
    sprint_kpis = [
        ("MILESTONE DELIVERY SLA", "99.2%", "12 Sprints Completed on Schedule. Top 5% Industry Velocity."),
        ("CYCLE TIME VELOCITY", "1.8 Hours", "PR Review to Merge latency. 4x faster than industry median."),
        ("POD HEALTH & SATISFACTION", "98.4%", "Net positive collaboration score from tech leadership.")
    ]
    card_w = (W - cx - 70) // 3
    for idx, (head, stat, desc) in enumerate(sprint_kpis):
        px = cx + idx * (card_w + 20)
        py = 230
        draw.rounded_rectangle([px, py, px + card_w, py + 480], radius=20, fill=C_WHITE, outline=C_BORDER, width=2)
        draw.text((px + 25, py + 30), head, font=f_mono, fill=C_BLUE)
        draw.text((px + 25, py + 75), stat, font=f_head, fill=C_TEXT_BLACK)
        draw.line([(px + 25, py + 145), (px + card_w - 25, py + 145)], fill=C_BORDER, width=2)
        
        words = desc.split()
        draw.text((px + 25, py + 180), " ".join(words[:4]), font=f_body, fill=C_TEXT_BODY)
        draw.text((px + 25, py + 220), " ".join(words[4:]), font=f_body, fill=C_TEXT_BODY)
        draw_badge(draw, px + 25, py + 390, "SPRINT AUDITED", f_badge, C_GREEN_LIGHT, C_GREEN, radius=8)

    # Adaptive Learning Engine Box
    bot_y = 740
    draw.rounded_rectangle([cx, bot_y, W - 30, H - 35], radius=20, fill=C_BLUE_LIGHT, outline=(186, 230, 253, 255), width=2)
    draw.text((cx + 35, bot_y + 30), "ADAPTIVE MATCHING FEEDBACK LOOP // CONTINUOUS CALIBRATION", font=f_mono, fill=C_BLUE)
    draw.text((cx + 35, bot_y + 70), "How Spotalents Intelligence Learns From Every Deployed Sprint", font=f_title, fill=C_TEXT_BLACK)

    learnings = [
        "• Sprint #12 Delivery Telemetry parsed: Codebase velocity and PR rhythm incorporated into organization talent model.",
        "• Matching precision recalibrated: Model adjusted for high-throughput concurrency, yielding +3.1% precision on future hires.",
        "• Autonomous pod rebalancing: Engineering manager notified of capacity headroom 2 sprints ahead of product roadmap deadlines."
    ]
    for l_i, l_text in enumerate(learnings):
        draw.text((cx + 35, bot_y + 145 + l_i * 85), l_text, font=f_body, fill=C_TEXT_BODY)

    draw.rounded_rectangle([cx + 35, bot_y + 440, cx + 550, bot_y + 530], radius=16, fill=C_BLUE)
    draw.text((cx + 80, bot_y + 470), "View Sprint Telemetry Report", font=f_body_bold, fill=C_WHITE)

    res_desktop = im.resize((1040, 758), Image.Resampling.LANCZOS)
    save_responsive_variants(res_desktop, 'images/6ac0f44bbebcfc65055a419a_Cases Image 06.avif', [500, 800])

    res_mobile = im.resize((962, 752), Image.Resampling.LANCZOS)
    save_responsive_variants(res_mobile, 'images/6ac37306e1bdf8eccc624a13_Case Dashboard Image 06.avif', [500, 800])

if __name__ == '__main__':
    print("Generating Case 01 Real UI...")
    render_case_01()
    print("Generating Case 02 Real UI...")
    render_case_02()
    print("Generating Case 03 Real UI...")
    render_case_03()
    print("Generating Case 04 Real UI...")
    render_case_04()
    print("Generating Case 05 Real UI...")
    render_case_05()
    print("Generating Case 06 Real UI...")
    render_case_06()
    print("All 6 cases regenerated as real product demo snapshots!")

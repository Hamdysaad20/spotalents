import os
from PIL import Image, ImageDraw, ImageFont

def render_find_image():
    # Render at 2x scale: 4800 x 500, then downsample to 2400 x 250
    W, H = 4800, 500
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    font_bold_title = ImageFont.truetype('/tmp/InstrumentSans-Bold.ttf', 34)
    font_bold_sub = ImageFont.truetype('/tmp/InstrumentSans-Bold.ttf', 24)
    font_bold_badge = ImageFont.truetype('/tmp/InstrumentSans-Bold.ttf', 20)
    font_regular = ImageFont.truetype('/tmp/InstrumentSans.ttf', 22)
    font_mono = ImageFont.truetype('/tmp/SpaceMono.ttf', 20)

    # Background track container
    track_rect = [60, 40, W - 60, H - 40]
    draw.rounded_rectangle(track_rect, radius=32, fill=(255, 255, 255, 245), outline=(226, 232, 240, 255), width=3)

    # Connecting horizontal line
    draw.line([(200, H // 2), (W - 200, H // 2)], fill=(226, 232, 240, 255), width=6)
    # Active progress line up to 85%
    draw.line([(200, H // 2), (int(W * 0.82), H // 2)], fill=(1, 59, 255, 255), width=6)

    # 5 Stages
    stages = [
        {
            "step": "STEP 01 // 0:00",
            "title": "Role Context Ingestion",
            "desc": "Lead Go/K8s + React Pod",
            "badge": "SPEC VALIDATED",
            "badge_bg": (233, 246, 255, 255),
            "badge_fg": (1, 59, 255, 255),
            "dot_active": True
        },
        {
            "step": "STEP 02 // 0:20",
            "title": "NIMO Signal Matching",
            "desc": "4,820 Evaluated → 14 Scored",
            "badge": "96.4% CONFIDENCE",
            "badge_bg": (236, 253, 245, 255),
            "badge_fg": (16, 185, 129, 255),
            "dot_active": True
        },
        {
            "step": "STEP 03 // 1:05",
            "title": "Git & Codebase Audit",
            "desc": "142 PRs Audited • 2.1h Cycle",
            "badge": "PRODUCTION PROOF",
            "badge_bg": (233, 246, 255, 255),
            "badge_fg": (1, 59, 255, 255),
            "dot_active": True
        },
        {
            "step": "STEP 04 // 1:30",
            "title": "Squad Calibration",
            "desc": "Lead + 2 Seniors + QA",
            "badge": "97.8% CHEMISTRY",
            "badge_bg": (236, 253, 245, 255),
            "badge_fg": (16, 185, 129, 255),
            "dot_active": True
        },
        {
            "step": "STEP 05 // 3:40",
            "title": "Activated to Production",
            "desc": "Shipping Code in 48 Hours",
            "badge": "POD LIVE // DEPLOYED",
            "badge_bg": (1, 59, 255, 255),
            "badge_fg": (255, 255, 255, 255),
            "dot_active": True
        }
    ]

    card_width = 820
    card_height = 340
    spacing = (W - 240 - (5 * card_width)) // 4
    start_x = 120

    for i, s in enumerate(stages):
        cx = start_x + i * (card_width + spacing)
        cy = (H - card_height) // 2
        card_rect = [cx, cy, cx + card_width, cy + card_height]

        # Draw card background
        is_last = (i == 4)
        card_bg = (248, 250, 252, 255) if not is_last else (239, 246, 255, 255)
        border_col = (1, 59, 255, 180) if is_last else (226, 232, 240, 255)
        draw.rounded_rectangle(card_rect, radius=24, fill=card_bg, outline=border_col, width=3 if not is_last else 4)

        # Header step
        draw.text((cx + 36, cy + 32), s["step"], font=font_mono, fill=(100, 116, 139, 255))
        
        # Status Badge top right
        badge_text = s["badge"]
        bbox = font_bold_badge.getbbox(badge_text)
        bw = bbox[2] - bbox[0] + 28
        bh = bbox[3] - bbox[1] + 18
        bx = cx + card_width - bw - 36
        by = cy + 28
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=s["badge_bg"])
        draw.text((bx + 14, by + 7), badge_text, font=font_bold_badge, fill=s["badge_fg"])

        # Title
        draw.text((cx + 36, cy + 95), s["title"], font=font_bold_title, fill=(15, 23, 42, 255))
        
        # Description
        draw.text((cx + 36, cy + 155), s["desc"], font=font_regular, fill=(51, 65, 85, 255))

        # Bottom telemetry indicators
        draw.line([(cx + 36, cy + 225), (cx + card_width - 36, cy + 225)], fill=(226, 232, 240, 200), width=2)
        
        # Indicator dots
        draw.ellipse([cx + 36, cy + 255, cx + 52, cy + 271], fill=(16, 185, 129, 255) if not is_last else (1, 59, 255, 255))
        telemetry_txt = "Verified Git SHA • NIMO Engine" if i < 4 else "Active Pod ID: #842 • 48h SLA Active"
        draw.text((cx + 66, cy + 252), telemetry_txt, font=font_bold_badge, fill=(71, 85, 105, 255))

    # Downsample to 2400 x 250 with Lanczos
    res = im.resize((2400, 250), Image.Resampling.LANCZOS)
    res.save('/tmp/test_find_out.png', 'PNG')
    print('Rendered /tmp/test_find_out.png successfully!')

render_find_image()

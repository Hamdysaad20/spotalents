import os
import math
from PIL import Image, ImageDraw, ImageFont

# Ensure fonts
FONT_BOLD = '/tmp/InstrumentSans-Bold.ttf'
FONT_REG = '/tmp/InstrumentSans.ttf'
FONT_MONO = '/tmp/SpaceMono.ttf'

# Colors
C_BG_CREAM = (241, 241, 229, 255)       # #F1F1E5
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

def save_responsive_variants(base_img, base_path, widths):
    # Save main file (both AVIF and PNG)
    base_img.save(base_path, 'AVIF', quality=95)
    png_path = base_path.replace('.avif', '.png')
    base_img.save(png_path, 'PNG')
    print(f"Saved: {base_path}")

    # Generate each responsive width
    orig_w, orig_h = base_img.size
    for w in widths:
        if w < orig_w:
            h = int(orig_h * (w / orig_w))
            res_img = base_img.resize((w, h), Image.Resampling.LANCZOS)
            var_path = base_path.replace('.avif', f'-p-{w}.avif')
            res_img.save(var_path, 'AVIF', quality=90)
            res_img.save(var_path.replace('.avif', '.png'), 'PNG')
            print(f"  Variant: {var_path} ({w}x{h})")

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
    W, H = 4800, 500  # 2x supersampling
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

print("find image logic ready")

"""Cover 23: Data Infrastructure Quality for AI Readiness"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "/Users/aupadh12/Desktop/Ashutosh_work/Blog_contents/enigmaAI/blogposts/covers"

def load_font_ttc(size, index=0):
    try:
        return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=index)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except:
            return ImageFont.load_default()

def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def text_center(draw, text, cx, y, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    w = bb[2] - bb[0]
    draw.text((cx - w // 2, y), text, font=font, fill=fill)

def wrap_text(draw, text, x, y, max_width, font, fill):
    bb = draw.textbbox((0, 0), "Ag", font=font)
    lh = (bb[3] - bb[1]) + 6
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_width:
            line = test
        else:
            if line:
                draw.text((x, y), line, font=font, fill=fill)
                y += lh
            line = word
    if line:
        draw.text((x, y), line, font=font, fill=fill)
    return y

def draw_arrow(draw, x0, y0, x1, y1, color, width=2, head=8):
    import math
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for side in (+0.5, -0.5):
        ax = x1 - head * math.cos(angle - side)
        ay = y1 - head * math.sin(angle - side)
        draw.line([(x1, y1), (ax, ay)], fill=color, width=width)

def cover_23():
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), (12, 8, 18))
    draw = ImageDraw.Draw(img)

    # Dark purple-teal gradient background
    for i in range(H):
        t = i / H
        draw.line([(0, i), (W, i)], fill=(int(12+5*t), int(8+5*t), int(18+16*t)))
    draw.rectangle([430, 0, W, H], fill=(14, 10, 24))

    ACCENT = (168, 85, 247)    # violet/purple
    ACCENT2 = (196, 130, 255)
    TEAL = (45, 212, 191)
    AMBER = (251, 191, 36)
    RED = (239, 68, 68)
    GREEN = (74, 222, 128)
    TEXT_DIM = (150, 140, 180)

    font_tiny  = load_font_ttc(11)
    font_small = load_font_ttc(13)
    font_head  = load_font_ttc(15, index=1)
    font_badge = load_font_ttc(11, index=1)
    font_stat  = load_font_ttc(30, index=1)
    font_stat_lbl = load_font_ttc(11)
    font_diag_title = load_font_ttc(12, index=1)

    # ---- LEFT SIDE ----
    # Badge
    badge_text = "DATA ENGINEERING"
    bb = draw.textbbox((0,0), badge_text, font=font_badge)
    bw, bh = bb[2]-bb[0]+28, bb[3]-bb[1]+14
    rounded_rect(draw, [44, 54, 44+bw, 54+bh], 20, fill=ACCENT)
    draw.text((44+14, 54+7), badge_text, font=font_badge, fill=(255,255,255))

    draw.text((44, 108), "Data Infrastructure", font=load_font_ttc(36, index=1), fill=(235, 240, 255))
    draw.text((44, 156), "Quality for", font=load_font_ttc(34, index=1), fill=ACCENT2)
    draw.text((44, 200), "AI Readiness", font=load_font_ttc(34, index=1), fill=TEAL)

    sub = "From raw bytes to AI-ready. The five levels of readiness — and the silent failures that stop you at Level 2."
    wrap_text(draw, sub, 44, 260, 360, load_font_ttc(15), TEXT_DIM)

    # Stats
    y_stats = 375
    for val, lbl, sx in [("5", "READINESS LEVELS", 44), ("6", "QUALITY DIMS", 190), ("0", "SILENT ERRORS", 316)]:
        draw.text((sx, y_stats), val, font=font_stat, fill=ACCENT)
        draw.text((sx, y_stats + 38), lbl, font=font_stat_lbl, fill=TEXT_DIM)

    # Author
    y = H - 52
    ax, ar = 28, 18
    draw.ellipse([ax, y, ax+ar*2, y+ar*2], fill=ACCENT)
    text_center(draw, "A", ax+ar, y+ar-8, load_font_ttc(15, index=1), (255,255,255))
    draw.text((ax+ar*2+10, y+2), "Ashutosh Upadhyay", font=load_font_ttc(14, index=1), fill=(230,230,230))
    draw.text((ax+ar*2+10, y+20), "Platform Engineering, J&J Innovative Medicine", font=load_font_ttc(13), fill=(150,150,160))

    # Tags
    tags = ["Data Quality", "AI Readiness", "S3", "Parquet", "AWS"]
    x = W - 20
    ty = H - 38
    for tag in reversed(tags):
        bb = draw.textbbox((0,0), tag, font=font_tiny)
        tw = bb[2]-bb[0]+20
        rounded_rect(draw, [x-tw, ty, x, ty+26], 13, fill=(30,20,50), outline=(80,60,110), width=1)
        draw.text((x-tw+10, ty+5), tag, font=font_tiny, fill=(190,180,220))
        x -= tw + 8

    # ---- RIGHT: Five-level readiness pyramid ----
    RX = 460
    draw.text((RX+30, 28), "AI DATA READINESS FRAMEWORK — FIVE LEVELS (BREWER ET AL., 2025)", font=font_diag_title, fill=(120, 80, 200))

    levels = [
        ("L0  Raw", "As-produced: inconsistent formats, schema drift, missing fields", RED, (40,8,8)),
        ("L1  Cleaned", "Types consistent, nulls handled, duplicates removed", AMBER, (38,28,8)),
        ("L2  Structured", "Parquet/HDF5, partitioned, queryable via Athena", TEAL, (8,32,30)),
        ("L3  Enriched", "Joined with ontologies, annotated, feature-engineered", GREEN, (10,34,16)),
        ("L4  AI-Ready", "Validated schema · freshness checked · serving format optimised", ACCENT2, (22,12,40)),
    ]

    ly = 72
    for label, desc, color, bg in levels:
        rounded_rect(draw, [RX+20, ly, RX+680, ly+68], 8, fill=bg, outline=color, width=1)
        draw.text((RX+30, ly+10), label, font=font_head, fill=color)
        wrap_text(draw, desc, RX+160, ly+10, 490, font_small, TEXT_DIM)
        ly += 78

    # Silent failures panel
    rounded_rect(draw, [RX+20, ly+8, RX+680, ly+110], 8, fill=(20,10,16), outline=RED, width=2)
    draw.text((RX+30, ly+18), "⚠  Silent Failures That Block L2 → L4", font=load_font_ttc(13, index=1), fill=(240,100,100))
    failures = [
        ("Athena UNLOAD", "files have no .parquet extension  →  endswith() always False"),
        ("TSV delimiter trap", "read_csv defaults to comma  →  one-column table, no error"),
        ("large_string type",  "large_string != pa.string()  →  type checks silently miss"),
        ("Null propagation",   "pc.or_(null, False) = null  →  all rows filtered out"),
    ]
    fy = ly + 38
    for cause, effect in failures:
        draw.text((RX+34, fy), f"• {cause}:", font=load_font_ttc(12, index=1), fill=(220,160,160))
        draw.text((RX+34+170, fy), effect, font=font_tiny, fill=TEXT_DIM)
        fy += 16

    # Freshness note
    rounded_rect(draw, [RX+20, ly+122, RX+680, ly+160], 6, fill=(14,20,14), outline=GREEN, width=1)
    text_center(draw, "Freshness is a first-class quality dimension [IBM Think]. Build a per-source manifest. Check it before answering.", (RX+20+RX+680)//2, ly+132, font_small, (120,220,150))
    text_center(draw, "not_ingested ≠ empty result  — always return a status, never an empty list as the answer.", (RX+20+RX+680)//2, ly+150, font_tiny, TEXT_DIM)

    img.save(os.path.join(OUTPUT_DIR, "23-data-infrastructure-quality-ai-readiness.png"))
    print("✓ cover 23")

cover_23()

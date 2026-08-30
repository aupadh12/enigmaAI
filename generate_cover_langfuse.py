"""Cover 23: Langfuse LLM Observability"""
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

def wrap_text(draw, text, x, y, max_width, font, fill, lh=None):
    bb = draw.textbbox((0, 0), "Ag", font=font)
    if lh is None:
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

def cover_23_langfuse():
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), (8, 6, 20))
    draw = ImageDraw.Draw(img)

    # Deep indigo background
    for i in range(H):
        t = i / H
        draw.line([(0, i), (W, i)], fill=(int(8+6*t), int(6+5*t), int(20+18*t)))
    draw.rectangle([430, 0, W, H], fill=(10, 8, 26))

    # Langfuse brand: orange/amber accent
    ACCENT = (251, 146, 60)   # orange
    ACCENT2 = (253, 186, 116)
    TEAL = (45, 212, 191)
    PURPLE = (167, 139, 250)
    GREEN = (74, 222, 128)
    TEXT_DIM = (145, 138, 175)
    BOX_BG = (16, 14, 36)

    font_tiny  = load_font_ttc(11)
    font_small = load_font_ttc(13)
    font_head  = load_font_ttc(15, index=1)
    font_badge = load_font_ttc(11, index=1)
    font_stat  = load_font_ttc(30, index=1)
    font_stat_lbl = load_font_ttc(11)
    font_diag_title = load_font_ttc(12, index=1)

    # ---- LEFT SIDE ----
    bb = draw.textbbox((0,0), "OBSERVABILITY", font=font_badge)
    bw, bh = bb[2]-bb[0]+28, bb[3]-bb[1]+14
    rounded_rect(draw, [44, 54, 44+bw, 54+bh], 20, fill=ACCENT)
    draw.text((44+14, 54+7), "OBSERVABILITY", font=font_badge, fill=(255,255,255))

    draw.text((44, 108), "Langfuse in", font=load_font_ttc(40, index=1), fill=(235, 240, 255))
    draw.text((44, 158), "Production:", font=load_font_ttc(36, index=1), fill=ACCENT2)
    draw.text((44, 204), "LLM Observability", font=load_font_ttc(26, index=1), fill=(200, 215, 255))
    draw.text((44, 238), "Beyond Console Logs", font=load_font_ttc(24, index=1), fill=(170, 185, 230))

    sub = "Every trace. Every cost. Every prompt version. Every evaluation score. All in one open-source platform."
    wrap_text(draw, sub, 44, 282, 360, load_font_ttc(15), TEXT_DIM)

    y_stats = 380
    for val, lbl, sx in [("90B+", "OBS/MONTH", 44), ("33k", "GITHUB STARS", 168), ("4", "PILLARS", 316)]:
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
    tags = ["Langfuse", "LLM", "OpenTelemetry", "EKS", "Multi-Agent"]
    x = W - 20
    ty = H - 38
    for tag in reversed(tags):
        bb = draw.textbbox((0,0), tag, font=font_tiny)
        tw = bb[2]-bb[0]+20
        rounded_rect(draw, [x-tw, ty, x, ty+26], 13, fill=(22,18,44), outline=(80,64,140), width=1)
        draw.text((x-tw+10, ty+5), tag, font=font_tiny, fill=(190,180,220))
        x -= tw + 8

    # ---- RIGHT: Trace hierarchy diagram ----
    RX = 460
    draw.text((RX+30, 28), "MULTI-AGENT TRACE — LANGFUSE OBSERVABILITY", font=font_diag_title, fill=(140, 90, 50))

    # Top-level trace
    rounded_rect(draw, [RX+20, 65, RX+680, 120], 8, fill=(22,16,38), outline=ACCENT, width=2)
    draw.text((RX+30, 74), "TRACE: research-query-abc123", font=font_head, fill=ACCENT2)
    draw.text((RX+30, 94), "Total: $0.42  ·  Latency: 47.3s  ·  4 stages  ·  prompt v12", font=font_small, fill=TEXT_DIM)

    # Sub-agents
    stages = [
        ("Data Scout", "28 tool calls · 22 data sources · $0.04", TEAL, (8,28,26)),
        ("Analyst", "3 LLM calls · statistical analysis · $0.08", PURPLE, (18,12,36)),
        ("Synthesizer", "Claude Opus 5 · 12k tokens · $0.22", ACCENT, (30,18,8)),
        ("Critic [PASS]", "Opus 5 · factuality=0.91 · $0.08", GREEN, (8,28,14)),
    ]

    sy = 138
    for name, detail, color, bg in stages:
        rounded_rect(draw, [RX+40, sy, RX+665, sy+58], 6, fill=bg, outline=color, width=1)
        draw.line([(RX+40, sy), (RX+40, sy+58)], fill=color, width=3)
        draw.text((RX+52, sy+8), name, font=font_head, fill=color)
        draw.text((RX+52, sy+30), detail, font=font_small, fill=TEXT_DIM)
        sy += 68

    # Prompt management panel
    rounded_rect(draw, [RX+20, sy+6, RX+680, sy+80], 8, fill=BOX_BG, outline=(90, 60, 150), width=1)
    draw.text((RX+30, sy+14), "Prompt Management:", font=load_font_ttc(13, index=1), fill=(180, 140, 240))
    draw.text((RX+30, sy+34), "• system-prompt-v12 (production label) · cached · 8,900 tokens", font=font_small, fill=TEXT_DIM)
    draw.text((RX+30, sy+52), "• prompt update → UI change only · no pod restart needed", font=font_small, fill=TEXT_DIM)

    # Evaluation panel
    rounded_rect(draw, [RX+20, sy+92, RX+680, sy+158], 8, fill=(8, 24, 10), outline=GREEN, width=1)
    draw.text((RX+30, sy+100), "Evaluation Scores:", font=load_font_ttc(13, index=1), fill=(100, 220, 130))
    draw.text((RX+30, sy+120), "• factual_coherence: 0.91  ·  source_citation: 0.87  ·  relevance: 0.94", font=font_small, fill=TEXT_DIM)
    draw.text((RX+30, sy+140), "• scored by LLM-as-a-Judge (Haiku) · async, zero added latency", font=font_small, fill=TEXT_DIM)

    img.save(os.path.join(OUTPUT_DIR, "23-langfuse-llm-observability.png"))
    print("✓ cover 23 langfuse")

cover_23_langfuse()

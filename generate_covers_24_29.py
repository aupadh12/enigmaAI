"""Cover generator for blog posts #24–#29.
Modelled on generate_cover_langfuse.py — same 1200x627, same font/layout conventions.
One distinct accent colour and simple motif per post.
No internal names, IDs, or company-specific text in cover images.
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "/Users/aupadh12/Desktop/Ashutosh_work/Blog_contents/enigmaAI/blogposts/covers"

# ── Font helpers ──────────────────────────────────────────────────────────────

def load_font_ttc(size, index=0):
    try:
        return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=index)
    except Exception:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except Exception:
            return ImageFont.load_default()

# ── Drawing helpers ────────────────────────────────────────────────────────────

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

def draw_badge(draw, label, x, y, accent, font):
    bb = draw.textbbox((0, 0), label, font=font)
    bw = bb[2] - bb[0] + 28
    bh = bb[3] - bb[1] + 14
    rounded_rect(draw, [x, y, x + bw, y + bh], 20, fill=accent)
    draw.text((x + 14, y + 7), label, font=font, fill=(255, 255, 255))
    return bw, bh

def base_canvas(W=1200, H=627, bg=(8, 6, 20), split_x=430):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    for i in range(H):
        t = i / H
        draw.line([(0, i), (W, i)],
                  fill=(int(bg[0] + 6 * t), int(bg[1] + 5 * t), int(bg[2] + 18 * t)))
    draw.rectangle([split_x, 0, W, H], fill=(10, 8, 26))
    return img, draw

def author_line(draw, W, H, accent, label_font, tiny_font):
    y = H - 52
    ax, ar = 28, 18
    draw.ellipse([ax, y, ax + ar * 2, y + ar * 2], fill=accent)
    text_center(draw, "A", ax + ar, y + ar - 8, load_font_ttc(15, index=1), (255, 255, 255))
    draw.text((ax + ar * 2 + 10, y + 2), "Ashutosh Upadhyay",
              font=label_font, fill=(230, 230, 230))
    draw.text((ax + ar * 2 + 10, y + 20), "Platform Engineering",
              font=tiny_font, fill=(150, 150, 160))


# ── #24 — Memory Self-Poisoning ───────────────────────────────────────────────
# Accent: crimson-red (poisoned state)
def cover_24():
    W, H = 1200, 627
    img, draw = base_canvas()

    ACCENT  = (220, 38,  60)   # crimson
    ACCENT2 = (252, 110, 120)
    DIM     = (145, 138, 175)
    BOX_BG  = (20, 6, 12)
    GREEN   = (74, 222, 128)
    YELLOW  = (250, 204, 21)

    f_badge = load_font_ttc(11, index=1)
    f_tiny  = load_font_ttc(11)
    f_small = load_font_ttc(13)
    f_head  = load_font_ttc(15, index=1)
    f_stat  = load_font_ttc(30, index=1)

    draw_badge(draw, "MEMORY", 44, 54, ACCENT, f_badge)
    draw.text((44, 108), "Memory That", font=load_font_ttc(40, index=1), fill=(235, 240, 255))
    draw.text((44, 158), "Poisons Itself", font=load_font_ttc(36, index=1), fill=ACCENT2)
    draw.text((44, 204), "Self-Poisoning in", font=load_font_ttc(26, index=1), fill=(200, 215, 255))
    draw.text((44, 238), "Long-Term Agent Memory", font=load_font_ttc(22, index=1), fill=(170, 185, 230))

    sub = "A hallucinated claim persisted as a behavioural rule, injected as the user's own voice, and the model obeyed it."
    wrap_text(draw, sub, 44, 282, 360, load_font_ttc(15), DIM)

    for val, lbl, sx in [("0.45", "RELEVANCE THRESHOLD", 44), ("0.85", "POISON CONFIDENCE", 185)]:
        draw.text((sx, 390), val, font=f_stat, fill=ACCENT)
        draw.text((sx, 428), lbl, font=load_font_ttc(10), fill=DIM)

    author_line(draw, W, H, ACCENT, load_font_ttc(14, index=1), f_tiny)

    # Right panel: feedback loop diagram
    RX = 460
    draw.text((RX + 20, 28), "MEMORY SELF-POISONING LOOP", font=load_font_ttc(12, index=1), fill=(160, 60, 60))

    steps = [
        ("HALLUCINATE", "agent invents a tool claim", ACCENT, BOX_BG),
        ("PERSIST", "stored unconditionally into memory", YELLOW, (24, 20, 4)),
        ("EXTRACT", "extracted as confidence-0.85 rule", (251, 146, 60), (28, 14, 4)),
        ("INJECT", "injected as user-voice at session start", ACCENT2, (28, 6, 10)),
        ("OBEY", "model obeys its own hallucination", GREEN, (8, 28, 14)),
    ]
    sy = 58
    for label, detail, color, bg in steps:
        rounded_rect(draw, [RX + 20, sy, RX + 680, sy + 56], 6, fill=bg, outline=color, width=1)
        draw.line([(RX + 20, sy), (RX + 20, sy + 56)], fill=color, width=3)
        draw.text((RX + 32, sy + 8), label, font=f_head, fill=color)
        draw.text((RX + 32, sy + 30), detail, font=f_small, fill=DIM)
        if sy + 56 < 570:
            draw.line([(RX + 350, sy + 56), (RX + 350, sy + 70)], fill=(60, 50, 80), width=1)
            draw.polygon([(RX+344, sy+68), (RX+356, sy+68), (RX+350, sy+74)], fill=(60, 50, 80))
        sy += 76

    # Fix banner
    rounded_rect(draw, [RX + 20, sy + 4, RX + 680, sy + 52], 8,
                 fill=(8, 28, 14), outline=GREEN, width=1)
    draw.text((RX + 30, sy + 12), "FIX: tool-success gate + delete record AND source event",
              font=load_font_ttc(12, index=1), fill=GREEN)
    draw.text((RX + 30, sy + 32), "provenance label · admin purge endpoints", font=f_small, fill=DIM)

    img.save(os.path.join(OUTPUT_DIR, "24-agent-memory-self-poisoning.png"))
    print("✓ cover 24 — agent-memory-self-poisoning")


# ── #25 — Context Overflow In-Flight ─────────────────────────────────────────
# Accent: electric-blue (in-flight / stream)
def cover_25():
    W, H = 1200, 627
    img, draw = base_canvas(bg=(6, 8, 22))

    ACCENT  = (56, 189, 248)   # sky-blue
    ACCENT2 = (125, 211, 252)
    DIM     = (140, 148, 178)
    ORANGE  = (251, 146, 60)
    GREEN   = (74, 222, 128)
    RED     = (248, 113, 113)

    f_badge = load_font_ttc(11, index=1)
    f_tiny  = load_font_ttc(11)
    f_small = load_font_ttc(13)
    f_head  = load_font_ttc(15, index=1)

    draw_badge(draw, "AGENTIC AI", 44, 54, ACCENT, f_badge)
    draw.text((44, 108), "The Overflow",    font=load_font_ttc(40, index=1), fill=(235, 240, 255))
    draw.text((44, 158), "Was Not Here",    font=load_font_ttc(36, index=1), fill=ACCENT2)
    draw.text((44, 204), "Context Window Accumulation", font=load_font_ttc(22, index=1), fill=(200, 215, 255))
    draw.text((44, 236), "in Long Agentic Loops",       font=load_font_ttc(20, index=1), fill=(170, 185, 230))

    sub = "Suspected loaded history. Measurement proved otherwise. Here is the real cause and the conversation-manager trade-offs."
    wrap_text(draw, sub, 44, 278, 360, load_font_ttc(15), DIM)

    for val, lbl, sx in [("268KB", "MAX LOADED HIST", 44), ("300KB", "DYNAMO CAP", 196), ("~80", "TOOL CALLS", 316)]:
        draw.text((sx, 390), val, font=load_font_ttc(28, index=1), fill=ACCENT)
        draw.text((sx, 426), lbl, font=load_font_ttc(10), fill=DIM)

    author_line(draw, W, H, ACCENT, load_font_ttc(14, index=1), f_tiny)

    # Right panel: where the bytes accumulate
    RX = 460
    draw.text((RX + 20, 28), "WHERE THE BYTES ACTUALLY LIVE", font=load_font_ttc(12, index=1), fill=(30, 120, 180))

    bars = [
        ("Loaded history", 268, 300, ACCENT, "(max 268 KB stored vs 300 KB DynamoDB cap)"),
    ]
    BARY = 80
    BAR_MAX_W = 560
    for label, val, cap, color, note in bars:
        draw.text((RX + 20, BARY), label, font=f_head, fill=(220, 230, 255))
        filled_w = int(BAR_MAX_W * min(val, cap) / cap)
        rounded_rect(draw, [RX + 20, BARY + 22, RX + 20 + BAR_MAX_W, BARY + 42],
                     4, fill=(20, 18, 38))
        if filled_w > 0:
            rounded_rect(draw, [RX + 20, BARY + 22, RX + 20 + filled_w, BARY + 42],
                         4, fill=color)
        draw.text((RX + 20, BARY + 46), note, font=f_small, fill=DIM)
        BARY += 80

    # Manager comparison
    sy = BARY + 10
    rounded_rect(draw, [RX + 20, sy, RX + 680, sy + 90], 8, fill=(8, 18, 30), outline=ACCENT, width=1)
    draw.text((RX + 30, sy + 10), "Cap-tool-results-only manager:", font=f_head, fill=ACCENT2)
    draw.text((RX + 30, sy + 34), "• Stops quadratic re-billing (NullConversationManager)", font=f_small, fill=DIM)
    draw.text((RX + 30, sy + 52), "• Preserves delta-slice anchor (avoid window corruption)", font=f_small, fill=DIM)
    draw.text((RX + 30, sy + 70), "• Capture tool results at the event, not after the fact", font=f_small, fill=GREEN)

    img.save(os.path.join(OUTPUT_DIR, "25-agent-context-overflow-in-flight.png"))
    print("✓ cover 25 — agent-context-overflow-in-flight")


# ── #26 — Silent Wrong Data ───────────────────────────────────────────────────
# Accent: amber-yellow (silent corruption, warning)
def cover_26():
    W, H = 1200, 627
    img, draw = base_canvas(bg=(12, 10, 6))

    ACCENT  = (245, 158, 11)   # amber
    ACCENT2 = (252, 211, 77)
    DIM     = (155, 145, 130)
    RED     = (248, 113, 113)
    GREEN   = (74, 222, 128)
    TEAL    = (45, 212, 191)

    f_badge = load_font_ttc(11, index=1)
    f_tiny  = load_font_ttc(11)
    f_small = load_font_ttc(13)
    f_head  = load_font_ttc(14, index=1)

    draw_badge(draw, "DATA ENGINEERING", 44, 54, ACCENT, f_badge)
    draw.text((44, 108), "Silent Wrong",   font=load_font_ttc(40, index=1), fill=(235, 240, 255))
    draw.text((44, 158), "Data",           font=load_font_ttc(36, index=1), fill=ACCENT2)
    draw.text((44, 204), "Eight ways a pipeline lied", font=load_font_ttc(22, index=1), fill=(200, 215, 255))
    draw.text((44, 236), "without a single visible error",   font=load_font_ttc(20, index=1), fill=(170, 185, 230))

    sub = "None of these failures surfaced an error. No alert — just quietly wrong answers delivered with full confidence."
    wrap_text(draw, sub, 44, 278, 360, load_font_ttc(15), DIM)

    for val, lbl, sx in [("8", "SILENT FAILURES", 44), ("0", "ERRORS SURFACED", 168), ("0", "ALERTS FIRED", 316)]:
        draw.text((sx, 390), val, font=load_font_ttc(34, index=1), fill=ACCENT)
        draw.text((sx, 432), lbl, font=load_font_ttc(10), fill=DIM)

    author_line(draw, W, H, ACCENT, load_font_ttc(14, index=1), f_tiny)

    # Right panel: 8 failure pills
    RX = 460
    draw.text((RX + 20, 22), "EIGHT FAILURE MODES — ALL SILENT", font=load_font_ttc(12, index=1), fill=(160, 120, 20))

    failures = [
        (".upper() erased the only discriminator (79 collisions)", RED),
        ("Guessed enum -> 44% rows to wrong default", RED),
        ("2 of 3 inferred extractors were defective", ACCENT),
        ("BCL2L->BCL2 was wrong (should be BCL2L1)", ACCENT),
        ("Accession = child element, not attribute -> blank join key", ACCENT),
        ("Counter measured writes, not distinct entities", TEAL),
        ("entity_id missing type prefix -> unfindable nodes", TEAL),
        ("Null potency metric silently dropped records", GREEN),
    ]
    fy = 58
    for text, color in failures:
        rounded_rect(draw, [RX + 20, fy, RX + 680, fy + 36], 6, fill=(18, 16, 10), outline=color, width=1)
        draw.line([(RX + 20, fy), (RX + 20, fy + 36)], fill=color, width=3)
        draw.text((RX + 30, fy + 10), text, font=f_small, fill=(210, 205, 195))
        fy += 44

    img.save(os.path.join(OUTPUT_DIR, "26-silent-wrong-data-agent-pipelines.png"))
    print("✓ cover 26 — silent-wrong-data-agent-pipelines")


# ── #27 — FinOps Silent Day Loss ──────────────────────────────────────────────
# Accent: teal/cyan (cost data, financial)
def cover_27():
    W, H = 1200, 627
    img, draw = base_canvas(bg=(6, 12, 14))

    ACCENT  = (20, 184, 166)   # teal
    ACCENT2 = (94, 234, 212)
    DIM     = (130, 155, 155)
    RED     = (248, 113, 113)
    ORANGE  = (251, 146, 60)
    YELLOW  = (250, 204, 21)

    f_badge = load_font_ttc(11, index=1)
    f_tiny  = load_font_ttc(11)
    f_small = load_font_ttc(13)
    f_head  = load_font_ttc(14, index=1)

    draw_badge(draw, "FINOPS", 44, 54, ACCENT, f_badge)
    draw.text((44, 108), "One Missing Key",  font=load_font_ttc(38, index=1), fill=(235, 240, 255))
    draw.text((44, 156), "Deleted Three",    font=load_font_ttc(34, index=1), fill=ACCENT2)
    draw.text((44, 200), "Days of Cost Data",font=load_font_ttc(28, index=1), fill=(200, 215, 255))

    sub = "A recognised-but-incomplete pricing entry is more dangerous than an unknown model. Here is how a KeyError inside a callback quietly discarded whole days."
    wrap_text(draw, sub, 44, 256, 360, load_font_ttc(14), DIM)

    draw.text((44, 390), "3", font=load_font_ttc(36, index=1), fill=RED)
    draw.text((44, 432), "DAYS LOST", font=load_font_ttc(10), fill=DIM)
    # "KeyError" at size 28 ends ~x=228; "-> recovered" starts at x=250 with room to spare
    draw.text((100, 390), "KeyError", font=load_font_ttc(28, index=1), fill=RED)
    draw.text((100, 432), "SILENT CAUSE", font=load_font_ttc(10), fill=DIM)
    draw.text((280, 390), "-> recovered", font=load_font_ttc(18, index=1), fill=ACCENT)

    author_line(draw, W, H, ACCENT, load_font_ttc(14, index=1), f_tiny)

    # Right panel: failure chain
    RX = 460
    draw.text((RX + 20, 22), "HOW THREE DAYS DISAPPEARED", font=load_font_ttc(12, index=1), fill=(20, 120, 110))

    chain = [
        ("Partial pricing entry in registry", RED, "(recognised but incomplete)"),
        ("KeyError inside pagination callback", RED, "(exception swallowed by blanket except)"),
        ("'query failed' — whole day discarded", ORANGE, "(no per-day retry, no alert)"),
        ("Summary log line said: success", YELLOW, "(lied — day count was decremented)"),
        ("extracted_at date == date -> detect truncation", ACCENT2, "(flanked-by-events test)"),
        ("_drop_incomplete_rates() + recovery runs", ACCENT, "(conservation checks before commit)"),
    ]
    cy = 58
    for label, color, note in chain:
        rounded_rect(draw, [RX + 20, cy, RX + 680, cy + 52], 6, fill=(8, 18, 20), outline=color, width=1)
        draw.line([(RX + 20, cy), (RX + 20, cy + 52)], fill=color, width=3)
        draw.text((RX + 32, cy + 6), label, font=f_head, fill=color)
        draw.text((RX + 32, cy + 28), note, font=f_small, fill=DIM)
        if cy + 52 < 540:
            draw.line([(RX + 350, cy + 52), (RX + 350, cy + 60)], fill=(40, 70, 68), width=1)
            draw.polygon([(RX+344, cy+58), (RX+356, cy+58), (RX+350, cy+64)], fill=(40, 70, 68))
        cy += 68

    img.save(os.path.join(OUTPUT_DIR, "27-finops-pipeline-silent-day-loss.png"))
    print("✓ cover 27 — finops-pipeline-silent-day-loss")


# ── #28 — Opus 5 Bedrock Migration ───────────────────────────────────────────
# Accent: violet/purple (LLM platform upgrade)
def cover_28():
    W, H = 1200, 627
    img, draw = base_canvas(bg=(10, 6, 20))

    ACCENT  = (167, 139, 250)  # violet
    ACCENT2 = (196, 181, 253)
    DIM     = (145, 138, 175)
    TEAL    = (45, 212, 191)
    ORANGE  = (251, 146, 60)
    RED     = (248, 113, 113)
    GREEN   = (74, 222, 128)

    f_badge = load_font_ttc(11, index=1)
    f_tiny  = load_font_ttc(11)
    f_small = load_font_ttc(13)
    f_head  = load_font_ttc(14, index=1)

    draw_badge(draw, "LLM PLATFORM", 44, 54, ACCENT, f_badge)
    draw.text((44, 108), "Upgrading to",   font=load_font_ttc(38, index=1), fill=(235, 240, 255))
    draw.text((44, 156), "Opus 5",         font=load_font_ttc(40, index=1), fill=ACCENT2)
    draw.text((44, 204), "on Amazon Bedrock", font=load_font_ttc(24, index=1), fill=(200, 215, 255))
    draw.text((44, 238), "Eight Gotchas We Hit", font=load_font_ttc(20, index=1), fill=(170, 185, 230))

    sub = "Billed for a full response, parsed an empty string. A 400 misread as 'model unavailable.' Thinking that burns max_tokens before the answer starts."
    wrap_text(draw, sub, 44, 282, 360, load_font_ttc(14), DIM)

    author_line(draw, W, H, ACCENT, load_font_ttc(14, index=1), f_tiny)

    # Right panel: gotchas grid
    RX = 460
    draw.text((RX + 20, 22), "EIGHT MIGRATION GOTCHAS", font=load_font_ttc(12, index=1), fill=(100, 70, 180))

    gotchas = [
        ("content[0] = thinking block, not text", RED, "billed and discarded on intermittent adaptive thinking"),
        ("400 != 'model unavailable'", RED, "sampling params rejected; misclassified as downgrade trigger"),
        ("Thinking bills against max_tokens", ORANGE, "effort alone -> plausible truncated text; raise ceiling"),
        ("stop_reason check is not optional", ORANGE, "always inspect stop_reason before consuming content"),
        ("global. profiles reject dated snapshots", ACCENT, "effort nests under output_config, not top-level"),
        ("boto3 floor: >= 1.40 required", ACCENT2, "silent API failures on older SDK versions"),
        ("CacheConfig strategy='auto'", TEAL, "CacheToolsConfig ttl='1h'; TTL ordering matters"),
        ("Static system prompt = cross-user hits", GREEN, "per-session prefix breaks shared cache"),
    ]
    gy = 58
    for label, color, note in gotchas:
        rounded_rect(draw, [RX + 20, gy, RX + 680, gy + 50], 5, fill=(14, 10, 28), outline=color, width=1)
        draw.line([(RX + 20, gy), (RX + 20, gy + 50)], fill=color, width=3)
        draw.text((RX + 32, gy + 5), label, font=f_head, fill=color)
        draw.text((RX + 32, gy + 27), note, font=f_small, fill=DIM)
        gy += 58

    img.save(os.path.join(OUTPUT_DIR, "28-opus-5-bedrock-migration.png"))
    print("✓ cover 28 — opus-5-bedrock-migration")


# ── #29 — AI Coding Assistant Analytics ──────────────────────────────────────
# Accent: green (developer productivity / adoption metrics)
def cover_29():
    W, H = 1200, 627
    img, draw = base_canvas(bg=(6, 14, 8))

    ACCENT  = (34, 197, 94)    # green
    ACCENT2 = (134, 239, 172)
    DIM     = (130, 155, 130)
    TEAL    = (45, 212, 191)
    BLUE    = (96, 165, 250)
    YELLOW  = (250, 204, 21)
    ORANGE  = (251, 146, 60)

    f_badge = load_font_ttc(11, index=1)
    f_tiny  = load_font_ttc(11)
    f_small = load_font_ttc(13)
    f_head  = load_font_ttc(14, index=1)

    draw_badge(draw, "FINOPS", 44, 54, ACCENT, f_badge)
    draw.text((44, 108), "Measuring AI",     font=load_font_ttc(38, index=1), fill=(235, 240, 255))
    draw.text((44, 156), "Coding Tool",      font=load_font_ttc(36, index=1), fill=ACCENT2)
    draw.text((44, 200), "Adoption",         font=load_font_ttc(34, index=1), fill=(200, 215, 255))

    sub = "Two tools, two telemetry shapes — cost attribution, daily credits, and why group coverage is not licence utilisation."
    wrap_text(draw, sub, 44, 260, 360, load_font_ttc(15), DIM)

    # "identity+" is wide — use size 22 so it does not overlap the second stat
    draw.text((44, 390), "identity+", font=load_font_ttc(22, index=1), fill=ACCENT)
    draw.text((44, 422), "MODEL+TOKENS", font=load_font_ttc(10), fill=DIM)
    draw.text((230, 390), "daily", font=load_font_ttc(28, index=1), fill=ACCENT)
    draw.text((230, 422), "NOT CUMULATIVE", font=load_font_ttc(10), fill=DIM)

    author_line(draw, W, H, ACCENT, load_font_ttc(14, index=1), f_tiny)

    # Right panel: telemetry comparison
    RX = 460
    draw.text((RX + 20, 22), "TWO TOOLS — TWO TELEMETRY SHAPES", font=load_font_ttc(12, index=1), fill=(20, 130, 60))

    # Claude Code panel
    rounded_rect(draw, [RX + 20, 50, RX + 680, 222], 8, fill=(8, 22, 10), outline=BLUE, width=1)
    draw.text((RX + 30, 60), "Claude Code on Bedrock", font=load_font_ttc(14, index=1), fill=BLUE)
    draw.text((RX + 30, 84), "Invocation log: identity + modelId + tokens in one record",
              font=f_small, fill=DIM)
    draw.text((RX + 30, 104), "-> per-user x per-model cost attribution for free",
              font=f_small, fill=ACCENT2)
    draw.text((RX + 30, 124), "Cost Explorer 'Amazon Bedrock' line ~= $0",
              font=f_small, fill=DIM)
    draw.text((RX + 30, 144), "-> spend is under per-model '(Amazon Bedrock Edition)' lines",
              font=f_small, fill=ACCENT2)
    draw.text((RX + 30, 164), "Onboarding trap: username-prefix casing is case-sensitive",
              font=f_small, fill=ORANGE)
    draw.text((RX + 30, 184), "Confirm invocation logging is already on before deploying",
              font=f_small, fill=(180, 180, 180))

    # Kiro panel
    rounded_rect(draw, [RX + 20, 234, RX + 680, 384], 8, fill=(8, 22, 10), outline=TEAL, width=1)
    draw.text((RX + 30, 244), "Kiro", font=load_font_ttc(14, index=1), fill=TEAL)
    draw.text((RX + 30, 268), "Credits: daily buckets, not cumulative",
              font=f_small, fill=DIM)
    draw.text((RX + 30, 288), "-> overage cap must scale: max(1, round(days/30))",
              font=f_small, fill=ACCENT2)
    draw.text((RX + 30, 308), "Group coverage != licence utilisation",
              font=f_head, fill=YELLOW)
    draw.text((RX + 30, 332), "-> users spending outside any group = denominator is wrong",
              font=f_small, fill=DIM)
    draw.text((RX + 30, 352), "-> 'no group' bucket required for correct accounting",
              font=f_small, fill=ACCENT2)

    # Key lesson
    rounded_rect(draw, [RX + 20, 396, RX + 680, 466], 8, fill=(8, 28, 14), outline=ACCENT, width=1)
    draw.text((RX + 30, 406), "Lesson: the telemetry shape determines what you can measure.",
              font=f_head, fill=ACCENT2)
    draw.text((RX + 30, 430), "Choose your data model before you choose your dashboard.",
              font=f_small, fill=DIM)

    img.save(os.path.join(OUTPUT_DIR, "29-ai-coding-assistant-usage-analytics.png"))
    print("✓ cover 29 — ai-coding-assistant-usage-analytics")


# ── Run all ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cover_24()
    cover_25()
    cover_26()
    cover_27()
    cover_28()
    cover_29()
    print("\nAll 6 covers generated.")

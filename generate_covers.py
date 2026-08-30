"""
Cover image generator for enigmaAI blog posts.
Generates 1200x627 PNG covers matching the existing style.
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys

OUTPUT_DIR = "/Users/aupadh12/Desktop/Ashutosh_work/Blog_contents/enigmaAI/blogposts/covers"

# ──────────────────────────────────────────────
# Font helpers
# ──────────────────────────────────────────────

def load_font(size, bold=False):
    candidates = [
        f"/System/Library/Fonts/{'HelveticaNeue-Bold.ttf' if bold else 'HelveticaNeue.ttf'}",
        f"/System/Library/Fonts/{'HelveticaNeue-Bold' if bold else 'HelveticaNeue'}",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass
    return ImageFont.load_default()

def load_font_ttc(size, index=0):
    try:
        return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=index)
    except:
        return load_font(size)

# ──────────────────────────────────────────────
# Drawing primitives
# ──────────────────────────────────────────────

def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, x0, y0, x1, y1, color, width=2, head=8):
    """Draw a line with an arrowhead pointing toward (x1,y1)."""
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    import math
    angle = math.atan2(y1 - y0, x1 - x0)
    for side in (+0.5, -0.5):
        ax = x1 - head * math.cos(angle - side)
        ay = y1 - head * math.sin(angle - side)
        draw.line([(x1, y1), (ax, ay)], fill=color, width=width)

def text_center(draw, text, cx, y, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    w = bb[2] - bb[0]
    draw.text((cx - w // 2, y), text, font=font, fill=fill)

def text_right(draw, text, rx, y, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    w = bb[2] - bb[0]
    draw.text((rx - w, y), text, font=font, fill=fill)

def wrap_text(draw, text, x, y, max_width, font, fill, line_height=None):
    """Draw word-wrapped text, return final y."""
    if line_height is None:
        bb = draw.textbbox((0, 0), "Ag", font=font)
        line_height = (bb[3] - bb[1]) + 6
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
                y += line_height
            line = word
    if line:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y

def badge(draw, text, x, y, bg, fg, font):
    bb = draw.textbbox((0, 0), text, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    pad_x, pad_y = 14, 7
    rounded_rect(draw, [x, y, x + w + pad_x * 2, y + h + pad_y * 2], radius=20, fill=bg)
    draw.text((x + pad_x, y + pad_y), text, font=font, fill=fg)
    return y + h + pad_y * 2

def author_block(draw, img_w, img_h, accent):
    """Draw author row at bottom-left."""
    y = img_h - 52
    # Circle avatar
    ax, ay, ar = 28, y, 18
    draw.ellipse([ax, ay, ax + ar * 2, ay + ar * 2], fill=accent)
    font_av = load_font_ttc(15, index=1)
    text_center(draw, "A", ax + ar, ay + ar - 8, font_av, (255, 255, 255))
    # Name + role
    font_name = load_font_ttc(14, index=1)
    font_role = load_font_ttc(13)
    draw.text((ax + ar * 2 + 10, y + 2), "Ashutosh Upadhyay", font=font_name, fill=(230, 230, 230))
    draw.text((ax + ar * 2 + 10, y + 20), "Platform Engineering, J&J Innovative Medicine", font=font_role, fill=(150, 150, 160))

def tags_block(draw, tags, img_w, img_h, accent):
    """Draw tag pills at bottom-right."""
    font = load_font_ttc(12)
    x = img_w - 20
    y = img_h - 38
    for tag in reversed(tags):
        bb = draw.textbbox((0, 0), tag, font=font)
        tw = bb[2] - bb[0] + 20
        rounded_rect(draw, [x - tw, y, x, y + 26], radius=13, fill=(40, 40, 60), outline=(80, 80, 110), width=1)
        draw.text((x - tw + 10, y + 5), tag, font=font, fill=(190, 190, 210))
        x -= tw + 8


# ──────────────────────────────────────────────
# Cover 18: DataSync Cross-Account S3
# ──────────────────────────────────────────────

def cover_18():
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), (8, 14, 28))
    draw = ImageDraw.Draw(img)

    # Background gradient effect (horizontal bands)
    for i in range(H):
        t = i / H
        r = int(8 + 4 * t)
        g = int(14 + 8 * t)
        b = int(28 + 18 * t)
        draw.line([(0, i), (W, i)], fill=(r, g, b))

    # Right diagram area (subtle highlight)
    draw.rectangle([430, 0, W, H], fill=(10, 18, 36))

    ACCENT = (0, 196, 180)     # teal
    ACCENT2 = (0, 230, 200)
    BOX_BG = (15, 28, 52)
    BOX_BORDER = (0, 150, 140)
    ERR_BG = (40, 15, 15)
    ERR_BORDER = (200, 60, 60)
    SUCCESS_BG = (10, 40, 25)
    SUCCESS_BORDER = (30, 160, 90)
    TEXT_DIM = (140, 155, 175)

    font_tiny  = load_font_ttc(11)
    font_small = load_font_ttc(13)
    font_med   = load_font_ttc(14)
    font_head  = load_font_ttc(15, index=1)
    font_title = load_font_ttc(38, index=1)
    font_sub   = load_font_ttc(16)
    font_badge = load_font_ttc(11, index=1)
    font_stat  = load_font_ttc(30, index=1)
    font_stat_lbl = load_font_ttc(11)
    font_diag_title = load_font_ttc(12, index=1)

    # ---- LEFT SIDE ----
    badge(draw, "DATA ENGINEERING", 44, 54, ACCENT, (0, 0, 0), font_badge)

    # Title with highlighted word
    y_title = 108
    draw.text((44, y_title), "AWS DataSync:", font=load_font_ttc(40, index=1), fill=(235, 240, 255))
    draw.text((44, y_title + 52), "S3 Cross-Account Transfer", font=load_font_ttc(32, index=1), fill=ACCENT2)
    draw.text((44, y_title + 96), "Without the Surprises", font=load_font_ttc(32, index=1), fill=(200, 210, 230))

    # Subtitle
    sub = "Console can't see the bucket. Role goes in the destination account. KMS is always the first thing that breaks."
    y_sub = y_title + 152
    wrap_text(draw, sub, 44, y_sub, 360, font_sub, TEXT_DIM)

    # Stats
    y_stats = 380
    for val, lbl, sx in [("2", "ACCOUNTS", 44), ("6", "SETUP STEPS", 130), ("3", "KMS GOTCHAS", 228)]:
        draw.text((sx, y_stats), val, font=font_stat, fill=ACCENT)
        draw.text((sx, y_stats + 38), lbl, font=font_stat_lbl, fill=TEXT_DIM)

    # Author + tags
    author_block(draw, W, H, ACCENT)
    tags_block(draw, ["DataSync", "S3", "Cross-Account", "IAM"], W, H, ACCENT)

    # ---- RIGHT SIDE DIAGRAM ----
    RX = 460  # diagram left edge
    DW = 700  # diagram total width available

    # Diagram title
    draw.text((RX + 50, 28), "CROSS-ACCOUNT S3 TRANSFER — IAM TRUST CHAIN", font=font_diag_title, fill=(100, 130, 160))

    # Account A box (large, left of diagram)
    ax0, ay0, ax1, ay1 = RX + 20, 80, RX + 300, 420
    rounded_rect(draw, [ax0, ay0, ax1, ay1], 10, fill=(12, 22, 44), outline=(50, 80, 120), width=1)
    draw.text((ax0 + 12, ay0 + 12), "ACCOUNT A  (DataSync + Destination)", font=load_font_ttc(11, index=1), fill=(80, 120, 180))

    # DataSync Task box
    rounded_rect(draw, [ax0+20, ay0+40, ax1-20, ay0+100], 8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    text_center(draw, "DataSync Task", (ax0+ax1)//2, ay0+50, font_head, (220,235,255))
    text_center(draw, "runs in Account A", (ax0+ax1)//2, ay0+72, font_small, TEXT_DIM)

    # IAM Role box
    rounded_rect(draw, [ax0+20, ay0+120, ax1-20, ay0+185], 8, fill=BOX_BG, outline=ACCENT, width=1)
    text_center(draw, "IAM Role: DataSyncS3Role", (ax0+ax1)//2, ay0+132, font_head, (220,235,255))
    text_center(draw, "trusted by datasync.amazonaws.com", (ax0+ax1)//2, ay0+155, font_small, TEXT_DIM)

    # Source Location box
    rounded_rect(draw, [ax0+20, ay0+205, ax1-20, ay0+260], 8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    text_center(draw, "Source Location", (ax0+ax1)//2, ay0+215, font_head, (220,235,255))
    text_center(draw, "→ Account B's bucket", (ax0+ax1)//2, ay0+237, font_small, ACCENT)

    # Dest Location box
    rounded_rect(draw, [ax0+20, ay0+280, ax1-20, ay0+335], 8, fill=SUCCESS_BG, outline=SUCCESS_BORDER, width=1)
    text_center(draw, "Dest Location", (ax0+ax1)//2, ay0+290, font_head, (200,240,215))
    text_center(draw, "→ Account A's bucket ✓", (ax0+ax1)//2, ay0+312, font_small, (100,210,140))

    # Account B box (right)
    bx0, by0, bx1, by1 = RX + 335, 140, RX + 670, 310
    rounded_rect(draw, [bx0, by0, bx1, by1], 10, fill=(22, 14, 34), outline=(80, 50, 120), width=1)
    draw.text((bx0 + 12, by0 + 12), "ACCOUNT B  (Source Only)", font=load_font_ttc(11, index=1), fill=(150, 100, 200))

    # S3 Source bucket
    rounded_rect(draw, [bx0+20, by0+40, bx1-20, by0+100], 8, fill=(28, 18, 44), outline=(100, 60, 160), width=1)
    text_center(draw, "S3 Bucket (source)", (bx0+bx1)//2, by0+52, font_head, (220,200,255))
    text_center(draw, "SSE-KMS encrypted", (bx0+bx1)//2, by0+74, font_small, TEXT_DIM)

    # Bucket policy box
    rounded_rect(draw, [bx0+20, by0+115, bx1-20, by0+155], 8, fill=(35, 20, 15), outline=(200, 130, 40), width=1)
    text_center(draw, "⚠  Bucket Policy: Step 3 — MANDATORY", (bx0+bx1)//2, by0+120, font_small, (240, 180, 80))
    text_center(draw, 'Grant Account A DataSync role read access', (bx0+bx1)//2, by0+138, font_tiny, TEXT_DIM)

    # Arrow: Source Location → Account B bucket
    draw_arrow(draw, ax1 - 20, ay0 + 230, bx0 + 20, by0 + 70, ACCENT, width=2)

    # KMS warning box
    rounded_rect(draw, [bx0, by0 + 175, bx1, by0 + 230], 8, fill=ERR_BG, outline=ERR_BORDER, width=1)
    text_center(draw, "KMS Key Policy — Most Common Failure", (bx0+bx1)//2, by0+183, font_small, (240,120,120))
    text_center(draw, "DataSync role needs kms:Decrypt in Account B", (bx0+bx1)//2, by0+203, font_tiny, TEXT_DIM)
    text_center(draw, "AND kms:GenerateDataKey in Account A", (bx0+bx1)//2, by0+218, font_tiny, TEXT_DIM)

    # Bottom note
    note_bg = (10, 28, 40)
    rounded_rect(draw, [RX + 20, 450, RX + 670, 510], 8, fill=note_bg, outline=(0, 130, 160), width=1)
    text_center(draw, "Key Rule: Run DataSync in the DESTINATION account.", (RX+20+RX+670)//2, 462, font_head, (200,240,255))
    text_center(draw, "CLI-only for cross-account source location — console can't see the bucket.", (RX+20+RX+670)//2, 484, font_small, TEXT_DIM)

    img.save(os.path.join(OUTPUT_DIR, "18-aws-datasync-cross-account-s3.png"))
    print("✓ cover 18")


# ──────────────────────────────────────────────
# Cover 19: IRSA + Cross-Account AssumeRole
# ──────────────────────────────────────────────

def cover_19():
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), (10, 10, 22))
    draw = ImageDraw.Draw(img)

    for i in range(H):
        t = i / H
        r = int(10 + 6 * t)
        g = int(10 + 5 * t)
        b = int(22 + 12 * t)
        draw.line([(0, i), (W, i)], fill=(r, g, b))

    draw.rectangle([430, 0, W, H], fill=(12, 12, 28))

    ACCENT = (245, 158, 11)   # amber
    ACCENT2 = (254, 200, 80)
    BOX_BG = (20, 20, 42)
    BOX_BORDER = (180, 130, 30)
    HOP1_COLOR = (100, 180, 255)
    HOP2_COLOR = (100, 220, 160)
    TEXT_DIM = (150, 150, 175)

    font_tiny  = load_font_ttc(11)
    font_small = load_font_ttc(13)
    font_med   = load_font_ttc(14)
    font_head  = load_font_ttc(15, index=1)
    font_badge = load_font_ttc(11, index=1)
    font_stat  = load_font_ttc(30, index=1)
    font_stat_lbl = load_font_ttc(11)
    font_diag_title = load_font_ttc(12, index=1)
    font_title = load_font_ttc(38, index=1)

    # ---- LEFT SIDE ----
    badge(draw, "IAM & IDENTITY", 44, 54, ACCENT, (0, 0, 0), font_badge)

    draw.text((44, 108), "The Two-Hop", font=load_font_ttc(42, index=1), fill=(235, 240, 255))
    draw.text((44, 160), "IAM Pattern:", font=load_font_ttc(36, index=1), fill=ACCENT2)
    draw.text((44, 210), "IRSA + Cross-Account", font=load_font_ttc(26, index=1), fill=(200, 210, 230))

    sub = "Hop 1: EKS pod gets IRSA credentials. Hop 2: assumes a role in a different account. Wire both correctly."
    wrap_text(draw, sub, 44, 270, 360, load_font_ttc(15), TEXT_DIM)

    y_stats = 370
    for val, lbl, sx in [("2", "HOPS", 44), ("N", "ACCOUNTS", 130), ("1h", "CRED TTL", 220)]:
        draw.text((sx, y_stats), val, font=font_stat, fill=ACCENT)
        draw.text((sx, y_stats + 38), lbl, font=font_stat_lbl, fill=TEXT_DIM)

    author_block(draw, W, H, ACCENT)
    tags_block(draw, ["IAM", "IRSA", "EKS", "STS"], W, H, ACCENT)

    # ---- RIGHT SIDE DIAGRAM ----
    RX = 460

    draw.text((RX + 30, 28), "IAM TRUST CHAIN — TWO-HOP CREDENTIAL FLOW", font=font_diag_title, fill=(120, 110, 60))

    # EKS Cluster
    rounded_rect(draw, [RX+20, 70, RX+310, 155], 10, fill=(14, 18, 36), outline=(60, 80, 160), width=1)
    draw.text((RX+32, 80), "EKS CLUSTER", font=load_font_ttc(11, index=1), fill=(80, 100, 200))
    rounded_rect(draw, [RX+40, 100, RX+290, 145], 6, fill=(20, 26, 50), outline=(50, 70, 140), width=1)
    text_center(draw, "Pod + ServiceAccount", (RX+40+RX+290)//2, 108, font_head, (200, 215, 255))
    text_center(draw, "eks.amazonaws.com/role-arn annotation", (RX+40+RX+290)//2, 127, font_tiny, TEXT_DIM)

    # Hop 1 label
    draw.text((RX + 330, 100), "HOP 1", font=load_font_ttc(11, index=1), fill=HOP1_COLOR)
    draw.text((RX + 320, 115), "OIDC Web", font=font_tiny, fill=HOP1_COLOR)
    draw.text((RX + 320, 129), "Identity", font=font_tiny, fill=HOP1_COLOR)

    # Arrow: Pod → IRSA Role
    draw_arrow(draw, RX+310, 110, RX+400, 110, HOP1_COLOR, width=2)

    # IRSA Role (home account)
    rounded_rect(draw, [RX+400, 70, RX+690, 160], 10, fill=(20, 30, 50), outline=(100, 160, 240), width=1)
    draw.text((RX+412, 78), "HOME ACCOUNT", font=load_font_ttc(11, index=1), fill=(80, 130, 220))
    rounded_rect(draw, [RX+418, 98, RX+672, 150], 6, fill=BOX_BG, outline=(80, 130, 220), width=1)
    text_center(draw, "IRSA Role", (RX+418+RX+672)//2, 106, font_head, (180, 210, 255))
    text_center(draw, "sts:AssumeRole → [TARGET_ACCOUNT_*/Role]", (RX+418+RX+672)//2, 126, font_tiny, ACCENT2)

    # Hop 2 labels + arrows to 3 target accounts
    targets = [
        ("TARGET ACCOUNT 1", "CloudWatch Logs role", (70, 140, 240), 190, 210),
        ("TARGET ACCOUNT 2", "S3 read role", (80, 200, 140), 310, 320),
        ("TARGET ACCOUNT 3", "DynamoDB role", (180, 100, 220), 430, 430),
    ]

    for label, perm, color, ybox, _yarrow in targets:
        bx0 = RX + 400
        bx1 = RX + 690
        by0 = ybox
        by1 = ybox + 68
        rounded_rect(draw, [bx0, by0, bx1, by1], 8, fill=(14, 22, 38), outline=color, width=1)
        draw.text((bx0 + 10, by0 + 8), label, font=load_font_ttc(11, index=1), fill=color)
        text_center(draw, "Trust: HOME_ACCOUNT/IRSARole", (bx0+bx1)//2, by0 + 28, font_tiny, TEXT_DIM)
        text_center(draw, f"Permissions: {perm}", (bx0+bx1)//2, by0 + 44, font_tiny, (160, 180, 200))

        # Arrow from IRSA role down to this account
        draw_arrow(draw, (bx0+bx1)//2, 160, (bx0+bx1)//2, by0, color, width=2)

    # HOP 2 label
    draw.text((RX + 540, 165), "HOP 2 — sts:AssumeRole", font=load_font_ttc(11, index=1), fill=HOP2_COLOR)

    # Credential cache note
    rounded_rect(draw, [RX+20, 190, RX+365, 295], 8, fill=(18, 28, 18), outline=(40, 160, 80), width=1)
    draw.text((RX+30, 200), "Credential Cache (per role_arn):", font=load_font_ttc(12, index=1), fill=(100, 200, 120))
    lines = [
        "• Assume role once, cache credentials",
        "• STS default TTL: 1 hour",
        "• Renew 5 min before expiry",
        "• One cache entry per (service, role, region)",
    ]
    cy = 220
    for l in lines:
        draw.text((RX+34, cy), l, font=font_tiny, fill=TEXT_DIM)
        cy += 16

    # Trust policy snippet
    rounded_rect(draw, [RX+20, 308, RX+365, 430], 8, fill=(14, 14, 30), outline=(70, 70, 110), width=1)
    draw.text((RX+30, 318), "Target account trust policy:", font=load_font_ttc(12, index=1), fill=(160, 160, 200))
    code_lines = [
        '"Principal": {',
        '  "AWS": "arn:aws:iam::',
        '    HOME_ACCOUNT:role/',
        '    IRSARole"',
        '},',
        '"Action": "sts:AssumeRole"',
    ]
    cy = 338
    for l in code_lines:
        draw.text((RX+34, cy), l, font=font_tiny, fill=(160, 220, 180))
        cy += 14

    img.save(os.path.join(OUTPUT_DIR, "19-irsa-cross-account-assumerole.png"))
    print("✓ cover 19")


# ──────────────────────────────────────────────
# Cover 20: ArgoCD Multi-Source Helm
# ──────────────────────────────────────────────

def cover_20():
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), (10, 8, 24))
    draw = ImageDraw.Draw(img)

    for i in range(H):
        t = i / H
        draw.line([(0, i), (W, i)], fill=(int(10+4*t), int(8+4*t), int(24+14*t)))

    draw.rectangle([430, 0, W, H], fill=(12, 10, 28))

    ACCENT = (129, 140, 248)   # indigo
    ACCENT2 = (165, 180, 255)
    BOX_BG = (18, 16, 40)
    BOX_BORDER = (90, 100, 200)
    TEXT_DIM = (150, 148, 180)
    GREEN = (72, 199, 142)

    font_tiny  = load_font_ttc(11)
    font_small = load_font_ttc(13)
    font_head  = load_font_ttc(15, index=1)
    font_badge = load_font_ttc(11, index=1)
    font_stat  = load_font_ttc(30, index=1)
    font_stat_lbl = load_font_ttc(11)
    font_diag_title = load_font_ttc(12, index=1)

    # ---- LEFT SIDE ----
    badge(draw, "GITOPS", 44, 54, ACCENT, (255, 255, 255), font_badge)

    draw.text((44, 108), "ArgoCD Multi-Source", font=load_font_ttc(36, index=1), fill=(235, 240, 255))
    draw.text((44, 156), "Helm: Separate the", font=load_font_ttc(30, index=1), fill=(210, 220, 255))
    draw.text((44, 200), "Chart from the Config", font=load_font_ttc(30, index=1), fill=ACCENT2)

    sub = "One source for the chart in your registry. One source for the values in Git. They version independently."
    wrap_text(draw, sub, 44, 256, 360, load_font_ttc(15), TEXT_DIM)

    y_stats = 370
    for val, lbl, sx in [("3", "GENERATORS", 44), ("50+", "APPS", 170), ("1", "ROOT DRIVER", 250)]:
        draw.text((sx, y_stats), val, font=font_stat, fill=ACCENT)
        draw.text((sx, y_stats + 38), lbl, font=font_stat_lbl, fill=TEXT_DIM)

    author_block(draw, W, H, ACCENT)
    tags_block(draw, ["ArgoCD", "Helm", "GitOps", "ApplicationSet"], W, H, ACCENT)

    # ---- RIGHT SIDE DIAGRAM ----
    RX = 460
    draw.text((RX+30, 28), "MULTI-SOURCE HELM — THREE APPLICATIONSET PATTERNS", font=font_diag_title, fill=(100, 95, 180))

    # Pattern boxes
    patterns = [
        ("Pattern 1: Static Application", "targetRevision: 1.2.3 (pinned)", "Production — explicit version bump", (60, 180, 120), (10, 40, 25)),
        ("Pattern 2: Prerelease Tag Plugin", 'targetRevision: {{ .highestTag }}', "Dev — auto-deploys latest beta", (200, 160, 40), (40, 30, 10)),
        ("Pattern 3: Pull Request Generator", "targetRevision: {{head_sha}}", "Ephemeral per-PR environments", (100, 140, 240), (14, 22, 50)),
    ]

    py = 80
    for title, version, desc, border, bg in patterns:
        bx0, bx1 = RX+20, RX+660
        rounded_rect(draw, [bx0, py, bx1, py+90], 8, fill=bg, outline=border, width=1)
        draw.text((bx0+14, py+10), title, font=font_head, fill=(220, 230, 255))
        draw.text((bx0+14, py+32), version, font=load_font_ttc(13), fill=border)
        draw.text((bx0+14, py+52), desc, font=font_small, fill=TEXT_DIM)
        # $values note
        draw.text((bx0+14, py+70), "valueFiles: $values/apps/my-app/values-*.yaml", font=font_tiny, fill=(120, 120, 160))
        py += 108

    # Separator
    draw.line([(RX+20, py+10), (RX+660, py+10)], fill=(40, 40, 60), width=1)

    # App of Apps
    rounded_rect(draw, [RX+20, py+22, RX+660, py+100], 10, fill=(18, 16, 40), outline=ACCENT, width=2)
    text_center(draw, "App of Apps — Root Driver Application", (RX+20+RX+660)//2, py+30, font_head, ACCENT2)
    text_center(draw, "Watches _scm_argocd/my-cluster/*.yaml", (RX+20+RX+660)//2, py+52, font_small, TEXT_DIM)
    text_center(draw, "Add YAML → commit → ArgoCD auto-deploys. No kubectl apply needed.", (RX+20+RX+660)//2, py+72, font_small, (180, 180, 210))

    # Rule callout
    rounded_rect(draw, [RX+20, py+112, RX+660, py+148], 6, fill=(12, 30, 20), outline=(40, 160, 80), width=1)
    text_center(draw, "Always use $values/ prefix in valueFiles — it references the declared ref: values source.", (RX+20+RX+660)//2, py+122, font_small, (100, 210, 140))
    text_center(draw, "Without it ArgoCD looks in the chart source and finds nothing.", (RX+20+RX+660)//2, py+140, font_tiny, TEXT_DIM)

    img.save(os.path.join(OUTPUT_DIR, "20-argocd-multisource-helm-gitops.png"))
    print("✓ cover 20")


# ──────────────────────────────────────────────
# Cover 21: Kargo GitOps Promotion
# ──────────────────────────────────────────────

def cover_21():
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), (8, 18, 12))
    draw = ImageDraw.Draw(img)

    for i in range(H):
        t = i / H
        draw.line([(0, i), (W, i)], fill=(int(8+4*t), int(18+6*t), int(12+6*t)))

    draw.rectangle([430, 0, W, H], fill=(10, 20, 14))

    ACCENT = (34, 197, 94)    # green
    ACCENT2 = (74, 222, 128)
    BOX_BG = (12, 30, 18)
    BOX_BORDER = (34, 160, 75)
    WARN = (250, 160, 50)
    TEXT_DIM = (140, 165, 148)

    font_tiny  = load_font_ttc(11)
    font_small = load_font_ttc(13)
    font_head  = load_font_ttc(15, index=1)
    font_badge = load_font_ttc(11, index=1)
    font_stat  = load_font_ttc(30, index=1)
    font_stat_lbl = load_font_ttc(11)
    font_diag_title = load_font_ttc(12, index=1)

    # ---- LEFT ----
    badge(draw, "GITOPS", 44, 54, ACCENT, (0, 0, 0), font_badge)

    draw.text((44, 108), "Kargo: GitOps", font=load_font_ttc(40, index=1), fill=(235, 245, 238))
    draw.text((44, 158), "Promotions That", font=load_font_ttc(34, index=1), fill=ACCENT2)
    draw.text((44, 204), "Don't Need Discipline", font=load_font_ttc(26, index=1), fill=(200, 220, 210))

    sub = "Manual promotions fail when they don't happen and when they happen wrong. Kargo automates the correct pattern."
    wrap_text(draw, sub, 44, 258, 360, load_font_ttc(15), TEXT_DIM)

    y_stats = 375
    for val, lbl, sx in [("3", "PRIMITIVES", 44), ("N", "STAGES", 165), ("0", "MANUAL EDITS", 238)]:
        draw.text((sx, y_stats), val, font=font_stat, fill=ACCENT)
        draw.text((sx, y_stats + 38), lbl, font=font_stat_lbl, fill=TEXT_DIM)

    author_block(draw, W, H, ACCENT)
    tags_block(draw, ["Kargo", "GitOps", "ArgoCD", "Release"], W, H, ACCENT)

    # ---- RIGHT DIAGRAM ----
    RX = 460
    draw.text((RX+30, 28), "WAREHOUSE → FREIGHT → STAGE PIPELINE", font=font_diag_title, fill=(60, 160, 80))

    # Warehouse
    wh_cx = RX + 100
    rounded_rect(draw, [RX+20, 70, RX+185, 150], 10, fill=(12, 32, 20), outline=ACCENT, width=2)
    text_center(draw, "Warehouse", wh_cx, 85, font_head, ACCENT2)
    text_center(draw, "Watches registry", wh_cx, 108, font_small, TEXT_DIM)
    text_center(draw, "for new images", wh_cx, 125, font_small, TEXT_DIM)

    # Freight
    fr_cx = RX + 295
    rounded_rect(draw, [RX+210, 70, RX+380, 150], 10, fill=(12, 32, 20), outline=ACCENT2, width=2)
    text_center(draw, "Freight", fr_cx, 85, font_head, (200, 245, 220))
    text_center(draw, "Immutable snapshot:", fr_cx, 108, font_small, TEXT_DIM)
    text_center(draw, "image SHA + tag", fr_cx, 125, font_small, TEXT_DIM)

    draw_arrow(draw, RX+185, 110, RX+210, 110, ACCENT, width=2)

    # Stage pipeline
    stages = [
        ("dev", "Auto-promote", ACCENT, BOX_BG),
        ("qa", "Auto-promote", ACCENT2, (10, 26, 16)),
        ("prod", "Manual gate ✓", WARN, (30, 20, 10)),
    ]

    sy_top = 200
    bw = 175
    bx = RX + 20
    for i, (name, policy, color, bg) in enumerate(stages):
        rounded_rect(draw, [bx, sy_top, bx+bw, sy_top+120], 10, fill=bg, outline=color, width=2)
        text_center(draw, name, bx+bw//2, sy_top+12, load_font_ttc(18, index=1), color)
        text_center(draw, policy, bx+bw//2, sy_top+42, font_small, (200, 210, 200))
        text_center(draw, "Kargo commits", bx+bw//2, sy_top+65, font_tiny, TEXT_DIM)
        text_center(draw, "values-" + name + ".yaml", bx+bw//2, sy_top+80, font_tiny, color)
        text_center(draw, "ArgoCD syncs", bx+bw//2, sy_top+98, font_tiny, TEXT_DIM)
        if i < 2:
            draw_arrow(draw, bx+bw, sy_top+60, bx+bw+20, sy_top+60, ACCENT, width=2)
        bx += bw + 20

    # What Kargo automates
    rounded_rect(draw, [RX+20, 350, RX+665, 440], 8, fill=(10, 22, 16), outline=(40, 120, 60), width=1)
    draw.text((RX+30, 360), "What Kargo automates:", font=load_font_ttc(13, index=1), fill=(100, 200, 130))
    items = [
        ("✗ Before", "Edit values file manually, decide which SHA to promote"),
        ("✓ After",  "Freight tracks exact SHA → Kargo commits → ArgoCD deploys"),
    ]
    iy = 382
    for prefix, text in items:
        c = (100, 210, 130) if "After" in prefix else (200, 100, 100)
        draw.text((RX+30, iy), prefix + ":", font=load_font_ttc(12, index=1), fill=c)
        draw.text((RX+100, iy), text, font=font_tiny, fill=TEXT_DIM)
        iy += 20

    # ArgoCD integration note
    rounded_rect(draw, [RX+20, 452, RX+665, 510], 6, fill=(10, 20, 14), outline=(30, 100, 50), width=1)
    text_center(draw, "Kargo integrates with ArgoCD — no duplicate configuration.", (RX+20+RX+665)//2, 464, font_head, (150, 220, 170))
    text_center(draw, "Set ARGOCD_INTEGRATION_ENABLED=true and point at your ArgoCD URL.", (RX+20+RX+665)//2, 486, font_small, TEXT_DIM)

    img.save(os.path.join(OUTPUT_DIR, "21-kargo-gitops-promotion-pipeline.png"))
    print("✓ cover 21")


# ──────────────────────────────────────────────
# Cover 22: Cross-Account CloudWatch Region Trap
# ──────────────────────────────────────────────

def cover_22():
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), (14, 8, 22))
    draw = ImageDraw.Draw(img)

    for i in range(H):
        t = i / H
        draw.line([(0, i), (W, i)], fill=(int(14+5*t), int(8+4*t), int(22+14*t)))

    draw.rectangle([430, 0, W, H], fill=(16, 10, 26))

    ACCENT = (56, 189, 248)    # sky blue
    ACCENT2 = (125, 211, 252)
    BOX_BG = (16, 18, 38)
    BOX_BORDER = (40, 140, 200)
    ERR_BG = (40, 10, 10)
    ERR_BORDER = (220, 60, 60)
    WARN_BG = (38, 26, 8)
    WARN_BORDER = (220, 160, 40)
    TEXT_DIM = (140, 148, 175)

    font_tiny  = load_font_ttc(11)
    font_small = load_font_ttc(13)
    font_head  = load_font_ttc(15, index=1)
    font_badge = load_font_ttc(11, index=1)
    font_stat  = load_font_ttc(30, index=1)
    font_stat_lbl = load_font_ttc(11)
    font_diag_title = load_font_ttc(12, index=1)

    # ---- LEFT SIDE ----
    badge(draw, "OBSERVABILITY", 44, 54, ACCENT, (0, 0, 0), font_badge)

    draw.text((44, 108), "Cross-Account", font=load_font_ttc(40, index=1), fill=(235, 240, 255))
    draw.text((44, 158), "CloudWatch:", font=load_font_ttc(36, index=1), fill=ACCENT2)
    draw.text((44, 206), "The Silent Zero Trap", font=load_font_ttc(26, index=1), fill=(200, 210, 240))

    sub = "Query the wrong region. Get zero results. No error. The logs are there — you just asked the wrong region."
    wrap_text(draw, sub, 44, 260, 360, load_font_ttc(15), TEXT_DIM)

    y_stats = 375
    for val, lbl, sx in [("N", "ACCOUNTS", 44), ("2", "REGIONS", 165), ("0", "ERROR ON MISS", 246)]:
        draw.text((sx, y_stats), val, font=font_stat, fill=ACCENT)
        draw.text((sx, y_stats + 38), lbl, font=font_stat_lbl, fill=TEXT_DIM)

    author_block(draw, W, H, ACCENT)
    tags_block(draw, ["CloudWatch", "Cross-Account", "IAM", "Observability"], W, H, ACCENT)

    # ---- RIGHT DIAGRAM ----
    RX = 460
    draw.text((RX+30, 28), "MULTI-ACCOUNT CLOUDWATCH — REGION DISCOVERY PATTERN", font=font_diag_title, fill=(60, 110, 180))

    # Pod / IRSA
    rounded_rect(draw, [RX+20, 70, RX+200, 145], 8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    text_center(draw, "EKS Pod", (RX+20+RX+200)//2, 82, font_head, (200, 220, 255))
    text_center(draw, "IRSA Role + STS", (RX+20+RX+200)//2, 104, font_small, TEXT_DIM)
    text_center(draw, "AssumeRole per account", (RX+20+RX+200)//2, 122, font_tiny, TEXT_DIM)

    # Account rows
    accounts = [
        ("Account 1", ["us-east-1 ✓"], "verified", (40, 160, 80)),
        ("Account 2", ["eu-west-1 ✓"], "verified", (40, 160, 80)),
        ("Account 3", ["us-east-1", "eu-west-1"], "both (unverified)", WARN_BORDER),
    ]

    ay = 175
    for acct, regions, status, color in accounts:
        rounded_rect(draw, [RX+20, ay, RX+320, ay+78], 8, fill=BOX_BG, outline=color, width=1)
        draw.text((RX+30, ay+8), acct, font=font_head, fill=(210, 220, 240))
        draw.text((RX+30, ay+30), "Regions: " + ", ".join(regions), font=font_small, fill=color)
        draw.text((RX+30, ay+50), "Status: " + status, font=font_tiny, fill=TEXT_DIM)
        draw_arrow(draw, RX+200, 110, RX+200, ay, ACCENT, width=1)
        ay += 96

    # The silent zero box
    rounded_rect(draw, [RX+340, 70, RX+690, 190], 8, fill=ERR_BG, outline=ERR_BORDER, width=2)
    draw.text((RX+350, 82), "⚠  THE SILENT ZERO PROBLEM", font=load_font_ttc(13, index=1), fill=(240, 100, 100))
    lines_err = [
        "Query us-east-1 for a log group in eu-west-1:",
        "→ API call SUCCEEDS",
        "→ Returns 0 results",
        "→ No error, no 404",
        "→ Window marked as COMPLETE",
        "→ Never queried again",
        "",
        "Looks like: 'logging was never enabled'",
    ]
    ey = 105
    for l in lines_err:
        c = (220, 120, 120) if l.startswith("→") else TEXT_DIM
        draw.text((RX+354, ey), l, font=font_tiny, fill=c)
        ey += 14

    # Region discovery snippet
    rounded_rect(draw, [RX+340, 202, RX+690, 360], 8, fill=(12, 14, 30), outline=(50, 70, 150), width=1)
    draw.text((RX+350, 212), "Region discovery pattern:", font=load_font_ttc(12, index=1), fill=(140, 160, 220))
    code = [
        "for region in candidate_regions:",
        "  client = cross_account_client(",
        "    'logs', role_arn, region)",
        "  resp = client.describe_log_groups(",
        "    logGroupNamePrefix=prefix,",
        "    limit=1)",
        "  if resp['logGroups']:",
        "    confirmed_regions.append(region)",
    ]
    cy = 232
    for l in code:
        draw.text((RX+354, cy), l, font=font_tiny, fill=(140, 220, 180))
        cy += 14

    # Window sync rule
    rounded_rect(draw, [RX+20, ay+10, RX+690, ay+80], 8, fill=(12, 20, 36), outline=(50, 110, 170), width=1)
    text_center(draw, "Window Cache Rule: Only mark a window complete after ALL regions for the account are queried.", (RX+20+RX+690)//2, ay+22, font_small, (160, 200, 240))
    text_center(draw, "If one region fails, leave the window incomplete — it will re-run on the next sync.", (RX+20+RX+690)//2, ay+44, font_tiny, TEXT_DIM)
    text_center(draw, "Store per-account region lists in config — never derive them dynamically per query.", (RX+20+RX+690)//2, ay+64, font_tiny, TEXT_DIM)

    img.save(os.path.join(OUTPUT_DIR, "22-cross-account-cloudwatch-region-trap.png"))
    print("✓ cover 22")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cover_18()
    cover_19()
    cover_20()
    cover_21()
    cover_22()
    print("All covers generated.")

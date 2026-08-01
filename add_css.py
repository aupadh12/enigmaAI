#!/usr/bin/env python3
import re

SLUGS = [
    "2-agentic-ai-systems",
    "4-finops-for-agentic-ai",
    "5-benchmarking-llms-in-the-enterprise",
    "6-securing-agentic-ai",
    "7-kubernetes-to-managed-agent-runtime",
]

COVER_CSS = """
        .cover-image {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 12px;
            margin-bottom: 32px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
"""

for slug in SLUGS:
    path = f"blogposts/{slug}.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    if ".cover-image" not in html:
        # replace </style> with COVER_CSS + </style>
        html = re.sub(r'</style>', COVER_CSS + '</style>', html, count=1)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ {slug}.html — added CSS")

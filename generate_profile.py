import os
import io
import sys
import math
import random
import requests
from PIL import Image, ImageEnhance, ImageOps

# Ensure UTF-8 output encoding for Windows terminal compatibility
sys.stdout.reconfigure(encoding='utf-8')


# ==============================================================================
# CONFIGURATION & USER PROFILE DATA
# ==============================================================================
USERNAME = "rehan-1002"
DISPLAY_NAME = "Rehan"
TITLE = "Full-Stack Software Engineer & Open Source Builder"

LOCATION = "Neo-Tokyo // Remote"
STATUS = "🟢 Architecting High-Performance Systems"
BIO = "Building sleek web apps, distributed systems, and SMIL graphics."

STACK_ITEMS = [
    ("HTML5", "#E34F26"),
    ("CSS3", "#1572B6"),
    ("JavaScript", "#F7DF1E"),
    ("React", "#61DAFB"),
    ("Next.js", "#FFFFFF"),
    ("Node.js", "#339933"),
    ("Python", "#3572A5"),
    ("MongoDB", "#47A248"),
    ("Supabase", "#3ECF8E"),
    ("Firebase", "#FFCA28"),
    ("Vercel", "#000000"),
    ("Git", "#F05032"),
    ("GitHub", "#181717"),
    ("Docker", "#2496ED"),
]


STATS = [
    ("Public Repos", "42"),
    ("Total Stars", "1.2k+"),
    ("Yearly Commits", "2,480+"),
    ("Pull Requests", "310"),
    ("Contributions", "Top 1%"),
]

# ==============================================================================
# HELPER: ASCII ART GENERATOR FROM AVATAR
# ==============================================================================
ASCII_CHARS = "@%#*+=-:. "  # From dark/dense to light

def generate_ascii_art(username=USERNAME, width=46, height=24):
    """
    Fetches GitHub avatar for `username`, converts to grayscale, resizes,
    and maps pixels to ASCII characters. Returns a list of strings (rows).
    """
    avatar_url = f"https://avatars.githubusercontent.com/{username}"
    img = None
    try:
        resp = requests.get(avatar_url, timeout=5)
        if resp.status_code == 200:
            img = Image.open(io.BytesIO(resp.content))
    except Exception as e:
        print(f"[-] Could not fetch avatar for {username}: {e}. Using fallback generator.")

    if not img:
        # Generate procedural avatar fallback image
        img = Image.new("RGB", (200, 200), color=(13, 17, 23))
        # Draw a stylized dev skull / helmet shape using PIL if needed, or simple pattern

    # Convert to grayscale and enhance contrast
    img = img.convert("L")
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)

    # Resize adjusting for character aspect ratio (approx 1:2)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    if hasattr(img, "get_flattened_data"):
        pixels = list(img.get_flattened_data())
    else:
        pixels = list(img.getdata())

    ascii_rows = []
    num_chars = len(ASCII_CHARS)

    for i in range(height):
        row = ""
        for j in range(width):
            pixel_val = pixels[i * width + j]
            # Map 0-255 to ASCII_CHARS index
            char_idx = int((pixel_val / 255) * (num_chars - 1))
            row += ASCII_CHARS[char_idx]
        ascii_rows.append(row)

    return ascii_rows


# ==============================================================================
# 1. FILE 2: terminal-card.svg (ASCII PORTRAIT TERMINAL)
# ==============================================================================
def build_terminal_card_svg(output_path="terminal-card.svg", username=USERNAME):
    ascii_rows = generate_ascii_art(username=username, width=44, height=22)
    card_width = 480
    card_height = 370

    # Color gradient logic for ASCII rows (Cyberpunk cyan -> purple -> pink)
    def get_row_color(row_idx, total_rows):
        ratio = row_idx / max(1, total_rows - 1)
        r = int(0 + ratio * 230)
        g = int(243 - ratio * 120)
        b = int(255)
        return f"rgb({r},{g},{b})"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="{card_width}" height="{card_height}">')
    svg.append('<defs>')
    # Glow filter for window frame & text accents
    svg.append('''
        <filter id="neon-glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
        <linearGradient id="card-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00f3ff" stop-opacity="0.6"/>
            <stop offset="50%" stop-color="#bd93f9" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#ff79c6" stop-opacity="0.6"/>
        </linearGradient>
        <linearGradient id="header-bg" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#161b22"/>
            <stop offset="100%" stop-color="#0d1117"/>
        </linearGradient>
    ''')
    svg.append('</defs>')

    # Global CSS inside SVG
    svg.append('<style>')
    svg.append('''
        .bg-card { fill: #0d1117; stroke: url(#card-border); stroke-width: 1.5px; rx: 12px; }
        .window-header { fill: url(#header-bg); rx: 12px; }
        .term-dot-red { fill: #ff5f56; }
        .term-dot-yellow { fill: #ffbd2e; }
        .term-dot-green { fill: #27c93f; }
        .header-title { font-family: 'Fira Code', Monaco, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }
        .ascii-text { font-family: 'Courier New', Courier, monospace; font-size: 10px; font-weight: bold; white-space: pre; }
        .cmd-text { font-family: 'Fira Code', Monaco, Consolas, monospace; font-size: 12px; font-weight: bold; }
    ''')
    svg.append('</style>')

    # Card background & frame
    svg.append(f'<rect width="{card_width-4}" height="{card_height-4}" x="2" y="2" class="bg-card"/>')

    # Header bar
    svg.append(f'<path d="M 2 14 A 12 12 0 0 1 14 2 L {card_width-14} 2 A 12 12 0 0 1 {card_width-2} 14 L {card_width-2} 36 L 2 36 Z" fill="url(#header-bg)"/>')
    svg.append(f'<line x1="2" y1="36" x2="{card_width-2}" y2="36" stroke="#21262d" stroke-width="1"/>')

    # macOS buttons
    svg.append('<circle cx="18" cy="19" r="5.5" class="term-dot-red"/>')
    svg.append('<circle cx="34" cy="19" r="5.5" class="term-dot-yellow"/>')
    svg.append('<circle cx="50" cy="19" r="5.5" class="term-dot-green"/>')

    # Header title text
    svg.append(f'<text x="{card_width/2}" y="23" text-anchor="middle" class="header-title">zsh — {username}@cyber-deck: ~ (80x24)</text>')

    # ASCII Content Container
    start_y = 54
    line_height = 11.5
    total_ascii_rows = len(ascii_rows)

    svg.append('<g transform="translate(18, 0)">')

    for idx, row in enumerate(ascii_rows):
        y_pos = start_y + (idx * line_height)
        delay = round(idx * 0.07, 2)
        color = get_row_color(idx, total_ascii_rows)

        # Escaped row string for SVG
        safe_row = (row.replace('&', '&amp;')
                       .replace('<', '&lt;')
                       .replace('>', '&gt;')
                       .replace(' ', '&#160;'))

        # Row container with default opacity 1 for instant visibility
        svg.append(f'<g opacity="1">')
        # Line reveal animation
        svg.append(f'<animate attributeName="opacity" values="0.3;1" begin="{delay}s" dur="0.15s" fill="freeze"/>')
        
        # ASCII Row Text
        svg.append(f'<text x="0" y="{y_pos}" fill="{color}" class="ascii-text">{safe_row}</text>')

        # Sweeping White Glint/Cursor block animation across the line
        cursor_delay = delay
        cursor_dur = 0.06
        svg.append(f'<rect x="0" y="{y_pos - 9}" width="8" height="10" fill="#ffffff" opacity="0.8" filter="url(#neon-glow-cyan)">')
        svg.append(f'<animate attributeName="x" values="0;400" begin="{cursor_delay}s" dur="{cursor_dur}s" fill="freeze"/>')
        svg.append(f'<animate attributeName="opacity" values="0.8;0" begin="{cursor_delay + cursor_dur}s" dur="0.02s" fill="freeze"/>')
        svg.append('</rect>')

        svg.append('</g>')

    svg.append('</g>') # End ASCII group

    # Terminal Footer Section ($ whoami -> username reveal)
    footer_y = start_y + (total_ascii_rows * line_height) + 16
    svg.append(f'<line x1="16" y1="{footer_y - 12}" x2="{card_width-16}" y2="{footer_y - 12}" stroke="#21262d" stroke-width="1"/>')

    # $ whoami typewriter prompt
    cmd_start_time = round(total_ascii_rows * 0.07 + 0.1, 2)
    svg.append(f'<g transform="translate(20, {footer_y})">')
    
    # Prompt symbol
    svg.append('<text x="0" y="0" fill="#ff79c6" class="cmd-text">➜ </text>')
    svg.append('<text x="16" y="0" fill="#50fa7b" class="cmd-text">~ </text>')

    # Command typed out
    cmd_str = f"whoami --profile {username}"
    typed_id = "typed_cmd"
    svg.append(f'<text x="36" y="0" fill="#f8f8f2" class="cmd-text">{cmd_str}</text>')

    # Output response line (Default opacity 1)
    resp_start_time = cmd_start_time + 0.5
    svg.append(f'<g opacity="1" transform="translate(0, 18)">')
    svg.append(f'<animate attributeName="opacity" values="0;1" begin="{resp_start_time}s" dur="0.2s" fill="freeze"/>')
    svg.append(f'<text x="0" y="0" fill="#00f3ff" class="cmd-text" filter="url(#neon-glow-cyan)">⚡ [{DISPLAY_NAME}] :: ACTIVE_SESSION</text>')
    svg.append('</g>')

    # Blinking cursor
    cursor_x = 36 + (len(cmd_str) * 7.2)
    svg.append(f'<rect x="{cursor_x}" y="-10" width="7" height="12" fill="#00f3ff" opacity="1">')
    svg.append(f'<animate attributeName="opacity" values="1;0;1" begin="0s" dur="0.8s" repeatCount="indefinite"/>')
    svg.append('</rect>')


    svg.append('</g>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[+] Successfully generated {output_path}")


# ==============================================================================
# 2. FILE 3: info-card.svg (NEOFETCH INFO CARD)
# ==============================================================================
def build_info_card_svg(output_path="info-card.svg"):
    card_width = 480
    card_height = 370

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="{card_width}" height="{card_height}">')
    svg.append('<defs>')
    svg.append('''
        <filter id="neon-glow-purple" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
        <linearGradient id="card-border-info" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ff9e3b" stop-opacity="0.6"/>
            <stop offset="50%" stop-color="#00f3ff" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#39d353" stop-opacity="0.6"/>
        </linearGradient>
        <linearGradient id="divider-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#ff9e3b"/>
            <stop offset="50%" stop-color="#00f3ff"/>
            <stop offset="100%" stop-color="#bd93f9"/>
        </linearGradient>
    ''')
    svg.append('</defs>')

    svg.append('<style>')
    svg.append('''
        .bg-card { fill: #0d1117; stroke: url(#card-border-info); stroke-width: 1.5px; rx: 12px; }
        .window-header { fill: #161b22; rx: 12px; }
        .term-dot-red { fill: #ff5f56; }
        .term-dot-yellow { fill: #ffbd2e; }
        .term-dot-green { fill: #27c93f; }
        .header-title { font-family: 'Fira Code', Monaco, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }
        
        .neo-title { font-family: 'Fira Code', Monaco, monospace; font-size: 15px; font-weight: 800; fill: #ff9e3b; }
        .neo-host { font-family: 'Fira Code', Monaco, monospace; font-size: 13px; font-weight: 600; fill: #00f3ff; }
        
        .label-orange { font-family: 'Fira Code', monospace; font-size: 11.5px; font-weight: bold; fill: #ff9e3b; }
        .label-blue { font-family: 'Fira Code', monospace; font-size: 11.5px; font-weight: bold; fill: #00f3ff; }
        .label-green { font-family: 'Fira Code', monospace; font-size: 11.5px; font-weight: bold; fill: #39d353; }
        .label-purple { font-family: 'Fira Code', monospace; font-size: 11.5px; font-weight: bold; fill: #bd93f9; }
        .label-white { font-family: 'Fira Code', monospace; font-size: 11.5px; font-weight: bold; fill: #f0f6fc; }
        .val-text { font-family: 'Fira Code', Monaco, monospace; font-size: 11.5px; fill: #c9d1d9; }
        .badge-bg { rx: 4px; }
    ''')
    svg.append('</style>')

    # Card background & frame
    svg.append(f'<rect width="{card_width-4}" height="{card_height-4}" x="2" y="2" class="bg-card"/>')

    # Header bar
    svg.append(f'<path d="M 2 14 A 12 12 0 0 1 14 2 L {card_width-14} 2 A 12 12 0 0 1 {card_width-2} 14 L {card_width-2} 36 L 2 36 Z" fill="#161b22"/>')
    svg.append(f'<line x1="2" y1="36" x2="{card_width-2}" y2="36" stroke="#21262d" stroke-width="1"/>')

    # macOS buttons
    svg.append('<circle cx="18" cy="19" r="5.5" class="term-dot-red"/>')
    svg.append('<circle cx="34" cy="19" r="5.5" class="term-dot-yellow"/>')
    svg.append('<circle cx="50" cy="19" r="5.5" class="term-dot-green"/>')

    # Header title text
    svg.append(f'<text x="{card_width/2}" y="23" text-anchor="middle" class="header-title">neofetch --sysinfo</text>')

    # Neofetch Header Banner
    svg.append('<g transform="translate(24, 60)">')
    
    # Title & Hostname line
    svg.append(f'<text x="0" y="0" class="neo-title">{USERNAME}</text>')
    svg.append(f'<text x="80" y="0" class="neo-host">@{DISPLAY_NAME}</text>')
    
    # Pulsing neon divider line
    svg.append('<rect x="0" y="8" width="432" height="2" fill="url(#divider-grad)" rx="1">')
    svg.append('<animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>')
    svg.append('</rect>')
    svg.append('</g>')

    # Info Items Data Configuration
    info_rows = [
        ("ABOUT", TITLE, "label-orange", "🟧"),
        ("FRONTEND", "HTML5 • CSS3 • JS • React • Next.js • Tailwind", "label-blue", "🟦"),
        ("BACKEND & DB", "Node.js • Express • Python • MongoDB • Supabase", "label-green", "🟩"),
        ("CLOUD & HOST", "Vercel • Render • Netlify • Firebase • Docker", "label-purple", "🟪"),
        ("TOOLS & VCS", "Git • GitHub • Postman • VS Code", "label-white", "⬜"),
        ("STATUS", STATUS, "label-green", "🟢"),
    ]

    start_y = 96
    row_height = 29.5

    for idx, (label, val, color_cls, icon) in enumerate(info_rows):
        y_pos = start_y + (idx * row_height)
        delay = round(idx * 0.02, 2)

        # Slide-up & fade-in SMIL animation with fallback opacity="1"
        svg.append(f'<g transform="translate(24, {y_pos})" opacity="1">')
        svg.append(f'<animate attributeName="opacity" values="0.4;1" begin="{delay}s" dur="0.15s" fill="freeze"/>')
        svg.append(f'<animateTransform attributeName="transform" type="translate" values="24,{y_pos+5}; 24,{y_pos}" begin="{delay}s" dur="0.15s" fill="freeze"/>')

        # Icon + Label
        svg.append(f'<text x="0" y="12" class="{color_cls}">{icon} {label.ljust(13)}:</text>')
        # Value Text
        svg.append(f'<text x="155" y="12" class="val-text">{val}</text>')

        svg.append('</g>')

    # Terminal Color Blocks Palette at bottom (Neofetch signature feature)
    palette_y = start_y + (len(info_rows) * row_height) + 12
    colors_row1 = ["#161b22", "#ff5555", "#50fa7b", "#f1fa8c", "#bd93f9", "#ff79c6", "#8be9fd", "#f8f8f2"]
    colors_row2 = ["#6272a4", "#ff6e6e", "#69ff94", "#ffffa5", "#d6acff", "#ff92d0", "#a4ffff", "#ffffff"]

    block_delay_start = round(len(info_rows) * 0.02 + 0.05, 2)

    svg.append(f'<g transform="translate(24, {palette_y})">')
    
    # Render palette blocks row 1 (fallback opacity="1")
    for b_idx, col in enumerate(colors_row1):
        b_delay = block_delay_start + (b_idx * 0.03)
        bx = b_idx * 24
        svg.append(f'<rect x="{bx}" y="0" width="20" height="12" fill="{col}" rx="3" opacity="1">')
        svg.append(f'<animate attributeName="opacity" values="0.4;1" begin="{b_delay:.2f}s" dur="0.15s" fill="freeze"/>')
        svg.append('</rect>')

    # Render palette blocks row 2 (fallback opacity="1")
    for b_idx, col in enumerate(colors_row2):
        b_delay = block_delay_start + 0.25 + (b_idx * 0.03)
        bx = b_idx * 24
        svg.append(f'<rect x="{bx}" y="15" width="20" height="12" fill="{col}" rx="3" opacity="1">')
        svg.append(f'<animate attributeName="opacity" values="0.4;1" begin="{b_delay:.2f}s" dur="0.15s" fill="freeze"/>')
        svg.append('</rect>')


    svg.append('</g>') # End palette group

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[+] Successfully generated {output_path}")


# ==============================================================================
# 3. FILE 1: github-contribution-animation.svg (CONTRIBUTION GRAPH)
# ==============================================================================
def build_contribution_svg(output_path="github-contribution-animation.svg"):
    cols = 53
    rows = 7
    square_size = 11
    gap = 3.5
    padding_x = 45
    padding_y = 52
    
    svg_width = int(padding_x + cols * (square_size + gap) + 20)
    svg_height = 210

    # Color palette for levels
    LEVEL_COLORS = {
        0: {"bg": "#161b22", "border": "#21262d", "glow": False},
        1: {"bg": "#0e4429", "border": "#1b5e39", "glow": False},
        2: {"bg": "#006d32", "border": "#26a641", "glow": False},
        3: {"bg": "#26a641", "border": "#39d353", "glow": True},
        4: {"bg": "#39d353", "border": "#00f3ff", "glow": True},
    }

    # Generate a realistic distribution of contribution levels
    random.seed(42)  # Consistent attractive layout
    grid = []
    for c in range(cols):
        col_data = []
        for r in range(rows):
            # Weighted random favoring active days
            weights = [0.25, 0.25, 0.25, 0.15, 0.10]
            level = random.choices([0, 1, 2, 3, 4], weights=weights)[0]
            col_data.append(level)
        grid.append(col_data)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('<defs>')
    # Specular outer glow filter for level 3 & 4 squares
    svg.append('''
        <filter id="square-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
        <linearGradient id="card-border-contrib" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#39d353" stop-opacity="0.5"/>
            <stop offset="50%" stop-color="#00f3ff" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#bd93f9" stop-opacity="0.5"/>
        </linearGradient>
    ''')
    svg.append('</defs>')

    svg.append('<style>')
    svg.append('''
        .bg-contrib { fill: #0d1117; stroke: url(#card-border-contrib); stroke-width: 1.5px; rx: 12px; }
        .header-text { font-family: 'Fira Code', Monaco, monospace; font-size: 13px; font-weight: bold; fill: #f0f6fc; }
        .subtext { font-family: 'Fira Code', Monaco, monospace; font-size: 11px; fill: #8b949e; }
        .label-text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 10px; fill: #7d8590; }
    ''')
    svg.append('</style>')

    # Main Card Background
    svg.append(f'<rect width="{svg_width-4}" height="{svg_height-4}" x="2" y="2" class="bg-contrib"/>')

    # Card Title Header & Total Counter
    svg.append(f'<text x="24" y="28" class="header-text">1,482 contributions in the last year</text>')
    svg.append(f'<text x="{svg_width-24}" y="28" text-anchor="end" class="subtext">Jan 2025 – Jan 2026</text>')

    # Month Labels (Jan..Dec) across top
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_step = cols / 12.0
    for i, m in enumerate(months):
        mx = padding_x + (i * month_step * (square_size + gap))
        svg.append(f'<text x="{mx:.1f}" y="45" class="label-text">{m}</text>')

    # Day Labels (Mon, Wed, Fri) on left side
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for r_idx, label in day_labels:
        dy = padding_y + (r_idx * (square_size + gap)) + 9
        svg.append(f'<text x="18" y="{dy}" class="label-text">{label}</text>')

    # Contribution Grid with Diagonal Slant Reveal Animation
    svg.append('<g>')

    for c in range(cols):
        for r in range(rows):
            level = grid[c][r]
            color_cfg = LEVEL_COLORS[level]
            x = padding_x + c * (square_size + gap)
            y = padding_y + r * (square_size + gap)
            cx = x + square_size / 2.0
            cy = y + square_size / 2.0

            # Diagonal Slant Delay Formula: (c + (6 - r)) * delay_factor
            # Sweeps from bottom-left (c=0, r=6) to top-right (c=52, r=0)
            slant_score = c + (6 - r)
            delay = round(slant_score * 0.045, 3)

            filter_attr = 'filter="url(#square-glow)"' if color_cfg["glow"] else ''

            # Group for each square
            svg.append(f'<g transform="translate({x:.1f}, {y:.1f})">')

            # Base Square (Default opacity 1 for instant display)
            svg.append(f'<rect width="{square_size}" height="{square_size}" rx="2" ry="2" fill="{color_cfg["bg"]}" stroke="{color_cfg["border"]}" stroke-width="0.8" {filter_attr} opacity="1">')
            svg.append(f'<animate attributeName="opacity" values="0.3;1" begin="{delay}s" dur="0.25s" fill="freeze"/>')
            svg.append(f'<animateTransform attributeName="transform" type="scale" values="0.1;1.2;1" begin="{delay}s" dur="0.3s" fill="freeze" transform-origin="{square_size/2} {square_size/2}"/>')
            svg.append('</rect>')


            # Specular Glint Highlight Flash (white/green flash as square settles)
            glint_color = "#ffffff" if level < 3 else "#39d353"
            svg.append(f'<rect width="{square_size}" height="{square_size}" rx="2" ry="2" fill="{glint_color}" opacity="0">')
            svg.append(f'<animate attributeName="opacity" values="0;0.95;0" begin="{delay}s" dur="0.35s" fill="freeze"/>')
            svg.append('</rect>')

            svg.append('</g>')

    svg.append('</g>') # End grid group

    # Legend at Bottom Right (Less [0][1][2][3][4] More)
    legend_y = svg_height - 18
    legend_x = svg_width - 150
    svg.append(f'<text x="{legend_x - 32}" y="{legend_y + 9}" class="label-text">Less</text>')

    for lvl in range(5):
        lx = legend_x + (lvl * 15)
        l_cfg = LEVEL_COLORS[lvl]
        l_filter = 'filter="url(#square-glow)"' if l_cfg["glow"] else ''
        svg.append(f'<rect x="{lx}" y="{legend_y}" width="11" height="11" rx="2" fill="{l_cfg["bg"]}" stroke="{l_cfg["border"]}" stroke-width="0.8" {l_filter}/>')

    svg.append(f'<text x="{legend_x + 80}" y="{legend_y + 9}" class="label-text">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[+] Successfully generated {output_path}")


# ==============================================================================
# 4. README INTEGRATION GENERATOR
# ==============================================================================
def update_readme(readme_path="README.md"):
    content = f"""<div align="center">

# ⚡ WELCOME TO MY CYBER DECK ⚡

```text
██████╗ ██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ███████╗██╗██╗     ███╗   ██╗███████╗████████╗
██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔════╝██║██║     ████╗  ██║██╔════╝╚══██╔══╝
██║  ██║██║   ██║██████╔╝█████╗  ██████╔╝██║   ██║█████╗  ██║██║     ██╔██╗ ██║█████╗     ██║   
██║  ██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗██║   ██║██╔══╝  ██║██║     ██║╚██╗██║██╔══╝     ██║   
██████╔╝╚██████╔╝██║     ███████╗██║  ██║╚██████╔╝██║     ██║███████╗██║ ╚████║███████╗   ██║   
╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   
```

---

<!-- CYBERPUNK PROFILE CARDS ROW -->
<table border="0" cellspacing="0" cellpadding="0" width="100%">
  <tr>
    <td width="50%" align="center" valign="top">
      <img src="./terminal-card.svg" width="100%" alt="Terminal ASCII Portrait" />
    </td>
    <td width="50%" align="center" valign="top">
      <img src="./info-card.svg" width="100%" alt="Neofetch Info Card" />
    </td>
  </tr>
</table>

<br />

<!-- GITHUB CONTRIBUTION GRAPH ANIMATION -->
<img src="./github-contribution-animation.svg" width="100%" alt="GitHub Contribution Graph Animation" />

---

### 🚀 Stack & Technologies
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Netlify](https://img.shields.io/badge/Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)



</div>
"""

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Successfully created/updated {readme_path}")


# ==============================================================================
# MAIN EXECUTION ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    print("==================================================================")
    print("🚀 GENERATING CYBERPUNK ANIMATED GITHUB PROFILE SVGS & README")
    print("==================================================================")
    
    # 1. Generate Terminal ASCII Card
    build_terminal_card_svg("terminal-card.svg", username=USERNAME)
    
    # 2. Generate Neofetch Info Card
    build_info_card_svg("info-card.svg")
    
    # 3. Generate Contribution Calendar SVG
    build_contribution_svg("github-contribution-animation.svg")
    
    # 4. Integrate into README.md
    update_readme("README.md")
    
    print("\n✅ All 3 high-end SVGs and README.md generated successfully!")

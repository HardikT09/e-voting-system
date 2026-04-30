"""
styles.py — Visual Theme & Style Constants
Centralizes all colors, fonts, and padding for a consistent modern look.
Concepts used: Constants, Dictionaries
"""

# ─── Color Palette ─────────────────────────────────────────────────────────────
# Deep navy + saffron accent — inspired by Indian tricolor vibes
COLORS = {
    "bg_dark":      "#0D1B2A",   # Main background (deep navy)
    "bg_card":      "#1B2C3E",   # Card / panel background
    "bg_input":     "#243447",   # Input field background
    "accent":       "#F4A31A",   # Saffron accent (buttons, highlights)
    "accent_hover": "#D4891A",   # Darker saffron on hover
    "accent_green": "#27AE60",   # Success / confirm green
    "accent_red":   "#E74C3C",   # Error / warning red
    "text_primary": "#EAECEF",   # Main text
    "text_muted":   "#8A9BB0",   # Secondary / muted text
    "text_dark":    "#0D1B2A",   # Dark text on light buttons
    "border":       "#2E4058",   # Subtle border color
    "radio_select": "#F4A31A",   # Selected radio highlight
    "white":        "#FFFFFF",
}

# ─── Font Definitions ──────────────────────────────────────────────────────────
FONTS = {
    "title":     ("Georgia",          26, "bold"),
    "subtitle":  ("Georgia",          14, "italic"),
    "heading":   ("Trebuchet MS",     16, "bold"),
    "body":      ("Trebuchet MS",     12),
    "body_bold": ("Trebuchet MS",     12, "bold"),
    "small":     ("Trebuchet MS",     10),
    "button":    ("Trebuchet MS",     12, "bold"),
    "label":     ("Trebuchet MS",     11),
    "voter_id":  ("Courier New",      18, "bold"),
    "result_big":("Georgia",          20, "bold"),
    "winner":    ("Georgia",          18, "bold"),
}

# ─── Padding / Sizing ──────────────────────────────────────────────────────────
PAD = {
    "window_pad": 30,
    "section":    20,
    "inner":      10,
    "btn_x":      30,
    "btn_y":       8,
}

# ─── Window Sizes ──────────────────────────────────────────────────────────────
SIZES = {
    "login":    "500x820",
    "vote":     "600x680",
    "results":  "640x700",
    "admin":    "420x300",
}

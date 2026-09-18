"""
Day 65: Design System & UX Principles Engine
Implements color luminance calculations, WCAG contrast ratio compliance,
modular typography scale generators, and design token architectures.
"""

from typing import Dict, Tuple, List


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Converts hex color string to RGB tuple."""
    hex_clean = hex_color.lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join([c * 2 for c in hex_clean])
    return int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16)


def calculate_relative_luminance(hex_color: str) -> float:
    """Calculates relative luminance according to WCAG 2.1 specs."""
    r, g, b = [x / 255.0 for x in hex_to_rgb(hex_color)]
    r_val = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g_val = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b_val = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r_val + 0.7152 * g_val + 0.0722 * b_val


def calculate_contrast_ratio(foreground_hex: str, background_hex: str) -> float:
    """Computes contrast ratio (1:1 to 21:1) between two colors."""
    lum1 = calculate_relative_luminance(foreground_hex)
    lum2 = calculate_relative_luminance(background_hex)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def evaluate_wcag(contrast: float) -> Dict[str, bool]:
    """Evaluates WCAG 2.1 AA and AAA compliance for normal and large text."""
    return {
        "AA_normal": contrast >= 4.5,
        "AA_large": contrast >= 3.0,
        "AAA_normal": contrast >= 7.0,
        "AAA_large": contrast >= 4.5,
    }


def generate_modular_scale(base: float = 16.0, ratio: float = 1.25, steps: int = 6) -> List[Dict[str, float]]:
    """Generates a Major Third (1.25) typographic scale."""
    labels = ["body", "h5", "h4", "h3", "h2", "h1"]
    scale = []
    for i in range(steps):
        size = round(base * (ratio ** i), 2)
        scale.append({"step": i, "label": labels[i] if i < len(labels) else f"display-{i}", "px": size, "rem": round(size / 16.0, 3)})
    return scale


CURATED_PALETTES = {
    "Cyberpunk Dark": {
        "bg": "#090d16",
        "card": "#131b2e",
        "primary": "#38bdf8",
        "accent": "#f43f5e",
        "text": "#f8fafc",
        "muted": "#94a3b8"
    },
    "Warm Editorial": {
        "bg": "#faf7f2",
        "card": "#ffffff",
        "primary": "#d97706",
        "accent": "#0f766e",
        "text": "#1c1917",
        "muted": "#78716c"
    },
    "Emerald Minimal": {
        "bg": "#061a14",
        "card": "#0c2e24",
        "primary": "#10b981",
        "accent": "#3b82f6",
        "text": "#ecfdf5",
        "muted": "#6ee7b7"
    }
}

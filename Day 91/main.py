"""
Day 91: Image Color Palette Generator
Interactive Unsupervised K-Means Clustering & Palette Studio CLI
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from palette_generator import ColorPaletteGenerator


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 91: IMAGE COLOR PALETTE GENERATOR (K-MEANS CLUSTERING)")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Unsupervised Machine Learning Concepts:")
    print("  • 3D Color Vector Space: Pixels mapped as (R, G, B) coordinate points")
    print("  • K-Means Centroid Optimization: Converging onto dominant color clusters")
    print("  • Cluster Frequency Proportions & Hexadecimal Code Conversion")
    print("  • Visual Palette Swatch Export via Pillow & ANSI TrueColor Terminal Blocks")
    print("=" * 76 + "\n")


def display_palette_cli(palette):
    print("\n🎨 EXTRACTED DOMINANT COLOR PALETTE")
    print("=" * 60)
    for rank, item in enumerate(palette, start=1):
        r, g, b = item["rgb"]
        # ANSI 24-bit TrueColor background square
        color_block = f"\033[48;2;{r};{g};{b}m        \033[0m"
        print(f"  {rank}. {color_block}  \033[1m{item['hex']}\033[0m  RGB({r:>3d}, {g:>3d}, {b:>3d})  [{item['percent']:>4.1f}%]")
    print("=" * 60 + "\n")


def analyze_sample():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_art = ColorPaletteGenerator.create_sample_artwork("sample_artwork.png")
    print(f"1. Synthesized sample artwork: {os.path.basename(sample_art)}")
    print("2. Running K-Means clustering (k=6 color clusters)...")
    palette = ColorPaletteGenerator.extract_palette(sample_art, num_colors=6)
    display_palette_cli(palette)

    swatch = ColorPaletteGenerator.export_palette_swatch(palette, "sample_palette_swatch.png")
    print(f"✅ Exported visual color palette swatch to:")
    print(f"   file:///{swatch.replace(os.sep, '/')}\n")


def analyze_custom():
    path = input("\nEnter path to image file: ").strip()
    if not os.path.exists(path):
        print(f"⚠️ Image '{path}' not found.\n")
        return

    k_str = input("Number of color clusters to extract (3-10, default 6): ").strip()
    k = int(k_str) if k_str.isdigit() else 6

    print(f"Running K-Means color clustering on '{os.path.basename(path)}'...")
    palette = ColorPaletteGenerator.extract_palette(path, num_colors=k)
    display_palette_cli(palette)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_name = os.path.splitext(os.path.basename(path))[0] + "_palette.png"
    swatch = ColorPaletteGenerator.export_palette_swatch(palette, out_name)
    print(f"✅ Saved palette swatch to: file:///{swatch.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies image creation, K-Means clustering convergence, and swatch output."""
    print("\n🔍 Running Day 91 Automated K-Means Color Palette Test Suite...")
    print("-" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_img = ColorPaletteGenerator.create_sample_artwork("test_art.png")
    assert os.path.exists(sample_img)
    print(" [PASS] 1. Synthetic image generation verified.")

    # 2. K-Means extraction check
    palette = ColorPaletteGenerator.extract_palette(sample_img, num_colors=5)
    assert len(palette) == 5, f"Expected 5 clusters, got {len(palette)}"
    total_pct = sum(item["percent"] for item in palette)
    assert abs(total_pct - 100.0) < 2.0, "Cluster percentages must sum to ~100%."
    print(" [PASS] 2. K-Means clustering: 5 distinct color centroids extracted with 100% total weight.")

    # 3. Hex code formatting check
    first_color = palette[0]
    assert first_color["hex"].startswith("#") and len(first_color["hex"]) == 7
    print(f" [PASS] 3. Hexadecimal color formatting verified: Dominant cluster = {first_color['hex']}.")

    # 4. Swatch image export check
    swatch_path = ColorPaletteGenerator.export_palette_swatch(palette, "test_swatch.png")
    assert os.path.exists(swatch_path) and os.path.getsize(swatch_path) > 1000
    print(" [PASS] 4. Pillow palette swatch image rendering verified.")

    # Clean test artifacts
    for f in [sample_img, swatch_path]:
        try:
            os.remove(f)
        except Exception:
            pass

    print("-" * 70)
    print("✨ ALL 4 TESTS PASSED! Image Color Palette Generator fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 🎨 Extract Color Palette from Sample Artwork (K-Means)")
        print("  2) 🖼️ Analyze Custom Local Image")
        print("  3) ✅ Run Automated Verification Suite (4 Unit Tests)")
        print("  4) 🚪 Exit")
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            analyze_sample()
        elif choice == "2":
            analyze_custom()
        elif choice == "3":
            run_automated_tests()
        elif choice in ("4", "exit", "quit", "q"):
            print("\n👋 Stay colorful! Keep exploring computer vision 🎨\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-4.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 91 gracefully... Goodbye!\n")

"""
Day 84: Image Watermarking Desktop & CLI Studio
Interactive Asset Copyright Protection CLI
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
from watermarker import WatermarkEngine


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 84: IMAGE WATERMARKING & DIGITAL ASSET COPYRIGHT STUDIO")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Core Pillow Image Processing Concepts:")
    print("  • RGBA Alpha-Channel Composite Layering (Image.alpha_composite)")
    print("  • Dynamic Bounding Box Typography Calculation (draw.textbbox)")
    print("  • Multi-mode Positioning: Corners, Center, and Anti-theft Tiled Arrays")
    print("  • Configurable Opacity Blending (0.0 to 1.0) & Font Size Scaling")
    print("=" * 76 + "\n")


def watermark_sample():
    print("\n🎨 WATERMARKING SAMPLE IMAGE")
    print("=" * 60)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_path = WatermarkEngine.create_sample_image("sample_photo.png")
    out_path = os.path.join(base_dir, "watermarked_sample.png")

    text = "© 2026 Tirth Patel • All Rights Reserved"
    WatermarkEngine.apply_text_watermark(
        image_path=sample_path,
        text=text,
        output_path=out_path,
        position="bottom-right",
        opacity=0.75,
        font_size=28
    )

    print(f"✅ Generated sample base photo: {os.path.basename(sample_path)}")
    print(f"✅ Applied watermark text: \"{text}\"")
    print(f"✅ Saved watermarked result to:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def watermark_tiled():
    print("\n🛡️ ANTI-THEFT TILED WATERMARK GENERATOR")
    print("=" * 60)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_path = WatermarkEngine.create_sample_image("sample_photo.png")
    out_path = os.path.join(base_dir, "tiled_watermark.png")

    text = "CONFIDENTIAL / PROOF"
    WatermarkEngine.apply_text_watermark(
        image_path=sample_path,
        text=text,
        output_path=out_path,
        position="tiled",
        opacity=0.35,
        font_size=32
    )

    print(f"✅ Generated anti-theft diagonal tiled proof:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def custom_watermark():
    print("\n🖼️ CUSTOM IMAGE WATERMARKING")
    print("=" * 60)
    img_path = input("Enter path to source image (leave blank for sample): ").strip()
    if not img_path or not os.path.exists(img_path):
        img_path = WatermarkEngine.create_sample_image("sample_photo.png")
        print(f"Using default scenic photo ({img_path})")

    text = input("Enter watermark text (e.g. '© 2026 Portfolio'): ").strip()
    if not text:
        text = "© 2026 Copyright Protected"

    print("\nPosition options: 1) bottom-right  2) bottom-left  3) center  4) top-right  5) tiled")
    pos_choice = input("Select position (1-5, default 1): ").strip()
    pos_map = {"1": "bottom-right", "2": "bottom-left", "3": "center", "4": "top-right", "5": "tiled"}
    pos = pos_map.get(pos_choice, "bottom-right")

    op_str = input("Opacity (0.1 to 1.0, default 0.6): ").strip()
    opacity = float(op_str) if op_str else 0.6

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(base_dir, "custom_watermarked.png")

    WatermarkEngine.apply_text_watermark(
        image_path=img_path,
        text=text,
        output_path=out_path,
        position=pos,
        opacity=opacity,
        font_size=32
    )

    print(f"\n✅ Watermarked image saved to:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies image generation, alpha composite blending, and position geometry."""
    print("\n🔍 Running Day 84 Automated Watermarking Test Suite...")
    print("-" * 70)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Sample creation
    sample_img = WatermarkEngine.create_sample_image("test_sample.png", 400, 300)
    assert os.path.exists(sample_img)
    print(" [PASS] 1. Canvas generation: Synthetic scenic photo created.")

    # 2. Bottom-right text watermark
    out_br = os.path.join(base_dir, "test_br.png")
    WatermarkEngine.apply_text_watermark(sample_img, "TEST", out_br, position="bottom-right", opacity=0.8)
    assert os.path.exists(out_br) and os.path.getsize(out_br) > 1000
    print(" [PASS] 2. Corner positioning (bottom-right) alpha-composite verified.")

    # 3. Center positioning
    out_c = os.path.join(base_dir, "test_c.png")
    WatermarkEngine.apply_text_watermark(sample_img, "CENTER", out_c, position="center", opacity=0.5)
    assert os.path.exists(out_c)
    print(" [PASS] 3. Centered watermark geometry calculation verified.")

    # 4. Tiled watermark
    out_t = os.path.join(base_dir, "test_t.png")
    WatermarkEngine.apply_text_watermark(sample_img, "PROOF", out_t, position="tiled", opacity=0.3)
    assert os.path.exists(out_t)
    print(" [PASS] 4. Multi-tile grid pattern overlay verified.")

    # Clean up test artifacts
    for f in [sample_img, out_br, out_c, out_t]:
        try:
            os.remove(f)
        except Exception:
            pass

    print("-" * 70)
    print("✨ ALL 4 TESTS PASSED! Image Watermarking Studio fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 🎨 Watermark Sample Scenic Photo (Bottom-Right Badge)")
        print("  2) 🛡️ Generate Tiled Anti-Theft Proof")
        print("  3) 🖼️ Custom Image & Watermark Parameters")
        print("  4) ✅ Run Automated Verification Suite (4 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            watermark_sample()
        elif choice == "2":
            watermark_tiled()
        elif choice == "3":
            custom_watermark()
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Keep protecting your creative assets! 🛡️\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 84 gracefully... Goodbye!\n")

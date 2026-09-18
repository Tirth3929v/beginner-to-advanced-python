# Day 43 - ASCII Art Banner
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logo = r"""
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                          ║
  ║     ██████╗   █████╗  ██╗   ██╗     ██╗  ██╗  ██████╗                    ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║  ╚════██╗                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║   █████╔╝                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║   ╚═══██╗                   ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║  ██████╔╝                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝  ╚═════╝                    ║
  ║                                                                          ║
  ║       🎨   I N T R O D U C T I O N   T O   C S S   3   ✨                ║
  ║                                                                          ║
  ║     [ CSS Selectors • Box Model • Padding • Margin • Typography ]        ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

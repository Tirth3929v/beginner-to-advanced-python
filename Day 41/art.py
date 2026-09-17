# Day 41 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██╗  ██╗   ██╗                       ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║  ███║                       ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║  ╚██║                       ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║   ██║                       ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║   ██║                       ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝   ╚═╝                       ║
  ║                                                                          ║
  ║       🌐   W E B   F O U N D A T I O N   -   H T M L 5   📄              ║
  ║                                                                          ║
  ║       [ Semantic HTML5 • Document Structure • Tags • Personal Site ]     ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

# Day 44 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██╗  ██╗  ██╗  ██╗                   ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║  ██║  ██║                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║  ███████║                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║  ╚════██║                   ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║       ██║                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝       ╚═╝                   ║
  ║                                                                          ║
  ║      📐   I N T E R M E D I A T E   C S S   -   F L E X B O X   📱       ║
  ║                                                                          ║
  ║      [ CSS Positioning • Flexbox • Media Queries • Responsive Layouts ]  ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

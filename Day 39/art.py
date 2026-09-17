# Day 39 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██████╗   ██████╗                    ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ██╔═████╗                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝ ██║██╔██║                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗ ████╔╝██║                   ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝ ╚██████╔╝                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝   ╚═════╝                    ║
  ║                                                                          ║
  ║         ✈️   F L I G H T   D E A L   F I N D E R   🌍                    ║
  ║                                                                          ║
  ║       [ Flight Search APIs • IATA Codes • Price Tracker • Capstone ]     ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

# Day 47 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██╗  ██╗  ███████╗                   ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║  ╚════██║                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║      ██╔╝                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║     ██╔╝                    ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║    ██║                      ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝    ╚═╝                      ║
  ║                                                                          ║
  ║     🛒   A M A Z O N   P R I C E   T R A C K E R   📉                    ║
  ║                                                                          ║
  ║    [ Web Scraping • Price Parsing • Threshold Alerts • Email Dispatch ]  ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

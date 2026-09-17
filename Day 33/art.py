# Day 33 - ASCII Art Banner
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ╚════██╗                    ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝  █████╔╝                    ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗  ╚═══██╗                    ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝ ██████╔╝                    ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝  ╚═════╝                     ║
  ║                                                                          ║
  ║       🛰️   I S S   O V E R H E A D   N O T I F I E R   🌌                ║
  ║                                                                          ║
  ║     [ REST APIs • Coordinates • Sunrise/Sunset API • Geolocation ]       ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

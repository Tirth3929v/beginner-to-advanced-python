# Day 40 - ASCII Art Banner
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║ ██╔═████╗                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║ ██║██╔██║                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║ ████╔╝██║                   ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║ ╚██████╔╝                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝  ╚═════╝                    ║
  ║                                                                          ║
  ║         ✈️   F L I G H T   C L U B   C A P S T O N E   💌                ║
  ║                                                                          ║
  ║     [ Customer Acquisition • Email Broadcasts • Google Flights Link ]    ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

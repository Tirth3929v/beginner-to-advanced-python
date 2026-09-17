# Day 31 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██████╗    ██╗                       ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ████║                       ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝   ██║                       ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗   ██║                       ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝   ██║                       ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝    ╚═╝                       ║
  ║                                                                          ║
  ║        📇   F L A S H   C A R D   L E A R N I N G   A P P   🇫🇷           ║
  ║                                                                          ║
  ║    [ Tkinter Canvas • Card Flip Timers • CSV Word Bank • State Tracking ]║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

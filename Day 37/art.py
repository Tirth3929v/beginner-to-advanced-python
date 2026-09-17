# Day 37 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██████╗  ███████╗                    ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ╚════██║                    ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝     ██╔╝                    ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗    ██╔╝                     ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝    ██║                      ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝     ╚═╝                      ║
  ║                                                                          ║
  ║          📊   P I X E L A   H A B I T   T R A C K E R   🟩               ║
  ║                                                                          ║
  ║    [ HTTP POST / PUT / DELETE • Headers • Pixela API • Habit Streaks ]   ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

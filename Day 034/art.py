# Day 34 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██████╗  ██╗  ██╗                    ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ██║  ██║                    ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝ ███████║                    ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗ ╚════██║                    ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝      ██║                    ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝       ╚═╝                    ║
  ║                                                                          ║
  ║          🧠   G U I   Q U I Z Z E R   A P P   🏆                         ║
  ║                                                                          ║
  ║      [ Open Trivia DB API • OOP Architecture • Tkinter True/False UI ]   ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

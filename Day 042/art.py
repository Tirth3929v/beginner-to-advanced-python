# Day 42 - ASCII Art Banner
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
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║  ██╔═══╝                    ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║  ███████╗                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝  ╚══════╝                   ║
  ║                                                                          ║
  ║       📝   I N T E R M E D I A T E   H T M L   -   F O R M S   📑        ║
  ║                                                                          ║
  ║      [ Tables • Forms • Inputs • Validation • Form Controls & POST ]     ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

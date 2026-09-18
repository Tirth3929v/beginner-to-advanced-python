# Day 38 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██████╗   █████╗                     ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ██╔══██╗                    ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝ ╚█████╔╝                    ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗ ██╔══██╗                    ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝ ╚█████╔╝                    ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝   ╚════╝                     ║
  ║                                                                          ║
  ║        🏋️   W O R K O U T   T R A C K I N G   A P P   📊                 ║
  ║                                                                          ║
  ║      [ Nutritionix NLP • Sheety Google Sheets • Bearer Auth • Calories ] ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

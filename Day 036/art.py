# Day 36 - ASCII Art Banner
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ██╔════╝                    ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝ ███████╗                    ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗ ██╔═══██╗                   ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝ ╚██████╔╝                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝   ╚═════╝                    ║
  ║                                                                          ║
  ║       📈   S T O C K   T R A D I N G   N E W S   A L E R T   📰          ║
  ║                                                                          ║
  ║     [ Stock APIs • Price Delta % • NewsAPI • Automated Dispatch ]         ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

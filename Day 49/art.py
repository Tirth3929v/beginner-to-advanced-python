# Day 49 - ASCII Art Banner
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
  ║     ██████╗   █████╗  ██╗   ██╗     ██╗  ██╗   ██████╗                   ║
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║  ██╔════╝                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║  ███████╗                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║  ██╔═══██╗                  ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║  ╚██████╔╝                  ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝   ╚═════╝                   ║
  ║                                                                          ║
  ║       💼   A U T O   J O B   A P P L I C A T I O N S   📑                ║
  ║                                                                          ║
  ║    [ LinkedIn Easy Apply • Selenium • Form Automation • Job Hunting ]    ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

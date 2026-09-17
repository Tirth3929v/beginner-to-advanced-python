# Day 45 - ASCII Art Banner
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║  ██╔════╝                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║  ███████╗                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║  ╚════██║                   ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║  ███████║                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝  ╚══════╝                   ║
  ║                                                                          ║
  ║       🥣   W E B   S C R A P I N G   -   B E A U T I F U L S O U P   🌐  ║
  ║                                                                          ║
  ║     [ BeautifulSoup4 • HTML Parsing • CSS Selectors • Top 100 Movies ]   ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

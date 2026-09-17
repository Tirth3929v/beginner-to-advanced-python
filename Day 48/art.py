# Day 48 - ASCII Art Banner
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ██║  ██║  ██╔══██╗                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝      ███████║  ╚█████╔╝                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝       ╚════██║  ██╔══██╗                   ║
  ║     ██████╔╝ ██║  ██║    ██║             ██║  ╚█████╔╝                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝             ╚═╝   ╚════╝                    ║
  ║                                                                          ║
  ║      🤖   S E L E N I U M   C O O K I E   C L I C K E R   🍪             ║
  ║                                                                          ║
  ║    [ Selenium 4 • WebDriver • XPath • Automated Gaming AI Bot ]          ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

# Day 32 - ASCII Art Banner
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ╚════██╗                    ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝  █████╔╝                    ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗ ██╔═══╝                     ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝ ███████╗                    ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝  ╚══════╝                    ║
  ║                                                                          ║
  ║        📧   A U T O M A T E D   B I R T H D A Y   W I S H E R   🎂       ║
  ║                                                                          ║
  ║     [ smtplib • datetime • Email Automation • Dynamic Templates ]        ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

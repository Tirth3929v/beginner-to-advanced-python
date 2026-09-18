# Day 30 - ASCII Art Banner
import sys

# Ensure UTF-8 output encoding for Windows terminals
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ██╔═████╗                   ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝ ██║██╔██║                   ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗ ████╔╝██║                   ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝ ╚██████╔╝                   ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝   ╚═════╝                    ║
  ║                                                                          ║
  ║        🛡️   E R R O R S ,   E X C E P T I O N S   &   J S O N   📂       ║
  ║                                                                          ║
  ║      [ try • except • else • finally • raise • Resilient JSON Vault ]    ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

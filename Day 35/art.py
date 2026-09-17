# Day 35 - ASCII Art Banner
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
  ║     ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝     ╚════██╗ ██╔════╝                    ║
  ║     ██║  ██║ ███████║  ╚████╔╝       █████╔╝ ███████╗                    ║
  ║     ██║  ██║ ██╔══██║   ╚██╔╝        ╚═══██╗ ╚════██║                    ║
  ║     ██████╔╝ ██║  ██║    ██║        ██████╔╝ ███████║                    ║
  ║     ╚═════╝  ╚═╝  ╚═╝    ╚═╝        ╚═════╝  ╚══════╝                    ║
  ║                                                                          ║
  ║          🌧️   S M S   W E A T H E R   R A I N   A L E R T   📱           ║
  ║                                                                          ║
  ║     [ OpenWeather API • Twilio SMS • Env Vars • Hourly Weather Codes ]   ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

# Day 46 - ASCII Art Banner
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
  ║     🎵   M U S I C A L   T I M E   M A C H I N E   📻                    ║
  ║                                                                          ║
  ║   [ Billboard Hot 100 • BeautifulSoup • Spotipy • Spotify Playlists ]    ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(logo)

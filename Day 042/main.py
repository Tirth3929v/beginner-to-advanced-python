"""
Day 42 - Web Foundation: Intermediate HTML & Forms
Studio launcher to inspect tables, input schemas, and launch local browser server.
"""

import http.server
import os
import socketserver
import sys
import webbrowser
from art import logo

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PORT = 8042
HTML_FILE = os.path.join(os.path.dirname(__file__), "index.html")


def launch_web_server():
    """Starts local Python HTTP server and opens page in browser."""
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"\n🚀 Local HTTP Web Server started at: http://localhost:{PORT}")
            print("🌐 Opening HTML Form & Table Studio in your browser...")
            webbrowser.open(f"http://localhost:{PORT}/index.html")
            print("Press Ctrl+C to stop server.\n")
            httpd.serve_forever()
    except OSError:
        print(f"ℹ️ Port {PORT} is busy, opening HTML file directly...")
        webbrowser.open(f"file://{os.path.abspath(HTML_FILE)}")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Web server stopped.")


def explain_form_controls():
    """Prints a reference guide to HTML5 form validation and input attributes."""
    print("\n" + "=" * 70)
    print(" 📋 HTML5 FORM CONTROLS & VALIDATION REFERENCE")
    print("=" * 70)
    print("""
 1. text, email, password: Core inputs for textual data.
 2. required: Prevents form submission until user fills the field.
 3. minlength / maxlength: Enforces character count constraints.
 4. pattern: Applies Regular Expressions (RegEx) directly in client browser.
 5. radio vs checkbox:
    - type="radio": Single-choice selection within matching 'name' group.
    - type="checkbox": Multi-choice toggles.
 6. select & option: Dropdown menus with pre-selected defaults.
 7. textarea: Multi-line textual responses with adjustable rows/cols.
 8. range: Numeric slider for ratings and skill thresholds.
    """)
    print("=" * 70 + "\n")


def main():
    print(logo)
    print("Welcome to Day 42 - Intermediate HTML & Forms Studio! 📝📑\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🚀 Launch Local Web Server & Preview Form in Browser")
            print(" 2. 📚 View HTML5 Form Validation & Control Cheat Sheet")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                launch_web_server()
            elif choice == "2":
                explain_form_controls()
            elif choice == "3":
                print("\nExiting Day 42 Studio... Happy coding! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 42 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()

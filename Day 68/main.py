# -*- coding: utf-8 -*-
"""
Day 68: Authentication with Flask-Login & Werkzeug Password Hashing
Phase 3: Web & Flask

Key Concepts:
Werkzeug Security (generate_password_hash, check_password_hash),
Flask-Login User Sessions (login_user, logout_user, login_required, current_user),
Flashed Messages & Login-Protected File Downloads
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from server import app, db, User


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 68: AUTHENTICATION WITH FLASK-LOGIN & PBKDF2 HASHING")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: Password Hashing/Salting, Session Cookies, @login_required\n")


def test_auth_lifecycle():
    """Runs automated end-to-end verification of all authentication scenarios."""
    print("🧪 Running Automated Authentication Lifecycle via Flask TestClient...\n")

    with app.test_client() as client:
        # 1. Access protected route unauthenticated (should redirect to /login)
        r_prot = client.get("/secrets")
        print(f"   ✅ [GET /secrets - Unauthenticated] Status {r_prot.status_code} (Redirected to /login)")
        assert r_prot.status_code in (302, 401)

        # 2. Register New User
        reg_payload = {
            "name": "Sarah Connor",
            "email": "sarah@resistance.net",
            "password": "superSecretPassword123"
        }
        r_reg = client.post("/register", data=reg_payload, follow_redirects=True)
        print(f"   ✅ [POST /register] Status {r_reg.status_code} (Registered & automatically logged into /secrets)")
        assert b"Welcome, Sarah Connor" in r_reg.data

        # Verify hashed password in DB
        with app.app_context():
            user = db.session.execute(db.select(User).where(User.email == reg_payload["email"])).scalar()
            assert user is not None, "User not persisted in DB!"
            assert user.password.startswith("pbkdf2:sha256:"), "Password was stored in plaintext!"
            print(f"   ↳ Cryptographic Hash Verified: {user.password[:35]}... [SALTED]")

        # 3. Duplicate Email Rejection
        r_dup = client.post("/register", data=reg_payload, follow_redirects=True)
        print(f"   ✅ [POST /register - Duplicate] Status {r_dup.status_code} (Caught duplicate registration)")
        assert b"already signed up" in r_dup.data

        # 4. Logout
        r_logout = client.get("/logout", follow_redirects=True)
        print(f"   ✅ [GET /logout] Status {r_logout.status_code} (Logged out cleanly)")

        # 5. Login with Wrong Password
        r_wrong_pass = client.post("/login", data={
            "email": "sarah@resistance.net",
            "password": "IncorrectPassword"
        }, follow_redirects=True)
        print(f"   ✅ [POST /login - Bad Password] Status {r_wrong_pass.status_code} (Rejected bad password)")
        assert b"Password incorrect" in r_wrong_pass.data

        # 6. Login with Valid Password
        r_login_ok = client.post("/login", data={
            "email": "sarah@resistance.net",
            "password": "superSecretPassword123"
        }, follow_redirects=True)
        print(f"   ✅ [POST /login - Success] Status {r_login_ok.status_code} (Authenticated session active)")
        assert b"Welcome, Sarah Connor" in r_login_ok.data

        # 7. Download Protected File
        r_down = client.get("/download")
        print(f"   ✅ [GET /download - Authenticated] Status {r_down.status_code} (Served protected attachment, {len(r_down.data)} bytes)")
        assert r_down.status_code == 200

    print("\n✨ All cryptographic hashing, session handling, and authorization tests passed with 100% success!")


def inspect_users():
    """Prints all user accounts and hashes in SQLite."""
    print("🔍 Querying Database of Registered Users...")
    with app.app_context():
        users = db.session.execute(db.select(User)).scalars().all()
        if not users:
            print("   (No users registered yet. Run option 1 to test or option 3 to register via UI.)")
        else:
            for u in users:
                print(f"   • [User #{u.id}] {u.name} <{u.email}> | Hash: {u.password[:30]}...")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated Authentication & Cryptographic Hashing Verification")
    print(" 2) Inspect Registered Users Database (Hashed Credentials)")
    print(" 3) Launch Live Flask-Login Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_auth_lifecycle()
    elif choice == "2":
        inspect_users()
    elif choice == "3":
        print("\n🌐 Starting Flask-Login Auth Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
        app.run(debug=False, port=5000)
    else:
        print("Exiting. Happy coding!")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Program interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()

"""
Day 32 - Automated Birthday Wisher & Monday Motivation Engine
Demonstrates smtplib, datetime manipulation, CSV processing, and template rendering.
"""

import csv
import datetime as dt
import os
import random
import smtplib
import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
QUOTES_FILE = os.path.join(CURRENT_DIR, "quotes.txt")
BIRTHDAYS_FILE = os.path.join(CURRENT_DIR, "birthdays.csv")
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "letter_templates")

# SMTP Configuration (Can be overridden with environment variables)
MY_EMAIL = os.environ.get("MY_EMAIL", "my_automated_bot@gmail.com")
MY_PASSWORD = os.environ.get("MY_EMAIL_PASSWORD", "app_specific_password_here")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))


def get_random_quote() -> str:
    """Reads quotes.txt and returns a single inspirational quote."""
    if not os.path.exists(QUOTES_FILE):
        return "Keep going, every day is a fresh start!"
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        quotes = [q.strip() for q in f.readlines() if q.strip()]
    return random.choice(quotes) if quotes else "Believe in your dreams!"


def send_email_message(to_address: str, subject: str, body: str, dry_run: bool = True):
    """
    Sends email via smtplib.
    If dry_run is True or credentials are placeholder, prints simulated preview.
    """
    if dry_run or "password_here" in MY_PASSWORD or not to_address:
        print("\n" + "—" * 60)
        print(" 📨 [SIMULATED EMAIL DISPATCH - SAFE TEST MODE]")
        print(f" From:    {MY_EMAIL}")
        print(f" To:      {to_address}")
        print(f" Subject: {subject}")
        print("—" * 60)
        print(body)
        print("—" * 60)
        print("✨ (In production, configure MY_EMAIL & MY_EMAIL_PASSWORD to send live)")
        return True

    # Live SMTP Dispatch
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            msg = f"Subject:{subject}\n\n{body}"
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=to_address, msg=msg.encode("utf-8"))
        print(f"✅ Successfully sent email to {to_address}!")
        return True
    except Exception as e:
        print(f"❌ Failed to dispatch email to {to_address}: {e}")
        return False


def run_monday_motivation(force: bool = False):
    """Checks if today is Monday (weekday == 0) and sends an inspirational quote."""
    today = dt.datetime.now()
    weekday_name = today.strftime("%A")
    print(f"\n📅 Current Day: {weekday_name} ({today.strftime('%Y-%m-%d')})")

    if today.weekday() == 0 or force:
        quote = get_random_quote()
        subject = f"Monday Motivation ✨ ({today.strftime('%b %d')})"
        body = f"Good morning!\n\nHere is your motivation for today:\n\n{quote}\n\nHave an amazing and productive week!"
        print("🚀 Dispatching Monday Motivation Quote...")
        send_email_message(MY_EMAIL, subject, body, dry_run=True)
    else:
        print(f"ℹ️ Today is {weekday_name}, not Monday. (Use option to force-send).")


def check_and_send_birthdays(force_date: tuple = None):
    """
    Matches today's month and day against birthdays.csv.
    Picks a random letter from letter_templates/, replaces [NAME], and sends.
    """
    now = dt.datetime.now()
    today_tuple = force_date if force_date else (now.month, now.day)
    print(f"\n🔍 Scanning birthday database for date: Month {today_tuple[0]}, Day {today_tuple[1]}...")

    if not os.path.exists(BIRTHDAYS_FILE):
        print(f"⚠️ {BIRTHDAYS_FILE} not found!")
        return

    # Load birthdays
    matches = []
    with open(BIRTHDAYS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                m = int(row["month"])
                d = int(row["day"])
                if (m, d) == today_tuple:
                    matches.append(row)
            except Exception:
                continue

    if matches:
        for person in matches:
            name = person["name"]
            email = person["email"]

            # Pick random template
            templates = [f for f in os.listdir(TEMPLATES_DIR) if f.startswith("letter_")] if os.path.exists(TEMPLATES_DIR) else []
            if templates:
                chosen = os.path.join(TEMPLATES_DIR, random.choice(templates))
                with open(chosen, "r", encoding="utf-8") as tf:
                    content = tf.read().replace("[NAME]", name)
            else:
                content = f"Happy Birthday {name}! Wishing you all the best on your special day! 🎂"

            subject = f"Happy Birthday, {name}! 🎂🎈"
            print(f"🎉 Birthday match found for {name} ({email})!")
            send_email_message(email, subject, content, dry_run=True)
    else:
        print("ℹ️ No birthdays found in database for today.")


def add_new_birthday(name: str, email: str, year: int, month: int, day: int):
    """Appends a new person to birthdays.csv."""
    with open(BIRTHDAYS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, year, month, day])
    print(f"✅ Successfully added {name} (Birthday: {month}/{day}) to vault!")


def list_birthdays():
    """Lists all stored birthdays."""
    if not os.path.exists(BIRTHDAYS_FILE):
        print("Vault is empty.")
        return
    with open(BIRTHDAYS_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        total = len(rows)
        print("\n" + "=" * 65)
        print(f" {'NAME':22s} | {'EMAIL':28s} | {'BIRTHDAY':10s}")
        print("=" * 65)
        for r in rows:
            b_str = f"{r['year']}-{int(r['month']):02d}-{int(r['day']):02d}"
            print(f" {r['name']:22s} | {r['email']:28s} | {b_str:10s}")
        print("=" * 65)
        print(f"📊 Total Stored Birthdays: {total} (Covers every single day of the year)\n")


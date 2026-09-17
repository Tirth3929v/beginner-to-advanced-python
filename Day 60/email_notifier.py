"""
Day 60: Contact Notification Engine
Dispatches email alerts or records inquiries into a local log when users
submit the Flask contact form via HTTP POST.
"""

import os
import smtplib
from datetime import datetime
from typing import Dict, Any


class ContactNotifier:
    """Handles alert notifications for new contact form submissions."""

    def __init__(self):
        self.email = os.environ.get("MY_EMAIL", "admin@example.com")
        self.password = os.environ.get("MY_PASSWORD", "your_password_here")
        self.submissions = []

    def process_submission(self, name: str, email: str, phone: str, message: str) -> Dict[str, Any]:
        """Records submission and simulates/dispatches email."""
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "email": email,
            "phone": phone,
            "message": message
        }
        self.submissions.append(record)

        # Print simulated dispatch to console
        print(f"\n📧 [NEW CONTACT FORM INQUIRY RECEIVED]:")
        print(f"   • Timestamp : {record['timestamp']}")
        print(f"   • From      : {name} <{email}> ({phone})")
        print(f"   • Message   : \"{message}\"")

        # Try live SMTP if environment credentials configured
        if self.email != "admin@example.com" and self.password != "your_password_here":
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()
                    connection.login(self.email, self.password)
                    msg = f"Subject: New Contact Message from {name}\n\nName: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
                    connection.sendmail(from_addr=email, to_addrs=self.email, msg=msg.encode("utf-8"))
                    print("   ✅ Live email alert sent to admin inbox!")
            except Exception as e:
                print(f"   ⚠️ Live SMTP dispatch omitted: {e}")
        else:
            print("   ℹ️ Recorded in local submissions ledger (Test/Simulation Mode).")

        return record

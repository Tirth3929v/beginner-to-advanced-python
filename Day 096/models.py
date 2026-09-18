"""
Day 96: Custom API-Powered E-Commerce Store
Database Models and Catalog Seed Data
"""

import sqlite3
import os
import uuid
from typing import List, Dict, Optional, Any


def get_db_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str):
    """Initializes tables for Products, Cart, and Orders."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT,
        image_emoji TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        customer_email TEXT NOT NULL,
        subtotal REAL NOT NULL,
        discount REAL NOT NULL,
        tax REAL NOT NULL,
        total REAL NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Seed products if empty
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        seed_catalog = [
            ("Mechanical Pro Keyboard (Cherry MX Blue)", "Hardware", 149.99, 25, "Hot-swappable tactile mechanical keyboard.", "⌨️"),
            ("4K Ultrawide 34' Curved Monitor", "Displays", 599.99, 10, "Color-calibrated IPS display for multitasking.", "🖥️"),
            ("Noise-Cancelling Wireless Studio Headphones", "Audio", 249.99, 18, "Active noise cancelling with 40h battery life.", "🎧"),
            ("Ergonomic Lumbar Support Office Chair", "Furniture", 389.00, 8, "Adjustable mesh chair with 3D armrests.", "🪑"),
            ("Python Developer Plushie & Sticker Pack", "Merchandise", 29.99, 100, "Official community mascot and vinyl decals.", "🐍"),
            ("USB-C Dual 4K Docking Station (100W PD)", "Accessories", 119.50, 40, "Gigabit ethernet, HDMI 2.1, and SD reader.", "🔌")
        ]
        cur.executemany(
            "INSERT INTO products (name, category, price, stock, description, image_emoji) VALUES (?, ?, ?, ?, ?, ?)",
            seed_catalog
        )

    conn.commit()
    conn.close()


class StoreRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        init_db(self.db_path)

    def get_all_products(self) -> List[Dict[str, Any]]:
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM products ORDER BY id ASC")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_cart(self, session_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id as cart_id, c.quantity, p.id as product_id, p.name, p.price, p.image_emoji
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
        """, (session_id,))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def add_to_cart(self, session_id: str, product_id: int, quantity: int = 1) -> bool:
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        # Check stock
        cur.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
        p = cur.fetchone()
        if not p or p["stock"] < quantity:
            conn.close()
            return False

        cur.execute("SELECT id, quantity FROM cart_items WHERE session_id = ? AND product_id = ?", (session_id, product_id))
        item = cur.fetchone()
        if item:
            cur.execute("UPDATE cart_items SET quantity = quantity + ? WHERE id = ?", (quantity, item["id"]))
        else:
            cur.execute("INSERT INTO cart_items (session_id, product_id, quantity) VALUES (?, ?, ?)", (session_id, product_id, quantity))

        conn.commit()
        conn.close()
        return True

    def remove_from_cart(self, session_id: str, product_id: int):
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM cart_items WHERE session_id = ? AND product_id = ?", (session_id, product_id))
        conn.commit()
        conn.close()

    def clear_cart(self, session_id: str):
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM cart_items WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

    def checkout(self, session_id: str, email: str, promo_code: Optional[str] = None) -> Dict[str, Any]:
        cart = self.get_cart(session_id)
        if not cart:
            return {"success": False, "error": "Cart is empty."}

        subtotal = sum(item["price"] * item["quantity"] for item in cart)
        discount = 0.0
        if promo_code and promo_code.strip().upper() == "PYTHON100":
            discount = subtotal * 0.20  # 20% off

        taxable_amount = max(0.0, subtotal - discount)
        tax = taxable_amount * 0.08  # 8% sales tax
        total = taxable_amount + tax

        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (order_id, session_id, customer_email, subtotal, discount, tax, total, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'PAID_MOCK_STRIPE')
        """, (order_id, session_id, email, round(subtotal, 2), round(discount, 2), round(tax, 2), round(total, 2)))

        # Deduct stock
        for item in cart:
            cur.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item["quantity"], item["product_id"]))

        conn.commit()
        conn.close()

        self.clear_cart(session_id)

        return {
            "success": True,
            "order_id": order_id,
            "customer_email": email,
            "subtotal": round(subtotal, 2),
            "discount": round(discount, 2),
            "tax": round(tax, 2),
            "total": round(total, 2),
            "payment_gateway": "Stripe Checkout (Mock Verified)"
        }

# routes/admin_routes.py
import os
import sqlite3
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import pytz
load_dotenv()

admin_bp = Blueprint("admin", __name__)

BASE_DIR = os.getcwd()
ADMIN_DB = os.path.join(BASE_DIR, "backend", "admin.db")
MASTER_CSV = os.getenv("MASTER_CSV_PATH")

def db():
    conn = sqlite3.connect(ADMIN_DB)
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.before_app_request
def init_tables():
    conn = db()
    c = conn.cursor()

    # Categories
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            status TEXT DEFAULT 'active'
        )
    """)
    
    # Activity Log
    c.execute("""
        CREATE TABLE IF NOT EXISTS login_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            email TEXT,
            login_time TEXT
        )
    """)

    conn.commit()
    conn.close()

def log_action(user, action):
    conn = db()
    IST=pytz.timezone("Asia/Kolkata")
    conn.execute("INSERT INTO activity_log (user, action, timestamp) VALUES (?, ?, ?)",
                 (user, action, datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# ----- CATEGORY MANAGEMENT ----- #
@admin_bp.get("/categories")
def list_categories():
    conn = db()
    rows = conn.execute("SELECT id, name FROM categories").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@admin_bp.post("/categories")
def create_category():
    name = request.json.get("name")
    user = request.json.get("user", "admin")
    conn = db()
    try:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        log_action(user, f"Added Category: {name}")
        conn.close()
        return jsonify({"message": "Category Added"}), 201
    except:
        conn.close()
        return jsonify({"error": "Category already exists"}), 400

@admin_bp.delete("/categories/<int:cid>")
def delete_category(cid):
    user = request.json.get("user", "admin")
    conn = db()
    conn.execute("DELETE FROM categories WHERE id=?", (cid,))
    conn.commit()
    log_action(user, f"Deleted Category ID: {cid}")
    conn.close()
    return jsonify({"message": "Category Removed"})

# ----- USER MANAGEMENT ----- #
@admin_bp.get("/users")
def all_users():
    conn = db()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@admin_bp.put("/users/<int:uid>")
def update_user(uid):
    new_status = request.json.get("status")
    user = request.json.get("user", "admin")
    conn = db()
    conn.execute("UPDATE users SET status=? WHERE id=?", (new_status, uid))
    conn.commit()
    log_action(user, f"Changed User:{uid} Status→ {new_status}")
    conn.close()
    return jsonify({"message": "User Status Updated"})

@admin_bp.delete("/users/<int:uid>")
def delete_user(uid):
    user = request.json.get("user", "admin")
    conn = db()
    conn.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit()
    log_action(user, f"Deleted User ID:{uid}")
    conn.close()
    return jsonify({"message": "User Removed"})

@admin_bp.get("/login-activity")
def login_activity():
    conn = db()
    logs = conn.execute("SELECT user_id,email,login_time FROM login_activity ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(r) for r in logs])
# ----- SYSTEM METRICS ----- #
@admin_bp.get("/metrics")
def system_metrics():
    metrics = {}
    if os.path.exists(MASTER_CSV):
        df = pd.read_csv(MASTER_CSV)
        df["amount"] = (
            df["amount"].astype(str)
            .str.replace("Rs.", "", regex=False)
            .str.replace(",", "")
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

        metrics["total_transactions"] = len(df)
        metrics["today_transactions"] = len(df[df["date"] == datetime.today().strftime("%Y-%m-%d")])
        metrics["total_spent"] = float(df["amount"].sum())
    else:
        metrics["message"] = "Master CSV Not Found"

    conn = db()
    metrics["total_users"] = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    metrics["categories_count"] = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    conn.close()

    return jsonify(metrics)

# ----- LOGS ----- #
@admin_bp.get("/logs")
def get_logs():
    conn = db()
    logs = conn.execute("SELECT * FROM activity_log ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(r) for r in logs])
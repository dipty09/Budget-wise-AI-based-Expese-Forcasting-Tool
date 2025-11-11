# backend/db_admin_init.py
import sqlite3, os

BASE = os.getcwd()
ADMIN_DB = os.path.join(BASE, "backend", "admin.db")
os.makedirs(os.path.dirname(ADMIN_DB), exist_ok=True)

conn = sqlite3.connect(ADMIN_DB)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    keywords TEXT
)
""")
c.execute("""
        CREATE TABLE IF NOT EXISTS login_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            email TEXT,
            login_time TEXT
        )
    """)
c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            status TEXT DEFAULT 'active'
        )
    """)
    
defaults = [
    ("Food & Dining", "restaurant,food,grocery,cafe"),
    ("Transportation", "uber,ola,train,bus,flight,fuel"),
    ("Utilities", "electricity,water,internet,bill"),
    ("Rent & Housing", "rent,apartment,lease"),
    ("Shopping", "amazon,flipkart,clothes"),
    ("Healthcare", "hospital,doctor,pharmacy"),
    ("Entertainment", "netflix,movie,music"),
    ("Salary / Income", "salary,income,credit,deposit")
]

for name, kw in defaults:
    try:
        c.execute("INSERT INTO categories (name, keywords) VALUES (?, ?)", (name, kw))
    except sqlite3.IntegrityError:
        pass

conn.commit()
conn.close()
print("✅ Admin DB initialized and seeded:", ADMIN_DB)
import os
import pytz
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import jwt,sqlite3
from datetime import datetime,timedelta
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# --- Helper: Write Login Event into admin.db ---
def log_login_activity(email, user_id):
    admin_db_path = os.path.join(os.getcwd(), "backend", "admin.db")
    conn = sqlite3.connect(admin_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            email TEXT,
            login_time TEXT
        )
    """)
    login_time=datetime.utcnow().strftime("%Y-%m-%d %H-%m-%S ")
    cursor.execute("INSERT INTO login_activity (user_id, email, login_time) VALUES (?, ?, ?)",
                   (user_id, email, login_time))
    conn.commit()
    conn.close()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email, password = data.get('email'), data.get('password')
    if not email or not password:
        return jsonify({"error:Email and password required"}),400
    hashed_password = generate_password_hash(password)

    
    # --- Store user in main app DB (budgetwise.db) ---
    conn = sqlite3.connect('budgetwise.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
        user_id = cursor.lastrowid   # ✅ capture new user id

    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already exists!"}), 409

    conn.close()

    # --- Also insert user into admin.db for Admin Panel ---
    admin_db_path = os.path.join(os.getcwd(), "backend", "admin.db")
    conn_admin = sqlite3.connect(admin_db_path)
    cursor_admin = conn_admin.cursor()

    cursor_admin.execute("""
        INSERT INTO users (id, name, email, status)
        VALUES (?, ?, ?, 'active')
    """, (user_id, email.split("@")[0], email))  # Use email prefix as name

    conn_admin.commit()
    conn_admin.close()

    return jsonify({"message": "User registered ✅"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')

    conn = sqlite3.connect('budgetwise.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):

        # ✅ Log login to admin.db (This is the key correction)
        log_login_activity(email, user[0])
        token = jwt.encode(
            {'user_id': user[0], 'exp': datetime.now() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        conn.close()
        return jsonify({'token': token, 'user_id': user[0], 'email': email, "message": "Login Successful ✅"}), 200

    conn.close()
    return jsonify({'error': 'Invalid credentials ❌'}), 401
@auth_bp.route('/login-activity', methods=['GET'])
def get_login_activity():
    admin_db_path=os.path.join(os.getcwd(),"backend","admin.db")
    conn = sqlite3.connect(admin_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, email, login_time FROM login_activity ORDER BY login_time DESC")
    records = cursor.fetchall()
    conn.close()

    # Convert to JSON list
    activity_list = [
        {"user_id": row[0], "email": row[1], "login_time": row[2]}
        for row in records
    ]

    return jsonify(activity_list), 200
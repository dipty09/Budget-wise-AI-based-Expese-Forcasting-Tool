import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import jwt, datetime, sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email, password = data.get('email'), data.get('password')
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('budgetwise.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists!"}), 400
    finally:
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')

    conn = sqlite3.connect('budgetwise.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401
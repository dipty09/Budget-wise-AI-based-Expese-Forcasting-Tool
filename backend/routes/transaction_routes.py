from flask import Blueprint, request, jsonify
import jwt,os,sqlite3

transaction_bp = Blueprint('transaction', __name__)
SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = decoded['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(user_id, *args, **kwargs)
    return wrapper


@transaction_bp.route('/add', methods=['POST'])
@token_required
def add_transaction(user_id):
    data = request.json
    conn = sqlite3.connect('budgetwise.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (user_id, date, amount, category, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, data['date'], data['amount'], data['category'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Transaction added successfully'}), 201
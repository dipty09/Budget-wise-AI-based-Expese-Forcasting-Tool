import os
import streamlit as st
from dotenv import load_dotenv 
from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp
from models.db import init_db

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

init_db()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(transaction_bp, url_prefix='/transaction')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
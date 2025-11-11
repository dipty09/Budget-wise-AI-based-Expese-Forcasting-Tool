import os
import streamlit as st
from dotenv import load_dotenv 
from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp
from routes.admin_routes import admin_bp
from models.db import init_db

load_dotenv()
def create_app():
   app = Flask(__name__)
   CORS(app)
   app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

   init_db()

# Register blueprints
   app.register_blueprint(auth_bp, url_prefix='/auth')
   app.register_blueprint(transaction_bp, url_prefix='/transaction')
   app.register_blueprint(admin_bp,url_prefix='/admin')
   return app
app=create_app()

if __name__ == '__main__':
    print("Backend server is running at http://127.0.0.0.1:5000")
    app.run(debug=True, port=5000)
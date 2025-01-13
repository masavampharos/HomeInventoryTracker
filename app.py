import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import logging

load_dotenv()

app = Flask(__name__)

# ログ設定
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# セッション設定
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Supabase PostgreSQL接続設定
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_DB_PASSWORD = os.environ.get('SUPABASE_DB_PASSWORD')
DB_URL = f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.{SUPABASE_URL.replace('https://', '')}/postgres"

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key')

db = SQLAlchemy(app)

# モデルのインポート
from models import Item, ConsumptionLog

# ルートのインポート
from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=False)
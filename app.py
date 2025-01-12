import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
import logging

app = Flask(__name__)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# セッション設定
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# シークレットキーの設定
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change-in-production')

# MySQLデータベース設定
mysql_user = 'masavampharos'
mysql_password = os.getenv('MYSQL_PASSWORD')  # MySQLのパスワードを環境変数から取得
mysql_host = 'masavampharos.mysql.pythonanywhere-services.com'
mysql_database = 'masavampharos$default'

# データベースURLの構築（mysql-connector-pythonを使用）
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベース接続のログ出力
logger.info(f"Connecting to database at: {mysql_host}")

# SQLAlchemyの初期化
db = SQLAlchemy(app)

# モデルのインポート
from models import Item, ConsumptionLog

# ルートのインポート
from routes import *

# データベース初期化
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
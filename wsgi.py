import os
import sys

# プロジェクトのパスを追加
path = '/home/masavampharos/HomeInventoryTracker'
if path not in sys.path:
    sys.path.append(path)

# 環境変数の設定
os.environ['FLASK_SECRET_KEY'] = 'dev-key-please-change-in-production'
os.environ['MYSQL_USER'] = 'masavampharos'
os.environ['MYSQL_PASSWORD'] = 'ecm0nef*euq4vzx-BHE'
os.environ['MYSQL_DATABASE'] = 'masavampharos$default'

# アプリケーションのインポート
from app import app as application
application.secret_key = os.environ['FLASK_SECRET_KEY'] 
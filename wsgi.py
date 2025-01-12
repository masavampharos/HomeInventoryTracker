import os
import sys

# アプリケーションのパスを設定
path = '/home/YOUR_USERNAME/HomeInventoryTracker'
if path not in sys.path:
    sys.path.append(path)

# アプリケーションインスタンスをインポート
from app import app as application

# 環境変数を設定
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0' 
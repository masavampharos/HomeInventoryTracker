import os
import sys

# PythonAnywhereのユーザー名に応じてパスを変更する必要があります
path = '/home/YOUR_USERNAME/HomeInventoryTracker'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

# 環境変数の設定
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0' 
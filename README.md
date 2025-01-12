# Home Inventory Tracker

家庭内の在庫管理を簡単に行うためのWebアプリケーションです。

## 機能

- 在庫アイテムの追加・編集・削除
- 在庫レベルの視覚的な管理
- 消費ログの記録
- 最小在庫数の設定と警告
- ドラッグ&ドロップによる並び替え

## 技術スタック

- Backend: Python/Flask
- Database: PostgreSQL
- Frontend: HTML/CSS/JavaScript

## セットアップ手順

1. リポジトリのクローン:
```bash
git clone https://github.com/masavampharos/HomeInventoryTracker.git
cd HomeInventoryTracker
```

2. 仮想環境の作成と有効化:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

4. PostgreSQLのセットアップ:
```bash
createdb home_inventory
```

5. 環境変数の設定:
`.env`ファイルを作成し、以下の内容を設定:
```
FLASK_SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/home_inventory
FLASK_DEBUG=1
```

6. アプリケーションの実行:
```bash
python app.py
```

## デプロイ

PythonAnywhereでのデプロイ手順は[こちら](https://help.pythonanywhere.com/pages/Flask/)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 
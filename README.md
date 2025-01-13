# Home Inventory Tracker

日用品の在庫管理をシンプルに行えるWebアプリケーション

## 機能

- アイテムの追加、編集、削除
- 在庫レベルの視覚的管理
- 消費ログの記録
- 最小在庫アラート
- ドラッグ&ドロップでの並び替え

## 技術スタック

- バックエンド: Python/Flask
- データベース: PostgreSQL (Supabase)
- フロントエンド: HTML/CSS/JavaScript
- デプロイ: Render.com

## ローカルでの実行方法

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

4. 環境変数の設定:
`.env`ファイルを作成し、以下の変数を設定:
```
FLASK_SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_DB_PASSWORD=your-database-password
```

5. アプリケーションの実行:
```bash
python app.py
```

## デプロイ手順

### Supabase設定

1. Supabaseでプロジェクトを作成
2. SQL Editorで以下のテーブルを作成:
   - `item`: アイテム管理用テーブル
   - `consumption_log`: 消費ログ用テーブル
3. 接続情報を取得:
   - Database URL
   - Database Password

### Render.com設定

1. Render.comでアカウント作成
2. 「New Web Service」を選択
3. GitHubリポジトリを連携
4. 環境変数を設定:
   - `FLASK_SECRET_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_DB_PASSWORD`
5. デプロイを実行

## デプロイ済みURL

https://homeinventorytracker.onrender.com

## ライセンス

MIT License 
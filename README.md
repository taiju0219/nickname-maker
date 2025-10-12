# Nickname Maker

あだ名生成アプリケーション

## 概要
このアプリケーションは、データベースに保存されたあだ名リストからランダムに1つを取得するシンプルなAPIです。
aiohttpとPostgreSQLを使用したバックエンドAPIを提供します。

## 機能
- ランダムなあだ名の取得
- PostgreSQLデータベースによるあだ名管理
- シンプルなGET APIエンドポイント
- CORS対応

## セットアップ

### 1. 依存関係のインストール
```bash
cd backend
pip install -r requirements.txt
```

### 2. PostgreSQLのセットアップ
1. PostgreSQLをインストール
    - https://www.postgresql.org/download/windows/
    - Download the installerよりver 18.0のWindoews x86-64版をダウンロード
    - 画面の指示に従いServerの18.0をインストール
    - スタックビルダが立ち上がった場合以下の3つを選択して『次へ』
      - Add-ons, tools and utilitiesより『pgBouncer v1.24.1-1』
        - 接続プール管理(オプション)に必要、パフォーマンス向上に役立つ
      - DataBase Driversより『psqlODBC(64 bit)v13.02.0000-1』
        - PythonのasyncpgライブラリがPostgre SQLに接続するために使用
      - DataBase Serverより『PostgreSQL(64 bit)v18.0-2』「
        - DataBaseのコア機能、ポスグレ本体
    - スタックビルダで設定した3つのアプリをインストールするためのウィンドウが順に立ち上がるので画面の指示ししたがって設定
    - インストール後`psql --version`
      - psqlがコマンドとして認識されなかった場合
        1. インストールされているか確認
          パスを直接指定して存在確認
          - `cd "C:\Program Files\PostgreSQL\18\bin"`
          - `.\psql.exe --version`
        2. 環境変数に追加
          - 『Win+R』→`sysdm.cpl`→Enter
          - 『詳細設定』→『環境変数』
          - 『システム環境変数』→『Path』を選択し『編集』
          - 『新規追加』→『C:\Program Files\PostgreSQL\18\bin』を追加して『OK』
          - PowerShellを再起動し、再度`psql --version`(念のためPCも再起動すると〇)
2. データベースを作成:
```sql
CREATE DATABASE nickname_maker;
```

### 3. 環境変数の設定
`.env.example`を`.env`にコピーして設定を編集:
```bash
cp .env.example .env
```

`.env`ファイルでデータベース接続情報を設定:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nickname_maker
DB_USER=postgres
DB_PASSWORD=your_password_here
```

- DBのパスワードを`./backend/.env`に設定する
- 最上階層に『.gitignore』というファイルを作成した後、中に『.backend/.env』と記述
  - これにより、gitのステージングなどの対象から、環境設定ファイル『.env』が除外される

### 4. サーバーの起動
```bash
python main.py
```

## APIエンドポイント

### GET /nickname
ランダムなあだ名を取得します。

**レスポンス:**
```json
{
  "nickname": "スーパー"
}
```

### GET /health
サーバーのヘルスチェック

**レスポンス:**
```json
{
  "status": "healthy",
  "message": "あだ名メーカーAPIは正常に動作しています"
}
```

## プロジェクト構造
```
backend/
├── main.py              # メインサーバーファイル
├── database.py          # データベース操作
├── config.py            # 設定管理
├── requirements.txt     # 依存関係
└── .env.example        # 環境変数テンプレート
```

## ライセンス
MIT License

#!/usr/bin/env python3
"""
データベース初期化スクリプト
PostgreSQL 18.0.2用
"""
import asyncio
import asyncpg
from config import Config

async def create_database():
    """データベースを作成"""
    config = Config()
    
    # まずpostgresデータベースに接続してデータベースを作成
    try:
        conn = await asyncpg.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database='postgres',  # デフォルトデータベース
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        
        # データベースが存在するかチェック
        result = await conn.fetchval("""
            SELECT 1 FROM pg_database WHERE datname = $1
        """, config.DB_NAME)
        
        if not result:
            await conn.execute(f'CREATE DATABASE {config.DB_NAME}')
            print(f"データベース '{config.DB_NAME}' を作成しました")
        else:
            print(f"データベース '{config.DB_NAME}' は既に存在します")
        
        await conn.close()
        
    except Exception as e:
        print(f"データベース作成エラー: {e}")
        return False
    
    return True

async def init_tables():
    """テーブルとデータを初期化"""
    config = Config()
    
    try:
        conn = await asyncpg.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        
        # テーブル作成
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS nicknames (
                id SERIAL PRIMARY KEY,
                nickname VARCHAR(50) NOT NULL UNIQUE
            );
        """)
        
        # あだ名データの挿入
        nicknames = [
            "超", "スーパー", "メガ", "ウルトラ", "ハイパー", "エクストラ",
            "ミスター", "ミス", "ドクター", "プロ", "マスター", "キング",
            "クイーン", "プリンセス", "プリンス", "チャンピオン", "ヒーロー",
            "レジェンド", "エース", "スター", "ダイヤモンド", "ゴールド",
            "シルバー", "プラチナ", "クリスタル", "レインボー", "サンシャイン",
            "ムーンライト", "ファイア", "アイス", "サンダー", "ストーム"
        ]
        
        for nickname in nicknames:
            await conn.execute("""
                INSERT INTO nicknames (nickname) 
                VALUES ($1) 
                ON CONFLICT (nickname) DO NOTHING
            """, nickname)
        
        print("テーブルとデータの初期化が完了しました")
        await conn.close()
        
    except Exception as e:
        print(f"テーブル初期化エラー: {e}")
        return False
    
    return True

async def main():
    """メイン処理"""
    print("PostgreSQL 18.0.2 データベース初期化を開始します...")
    
    # データベース作成
    if await create_database():
        # テーブル初期化
        if await init_tables():
            print("データベース初期化が完了しました！")
        else:
            print("テーブル初期化に失敗しました")
    else:
        print("データベース作成に失敗しました")

if __name__ == "__main__":
    asyncio.run(main())


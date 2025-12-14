import asyncpg
import asyncio
from config import Config

class Database:
    def __init__(self):
        self.pool = None
        self.config = Config()
    
    async def create_pool(self):
        """データベース接続プールを作成"""
        try:
            self.pool = await asyncpg.create_pool(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                min_size=1,
                max_size=10
            )
            print("データベース接続プールが作成されました")
        except Exception as e:
            print(f"データベース接続エラー: {e}")
            raise
    
    async def close_pool(self):
        """データベース接続プールを閉じる"""
        if self.pool:
            await self.pool.close()
            print("データベース接続プールが閉じられました")
    
    async def init_database(self):
        """データベースとテーブルを初期化"""
        try:
            async with self.pool.acquire() as conn:
                # テーブル作成
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS nicknames (
                        id SERIAL PRIMARY KEY,
                        nickname VARCHAR(50) NOT NULL UNIQUE
                    );
                """)
                
                # あだ名データの挿入（重複チェック付き）
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
                
                print("データベースの初期化が完了しました")
                
        except Exception as e:
            print(f"データベース初期化エラー: {e}")
            raise
    
    async def get_random_nickname(self):
        """ランダムなあだ名を取得"""
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchrow("""
                    SELECT nickname FROM nicknames 
                    ORDER BY RANDOM() 
                    LIMIT 1
                """)
                return result['nickname'] if result else "スーパー"
        except Exception as e:
            print(f"あだ名取得エラー: {e}")
            return "スーパー"  # フォールバック

# グローバルデータベースインスタンス
db = Database()

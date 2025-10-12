import aiohttp
from aiohttp import web
from aiohttp_cors import setup as cors_setup, ResourceOptions
import asyncio
from database import db
from config import Config

class NicknameMakerAPI:
    def __init__(self):
        self.config = Config()
        self.app = None
    
    async def create_app(self):
        """aiohttpアプリケーションを作成"""
        self.app = web.Application()
        
        # CORS設定
        cors = cors_setup(self.app, defaults={
            "*": ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # ルート設定
        self.app.router.add_get('/nickname', self.get_random_nickname)
        self.app.router.add_get('/health', self.health_check)
        
        # CORSをすべてのルートに適用
        for route in list(self.app.router.routes()):
            cors.add(route)
        
        return self.app
    
    async def get_random_nickname(self, request):
        """ランダムなあだ名を取得するエンドポイント"""
        try:
            # ランダムなあだ名を取得
            nickname = await db.get_random_nickname()
            
            return web.json_response({
                'nickname': nickname
            })
            
        except Exception as e:
            print(f"エラー: {e}")
            return web.json_response(
                {'error': 'サーバー内部エラーが発生しました'}, 
                status=500
            )
    
    async def health_check(self, request):
        """ヘルスチェックエンドポイント"""
        return web.json_response({
            'status': 'healthy',
            'message': 'あだ名メーカーAPIは正常に動作しています'
        })

async def init_database():
    """データベースを初期化"""
    try:
        await db.create_pool()
        await db.init_database()
        print("データベースの初期化が完了しました")
    except Exception as e:
        print(f"データベース初期化エラー: {e}")
        raise

async def cleanup_database():
    """データベース接続をクリーンアップ"""
    await db.close_pool()

async def create_app():
    """アプリケーションを作成して初期化"""
    api = NicknameMakerAPI()
    app = await api.create_app()
    
    # データベース初期化
    await init_database()
    
    # クリーンアップ処理を追加
    app.on_cleanup.append(cleanup_database)
    
    return app

def main():
    """メイン関数"""
    config = Config()
    
    print(f"あだ名メーカーAPIサーバーを開始します...")
    print(f"サーバーアドレス: http://{config.HOST}:{config.PORT}")
    print(f"エンドポイント:")
    print(f"  POST /generate-nickname - あだ名生成")
    print(f"  GET  /health - ヘルスチェック")
    
    # サーバー起動
    web.run_app(create_app(), host=config.HOST, port=config.PORT)

if __name__ == '__main__':
    main()

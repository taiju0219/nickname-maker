import aiohttp
from aiohttp import web
from aiohttp_cors import setup as cors_setup, ResourceOptions
import asyncio
import os
import json
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
        
        # フロントエンド用の静的ファイル配信
        self.app.router.add_get('/', self.serve_index)
        self.app.router.add_static('/', path='../frontend', name='static')
        
        # CORSをすべてのルートに適用
        for route in list(self.app.router.routes()):
            cors.add(route)
        
        return self.app
    
    async def get_random_nickname(self, request):
        """ランダムなあだ名を取得するエンドポイント"""
        try:
            # ランダムなあだ名を取得
            nickname = await db.get_random_nickname()
            
            # 日本語対応のJSONレスポンス
            json_data = json.dumps({
                'nickname': nickname
            }, ensure_ascii=False)
            
            return web.Response(
                text=json_data,
                content_type='application/json',
                charset='utf-8'
            )
            
        except Exception as e:
            print(f"エラー: {e}")
            error_data = json.dumps({
                'error': 'サーバー内部エラーが発生しました'
            }, ensure_ascii=False)
            
            return web.Response(
                text=error_data,
                content_type='application/json',
                charset='utf-8',
                status=500
            )
    
    async def health_check(self, request):
        """ヘルスチェックエンドポイント"""
        health_data = json.dumps({
            'status': 'healthy',
            'message': 'あだ名メーカーAPIは正常に動作しています'
        }, ensure_ascii=False)
        
        return web.Response(
            text=health_data,
            content_type='application/json',
            charset='utf-8'
        )
    
    async def serve_index(self, request):
        """フロントエンドのindex.htmlを配信"""
        try:
            # フロントエンドのindex.htmlを読み込み
            frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
            with open(frontend_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return web.Response(text=content, content_type='text/html')
        except FileNotFoundError:
            return web.Response(text="<h1>フロントエンドファイルが見つかりません</h1>", content_type='text/html')

async def init_database():
    """データベースを初期化"""
    try:
        await db.create_pool()
        await db.init_database()
        print("データベースの初期化が完了しました")
    except Exception as e:
        print(f"データベース初期化エラー: {e}")
        raise

async def cleanup_database(app):
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
    print(f"フロントエンド: http://localhost:{config.PORT}")
    print(f"エンドポイント:")
    print(f"  GET  /nickname - ランダムなあだ名取得")
    print(f"  GET  /health - ヘルスチェック")
    print(f"  GET  / - フロントエンド表示")
    
    # サーバー起動
    web.run_app(create_app(), host=config.HOST, port=config.PORT)

if __name__ == '__main__':
    main()

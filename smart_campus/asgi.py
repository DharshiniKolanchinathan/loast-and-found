import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_campus.settings")

django.setup()

import chat.routing

class DebugMiddleware:
    def __init__(self, inner):
        self.inner = inner
    async def __call__(self, scope, receive, send):
        try:
            if scope['type'] == 'websocket':
                print(f"DEBUG: WebSocket request received for path: {scope['path']}")
                # print(f"DEBUG: Headers: {dict(scope.get('headers', []))}")
            return await self.inner(scope, receive, send)
        except Exception as e:
            print(f"DEBUG: ASGI Middleware Error: {e}")
            raise e

print("ASGI application loading...")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": DebugMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})

print("ASGI application loaded.")
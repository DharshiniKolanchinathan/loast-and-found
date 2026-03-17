import os
import django
import asyncio
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_campus.settings")
django.setup()

from smart_campus.asgi import application

async def test_app():
    print("Testing ASGI application instantiation...")
    try:
        # Just check if 'websocket' is in the protocol router
        if 'websocket' in application.application_mapping:
            print("SUCCESS: WebSocket protocol router found.")
        else:
            print("FAILURE: WebSocket protocol router missing.")
            
        if 'http' in application.application_mapping:
            print("SUCCESS: HTTP protocol router found.")
        else:
            print("FAILURE: HTTP protocol router missing.")
            
    except Exception as e:
        print(f"ERROR during test: {e}")

if __name__ == "__main__":
    asyncio.run(test_app())

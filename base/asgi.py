# mysite/asgi.py
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


from chats.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
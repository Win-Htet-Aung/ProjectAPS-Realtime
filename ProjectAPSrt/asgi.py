"""
ASGI config for ProjectAPS-Realtime project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter  # for channels
from django.core.asgi import get_asgi_application
import DataManagement.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjectAPSrt.settings')

application = get_asgi_application()
# application = ProtocolTypeRouter(
#     {
#         'http': get_asgi_application(),
#         'websocket': AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#                 URLRouter(
#                     DataManagement.routing.websocket_urlpatterns
#                 )
#             ),
#         ),
#     }
# )

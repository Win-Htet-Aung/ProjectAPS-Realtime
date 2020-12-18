from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/dataplotter/<str:serial>/', consumers.DataPlotter.as_asgi()),
]

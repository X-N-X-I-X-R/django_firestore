# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import re_path
# from channels.auth import AuthMiddlewareStack
# from myapp import consumers  # Corrected import statement

# websocket_urlpatterns = [
#   re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#   # (http->django views is added by default)
#   'websocket': AuthMiddlewareStack(
#     URLRouter(
#       websocket_urlpatterns
#     )
#   ),
# })
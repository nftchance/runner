from django.core.asgi import get_asgi_application

from django.urls import path # new

from channels.routing import ProtocolTypeRouter, URLRouter # changed

from runner.middleware import TokenAuthMiddlewareStack 

from org.consumers import OrgConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            path('org/', OrgConsumer.as_asgi()),
        ])
    ),
})
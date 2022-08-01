from django.core.asgi import get_asgi_application

from django.urls import path # new

from channels.routing import ProtocolTypeRouter, URLRouter # changed

from runner.middleware import TokenAuthMiddlewareStack 

from runner.consumers import RunnerConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            path('runner/', RunnerConsumer.as_asgi()),
        ])
    ),
})
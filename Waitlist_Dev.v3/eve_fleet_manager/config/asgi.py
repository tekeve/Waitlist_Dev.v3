import os
from django.core.asgi import get_asgi_application

# 1. Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# 3. Import Channels and EventStream dependencies (must happen after get_asgi_application)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django_eventstream

# 4. Define the routing configuration
application = ProtocolTypeRouter({
    'http': URLRouter([
        # Intercept requests to /events/ and handle them with EventStream (SSE)
        # AuthMiddlewareStack ensures 'request.user' is available in the consumer
        path('events/', AuthMiddlewareStack(URLRouter(django_eventstream.routing.urlpatterns))),
        
        # All other HTTP requests go to the standard Django app
        re_path(r'', django_asgi_app),
    ]),
    # We will add 'websocket': ... here in the future if we need two-way websockets
})
from django.contrib import admin
from django.urls import path, include
import django_eventstream

urlpatterns = [
    # Admin Dashboard
    path('admin/', admin.site.urls),

    # EVE Online SSO (handled by django-esi)
    # This provides the /sso/callback/ endpoint we set in .env
    path('sso/', include('esi.urls', namespace='esi')),

    # Real-time Events (Server-Sent Events)
    # We include this here so 'reverse("events")' works in templates
    # The actual handling is done in asgi.py
    path('events/', include(django_eventstream.urls), {'channels': ['global']}),

    # Your Custom Apps
    path('', include('core.urls')),           # Landing page
    path('auth/', include('eve_auth.urls')),  # Alt management
    path('fleets/', include('fleets.urls')),  # The main fleet tool
    # path('sde/', include('sde.urls')),      # (Optional) if you build a public SDE browser
]
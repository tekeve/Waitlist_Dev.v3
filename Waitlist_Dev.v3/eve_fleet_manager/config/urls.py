from django.contrib import admin
from django.urls import path, include
from esi.views import sso_redirect
from eve_auth.views import login_callback, logout_user # Import the new view
import django_eventstream

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth Routes
    path('sso/callback/', login_callback, name='sso_callback'),
    path('sso/login/', sso_redirect, name='sso_login'),
    path('logout/', logout_user, name='logout'), # New Logout Route

    # The rest of ESI
    path('sso/', include('esi.urls', namespace='esi')),

    # Real-time Events
    path('events/', include(django_eventstream.urls), {'channels': ['global']}),

    # Apps
    path('', include('core.urls')),           
    path('auth/', include('eve_auth.urls')),
    path('fleets/', include('fleets.urls')),
]
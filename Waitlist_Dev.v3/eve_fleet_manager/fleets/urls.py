from django.urls import path
from . import views

app_name = 'fleets'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
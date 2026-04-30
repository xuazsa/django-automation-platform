from django.urls import path
from . import api_views

urlpatterns = [
    path('switch/backup/', api_views.switch_backup, name='api_switch_backup'),
]

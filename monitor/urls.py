from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/metrics/', views.get_system_metrics, name='api_metrics'),
    path('api/services/', views.get_service_status, name='api_services'),
    path('api/history/', views.get_metrics_history, name='api_history'),
    path('api/rules/', views.get_alert_rules, name='api_rules'),
    path('api/rules/create/', views.create_alert_rule, name='api_create_rule'),
    path('alerts/', views.alert_rules, name='alert_rules'),
]

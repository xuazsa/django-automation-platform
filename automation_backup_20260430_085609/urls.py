from django.urls import path
from . import views

app_name = 'automation'

urlpatterns = [
    path('', views.switch_list, name='dashboard'),
    path('switches/', views.switch_list, name='switch_list'),
]

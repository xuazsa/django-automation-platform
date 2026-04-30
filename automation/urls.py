from django.urls import path
from . import views
from . import views_python

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('tasks/run/<int:pk>/', views.task_run, name='task_run'),
    path('switches/', views.switch_list, name='switch_list'),
    path('python/', views_python.python_console, name='python_console'),
    path('api/execute_python/', views_python.execute_python, name='execute_python'),
    path('api/switch/backup/', views.switch_backup, name='api_switch_backup'),
]

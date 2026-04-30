from django.contrib import admin
from .models import Task, TaskLog, Switch

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'task_type', 'status', 'last_run')

@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'start_time', 'status')

@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip_address', 'vendor', 'status', 'last_seen')
    list_filter = ('vendor', 'status')
    search_fields = ('name', 'ip_address')

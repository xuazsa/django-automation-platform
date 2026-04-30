from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, TaskLog
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    tasks = Task.objects.all()
    total_tasks = tasks.count()
    active_tasks = tasks.filter(status='active').count()
    
    logs = TaskLog.objects.all()
    total_logs = logs.count()
    success_logs = logs.filter(status='success').count()
    success_rate = round(success_logs / total_logs * 100, 2) if total_logs > 0 else 0
    
    # 最近7天执行统计
    today = datetime.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    day_labels = [d.strftime('%m-%d') for d in reversed(last_7_days)]
    day_counts = []
    for d in reversed(last_7_days):
        count = TaskLog.objects.filter(start_time__date=d).count()
        day_counts.append(count)
    
    recent_logs = TaskLog.objects.all()[:10]
    
    context = {
        'total_tasks': total_tasks,
        'active_tasks': active_tasks,
        'total_logs': total_logs,
        'success_rate': success_rate,
        'day_labels': day_labels,
        'day_counts': day_counts,
        'recent_logs': recent_logs,
    }
    return render(request, 'automation/dashboard.html', context)

from django.shortcuts import render, redirect
from .models import Task, TaskLog
import subprocess

def dashboard(request):
    total_tasks = Task.objects.count()
    active_tasks = Task.objects.filter(status='active').count()
    recent_logs = TaskLog.objects.all().order_by('-start_time')[:10]
    return render(request, 'automation/dashboard.html', {
        'total_tasks': total_tasks,
        'active_tasks': active_tasks,
        'recent_logs': recent_logs,
    })

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'automation/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        Task.objects.create(
            name=request.POST.get('name'),
            task_type=request.POST.get('task_type'),
            command=request.POST.get('command'),
            cron_expr=request.POST.get('cron_expr', ''),
            status=request.POST.get('status', 'active'),
        )
        return redirect('task_list')
    return render(request, 'automation/task_form.html')

def task_delete(request, pk):
    Task.objects.filter(pk=pk).delete()
    return redirect('task_list')

def task_run(request, pk):
    task = Task.objects.get(pk=pk)
    log = TaskLog.objects.create(task=task, status='running')
    try:
        result = subprocess.run(task.command, shell=True, capture_output=True, text=True, timeout=60)
        log.output = result.stdout[:5000]
        log.error = result.stderr[:500]
        log.status = 'success' if result.returncode == 0 else 'failed'
    except Exception as e:
        log.status = 'failed'
        log.error = str(e)
    log.end_time = None
    log.save()
    task.last_run = log.start_time
    task.save()
    return redirect('task_list')

def python_console(request):
    from django.http import HttpResponse
    return HttpResponse("Python 执行器页面（待完善）")

def python_console(request):
    from django.shortcuts import render
    return render(request, 'automation/python_console.html')

def switch_list(request):
    from .models import Switch
    switches = Switch.objects.all()
    return render(request, 'automation/switch_list.html', {'switches': switches})

def switch_list(request):
    from .models import Switch
    switches = Switch.objects.all()
    return render(request, 'automation/switch_list.html', {'switches': switches})

def switch_backup(request):
    from django.http import JsonResponse
    from .models import Switch
    import json
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            switch = Switch.objects.get(pk=data.get('switch_id'))
            # 模拟备份成功
            return JsonResponse({'success': True, 'message': f'交换机 {switch.name} 备份成功'})
        except:
            return JsonResponse({'success': False, 'error': '备份失败'})
    return JsonResponse({'success': False, 'error': '方法不允许'})

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Metric, AlertRule
import psutil
import json
from datetime import datetime, timedelta

def dashboard(request):
    """监控仪表盘"""
    return render(request, 'monitor/dashboard.html')

def get_system_metrics(request):
    """获取系统指标"""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # 内存
    mem = psutil.virtual_memory()
    
    # 磁盘
    disk = psutil.disk_usage('/')
    
    # 网络
    net = psutil.net_io_counters()
    
    # 保存到数据库
    Metric.objects.create(
        name='cpu_usage',
        metric_type='cpu',
        value=cpu_percent,
        unit='%'
    )
    Metric.objects.create(
        name='memory_usage',
        metric_type='memory',
        value=mem.percent,
        unit='%'
    )
    Metric.objects.create(
        name='disk_usage',
        metric_type='disk',
        value=disk.percent,
        unit='%'
    )
    
    return JsonResponse({
        'cpu': cpu_percent,
        'memory': mem.percent,
        'memory_used': mem.used // (1024**2),
        'memory_total': mem.total // (1024**2),
        'disk': disk.percent,
        'disk_used': disk.used // (1024**3),
        'disk_total': disk.total // (1024**3),
        'network_sent': net.bytes_sent // (1024**2),
        'network_recv': net.bytes_recv // (1024**2),
    })

def get_service_status(request):
    """获取服务状态"""
    import subprocess
    
    services = ['nginx', 'mysqld', 'php-fpm']
    status = {}
    
    for service in services:
        result = subprocess.run(
            ['systemctl', 'is-active', service],
            capture_output=True, text=True
        )
        status[service] = result.stdout.strip() == 'active'
    
    return JsonResponse(status)

def get_metrics_history(request):
    """获取历史指标数据"""
    hours = int(request.GET.get('hours', 24))
    start_time = datetime.now() - timedelta(hours=hours)
    
    metrics = Metric.objects.filter(recorded_at__gte=start_time).order_by('recorded_at')
    
    data = {}
    for metric in metrics:
        if metric.name not in data:
            data[metric.name] = {'times': [], 'values': []}
        data[metric.name]['times'].append(metric.recorded_at.strftime('%H:%M'))
        data[metric.name]['values'].append(metric.value)
    
    return JsonResponse(data)

@csrf_exempt
def create_alert_rule(request):
    """创建告警规则"""
    if request.method == 'POST':
        data = json.loads(request.body)
        rule = AlertRule.objects.create(
            name=data['name'],
            metric_name=data['metric_name'],
            operator=data.get('operator', '>'),
            threshold=float(data['threshold']),
            severity=data.get('severity', 'warning'),
            message=data['message'],
        )
        return JsonResponse({'success': True, 'id': rule.id})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def get_alert_rules(request):
    """获取告警规则"""
    rules = AlertRule.objects.filter(enabled=True)
    data = [{
        'id': r.id,
        'name': r.name,
        'metric_name': r.metric_name,
        'operator': r.operator,
        'threshold': r.threshold,
        'severity': r.severity,
        'message': r.message,
    } for r in rules]
    return JsonResponse({'rules': data})

def alert_rules(request):
    return render(request, 'monitor/alert_rules.html')

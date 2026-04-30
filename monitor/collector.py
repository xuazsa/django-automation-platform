import os
import sys
import django

sys.path.append('/home/wp/notebooks/python_projects/mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from monitor.models import Metric
import psutil
from datetime import datetime

def collect_metrics():
    """采集系统指标并保存到数据库"""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    Metric.objects.create(
        name='cpu',
        metric_type='cpu',
        value=cpu_percent,
        unit='%',
        recorded_at=datetime.now()
    )
    
    # 内存
    mem = psutil.virtual_memory()
    Metric.objects.create(
        name='memory',
        metric_type='memory',
        value=mem.percent,
        unit='%',
        recorded_at=datetime.now()
    )
    
    # 磁盘
    disk = psutil.disk_usage('/')
    Metric.objects.create(
        name='disk',
        metric_type='disk',
        value=disk.percent,
        unit='%',
        recorded_at=datetime.now()
    )
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 采集完成: CPU={cpu_percent}%, 内存={mem.percent}%, 磁盘={disk.percent}%")

if __name__ == '__main__':
    collect_metrics()

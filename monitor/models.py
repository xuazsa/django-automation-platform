from django.db import models
from django.utils import timezone

class Metric(models.Model):
    """监控指标"""
    METRIC_TYPES = [
        ('cpu', 'CPU使用率'),
        ('memory', '内存使用率'),
        ('disk', '磁盘使用率'),
        ('network', '网络流量'),
        ('service', '服务状态'),
    ]
    name = models.CharField('指标名称', max_length=100)
    metric_type = models.CharField('指标类型', max_length=20, choices=METRIC_TYPES)
    value = models.FloatField('指标值')
    unit = models.CharField('单位', max_length=20, blank=True)
    tags = models.JSONField('标签', blank=True, default=dict)
    recorded_at = models.DateTimeField('记录时间', default=timezone.now)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.value}{self.unit} @ {self.recorded_at}"

    class Meta:
        verbose_name = '监控指标'
        verbose_name_plural = '监控指标'
        ordering = ['-recorded_at']

class AlertRule(models.Model):
    """告警规则"""
    SEVERITY_CHOICES = [
        ('info', '信息'),
        ('warning', '警告'),
        ('critical', '严重'),
    ]
    name = models.CharField('规则名称', max_length=100)
    metric_name = models.CharField('指标名称', max_length=100)
    operator = models.CharField('操作符', max_length=10, default='>')
    threshold = models.FloatField('阈值')
    severity = models.CharField('严重级别', max_length=20, choices=SEVERITY_CHOICES, default='warning')
    message = models.CharField('告警消息', max_length=500)
    enabled = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '告警规则'
        verbose_name_plural = '告警规则'

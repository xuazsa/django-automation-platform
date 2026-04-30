from django.db import models
from django.utils import timezone

class Switch(models.Model):
    VENDOR_CHOICES = [
        ('cisco', 'Cisco'),
        ('huawei', 'Huawei'),
        ('h3c', 'H3C'),
        ('ruijie', 'Ruijie'),
        ('other', '其他'),
    ]
    STATUS_CHOICES = [
        ('active', '在线'),
        ('offline', '离线'),
        ('maintenance', '维护中'),
    ]

    name = models.CharField('设备名称', max_length=100, unique=True)
    ip_address = models.GenericIPAddressField('管理IP', unique=True)
    vendor = models.CharField('厂商', max_length=20, choices=VENDOR_CHOICES)
    model = models.CharField('型号', max_length=50, blank=True)
    serial = models.CharField('序列号', max_length=50, blank=True)
    username = models.CharField('SSH用户名', max_length=50)
    password = models.CharField('SSH密码', max_length=100)
    enable_password = models.CharField('Enable密码', max_length=100, blank=True)

    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='offline')
    last_seen = models.DateTimeField('最后在线时间', blank=True, null=True)
    cpu_usage = models.FloatField('CPU使用率', blank=True, null=True)
    memory_usage = models.FloatField('内存使用率', blank=True, null=True)
    temperature = models.FloatField('温度(℃)', blank=True, null=True)

    location = models.CharField('物理位置', max_length=200, blank=True)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('添加时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    class Meta:
        verbose_name = '网络交换机'
        verbose_name_plural = '网络交换机'

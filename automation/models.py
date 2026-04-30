from django.db import models

class Task(models.Model):
    TASK_TYPES = [
        ('shell', 'Shell 命令'),
        ('python', 'Python 脚本'),
    ]
    STATUS_CHOICES = [
        ('active', '启用'),
        ('inactive', '禁用'),
    ]
    name = models.CharField('任务名称', max_length=100)
    task_type = models.CharField('任务类型', max_length=20, choices=TASK_TYPES)
    command = models.TextField('执行的命令/脚本')
    cron_expr = models.CharField('Cron 表达式', max_length=100, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    last_run = models.DateTimeField('最后执行时间', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

class TaskLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField('开始时间', auto_now_add=True)
    end_time = models.DateTimeField('结束时间', blank=True, null=True)
    status = models.CharField('状态', max_length=20, default='running')
    output = models.TextField('输出内容', blank=True)
    error = models.TextField('错误信息', blank=True)

    def __str__(self):
        return f"{self.task.name} - {self.start_time}"

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
    name = models.CharField('设备名称', max_length=100)
    ip_address = models.GenericIPAddressField('管理IP', unique=True)
    vendor = models.CharField('厂商', max_length=20, choices=VENDOR_CHOICES)
    username = models.CharField('SSH用户名', max_length=50, blank=True)
    password = models.CharField('SSH密码', max_length=100, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='offline')
    location = models.CharField('位置', max_length=200, blank=True)
    created_at = models.DateTimeField('添加时间', auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

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
    name = models.CharField('设备名称', max_length=100)
    ip_address = models.GenericIPAddressField('管理IP', unique=True)
    vendor = models.CharField('厂商', max_length=20, choices=VENDOR_CHOICES)
    username = models.CharField('SSH用户名', max_length=50, blank=True)
    password = models.CharField('SSH密码', max_length=100, blank=True)
    enable_password = models.CharField('Enable密码', max_length=100, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='offline')
    last_seen = models.DateTimeField('最后在线时间', blank=True, null=True)
    location = models.CharField('位置', max_length=200, blank=True)
    created_at = models.DateTimeField('添加时间', auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

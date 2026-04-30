from rest_framework import serializers
from .models import Switch, SwitchPort, SwitchCommandLog

class SwitchSerializer(serializers.ModelSerializer):
    """交换机序列化器"""
    class Meta:
        model = Switch
        fields = [
            'id', 'name', 'ip_address', 'vendor', 'model', 
            'status', 'last_seen', 'cpu_usage', 'memory_usage',
            'location', 'description', 'created_at'
        ]

class SwitchPortSerializer(serializers.ModelSerializer):
    """端口序列化器"""
    switch_name = serializers.CharField(source='switch.name', read_only=True)
    
    class Meta:
        model = SwitchPort
        fields = [
            'id', 'switch', 'switch_name', 'port_name', 
            'description', 'vlan', 'status', 'speed'
        ]

class CommandLogSerializer(serializers.ModelSerializer):
    """命令日志序列化器"""
    switch_name = serializers.CharField(source='switch.name', read_only=True)
    
    class Meta:
        model = SwitchCommandLog
        fields = [
            'id', 'switch', 'switch_name', 'command', 
            'executor', 'status', 'duration', 'executed_at'
        ]

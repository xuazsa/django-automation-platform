from rest_framework import serializers
from .models import Switch, SwitchPort, SwitchCommandLog

class SwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switch
        fields = ['id', 'name', 'ip_address', 'vendor', 'status', 'last_seen', 'cpu_usage', 'memory_usage', 'location']

class SwitchPortSerializer(serializers.ModelSerializer):
    switch_name = serializers.CharField(source='switch.name', read_only=True)
    class Meta:
        model = SwitchPort
        fields = ['id', 'switch', 'switch_name', 'port_name', 'vlan', 'status']

class CommandLogSerializer(serializers.ModelSerializer):
    switch_name = serializers.CharField(source='switch.name', read_only=True)
    class Meta:
        model = SwitchCommandLog
        fields = ['id', 'switch', 'switch_name', 'command', 'executor', 'status', 'executed_at']

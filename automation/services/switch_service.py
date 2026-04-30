from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime

class SwitchService:
    VENDOR_MAP = {
        'cisco': 'cisco_ios',
        'huawei': 'huawei',
        'h3c': 'hp_comware',
    }

    @classmethod
    def get_connection_params(cls, switch):
        device_type = cls.VENDOR_MAP.get(switch.vendor, 'cisco_ios')
        params = {
            'device_type': device_type,
            'host': switch.ip_address,
            'username': switch.username,
            'password': switch.password,
            'port': 22,
            'timeout': 30,
        }
        if switch.enable_password:
            params['secret'] = switch.enable_password
        return params

    @classmethod
    def execute_command(cls, switch, command, executor=''):
        try:
            params = cls.get_connection_params(switch)
            with ConnectHandler(**params) as conn:
                if switch.enable_password:
                    conn.enable()
                output = conn.send_command(command)
            switch.last_seen = datetime.now()
            switch.save()
            return True, output
        except NetmikoTimeoutException:
            return False, "连接超时"
        except NetmikoAuthenticationException:
            return False, "认证失败"
        except Exception as e:
            return False, str(e)

    @classmethod
    def backup_config(cls, switch):
        success, output = cls.execute_command(switch, 'show running-config')
        if success:
            return True, "备份成功"
        return False, output

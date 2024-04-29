# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
import re
from netmiko.cisco.cisco_ios import CiscoIosSSH

class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()
        
    def send_command(self, command, *args, **kwargs):
        command_output = super().send_command(command, *args, **kwargs)
        self._check_error_in_command(command, command_output)            
        return command_output
        
    def _check_error_in_command(self, command, command_output):
        if "%" in command_output:
            error = re.search(r'% (?P<error>.+)', command_output)
            raise ErrorInCommand(f'При выполнении команды "{command}" на устройстве {self.host} возникла ошибка "{error.group("error")}"')
            
    def send_config_set(self, config_commands, *args, **kwargs):
        if type(config_commands) == str:
            config_commands = [config_commands]
        command_output = ""
        for command in config_commands:
            command_output += super().send_config_set(command, *args, **kwargs)
            print(command_output)
            self._check_error_in_command(command, command_output)            
        return command_output
        
        
class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """
    pass
        

if __name__ == '__main__':
    device_params = {
        "device_type": "cisco_ios",
        "ip": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
        }
    r1 = MyNetmiko(**device_params)
    #print(r1.send_config_set('logging 0255.255.1'))
    print(r1.send_config_set('lo'))
    #print(r1.send_config_set('a'))

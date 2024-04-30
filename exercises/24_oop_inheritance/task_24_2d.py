# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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
            
    def send_config_set(self, config_commands, ignore_errors=True):
        if ignore_errors:
            command_output = super().send_config_set(config_commands)
        else:
            if type(config_commands) == str:
                config_commands = [config_commands]
            command_output = ""
            self.config_mode()
            for command in config_commands:
                command_output += super().send_config_set(command, exit_config_mode=False)
                self._check_error_in_command(command, command_output)
            self.exit_config_mode()
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
    print(r1.send_config_set('lo'))
    print(r1.send_config_set('lo', ignore_errors=True))
    print(r1.send_config_set('lo', ignore_errors=False))

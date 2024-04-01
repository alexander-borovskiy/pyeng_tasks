# -*- coding: utf-8 -*-
"""
Задание 19.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config
на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* filename - имя файла, в который будут записаны выводы всех команд
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию None)
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Аргументы show, config и limit должны передаваться только как ключевые. При передачи
этих аргументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands_to_devices(devices, 'result.txt', 'sh clock')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands_to_devices(devices, 'result.txt', 'sh clock')

TypeError: send_commands_to_devices() takes 2 positional argument but 3 were given


При вызове функции send_commands_to_devices, всегда должен передаваться
только один из аргументов show, config. Если передаются оба аргумента, должно
генерироваться исключение ValueError.


Вывод команд должен быть записан в файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, 'result.txt', show='sh clock')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

In [13]: send_commands_to_devices(devices, 'result.txt', config=commands)

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
"""
import logging
import netmiko
import time
import yaml

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_commands(device, *, show=None, config=None):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received: {}'
    ip = device['host']
    logging.info(start_msg.format(datetime.now().time(), ip))
    with netmiko.Netmiko(**device) as ssh:
        ssh.enable()
        prompt = ssh.find_prompt()
        if show:
            result = ssh.send_command(show)
            command = show
            return_result = f"{prompt}{command}\n{result}\n"
        else:
            result = ssh.send_config_set(config)
            return_result = f"{result}\n"
        logging.info(received_msg.format(datetime.now().time(), ip))
    return return_result


def send_commands_to_devices(devices, filename, *, show=None, config=None, limit=3):
    if show and config:
        raise ValueError("Передайте либо одну команду show, либо набор конфигурационных команд.")
    elif not show and not config:
        raise ValueError("Не передано ни одной команды.")
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        if show:
            for device in devices:
                future = executor.submit(send_commands, device, show=show)
                future_list.append(future)
        else:
            for device in devices:
                future = executor.submit(send_commands, device, config=config)
                future_list.append(future)
    with open(filename, "w") as file_to_save:
        for f in future_list:
            file_to_save.write(f.result())


if __name__ == "__main__":
    show_command ='sh clock'
    config_command = 'logging 10.5.5.5'
    config_commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_commands_to_devices(devices, "send_commands_to_devices_19_4.txt", show=show_command, limit=2)
    #send_commands_to_devices(devices, "send_commands_to_devices_19_4.txt", limit=2)
    #send_commands_to_devices(devices, "send_commands_to_devices_19_4.txt", 'sh clock',  limit=2)
    #send_commands_to_devices(devices, "send_commands_to_devices_19_4.txt", show=show_command, config=config_command, limit=2)
    #send_commands_to_devices(devices, "send_commands_to_devices_19_4.txt", config=config_command, limit=2)
    #send_commands_to_devices(devices, "send_commands_to_devices_19_4.txt", config=config_commands, limit=2)

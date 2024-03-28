# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

import subprocess
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat


def ping_ip_address(ip_address):
    reply = subprocess.run(['ping', '-c', '3', '-n', ip_address],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf-8')
    if reply.returncode == 0:
        return True #, reply.stdout
    else:
        return False #, reply.stderr


def ping_ip_addresses(ip_list, limit=3):
    available_ip = []
    not_available_ip = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip_address, ip_list)
        for ip, output in zip(ip_list, result):
            if output:
                available_ip.append(ip)
            else:
                not_available_ip.append(ip)
    return available_ip, not_available_ip


if __name__ == "__main__":
    print(ping_ip_addresses(["192.168.100.1",
                             "192.168.100.2",
                             "192.168.100.3",
                             "192.168.200.1",
                             "8.8.8.8",
                             ],
                             limit=2))

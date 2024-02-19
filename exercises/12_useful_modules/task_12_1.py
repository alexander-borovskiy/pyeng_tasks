# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess


def ping_ip_addresses (ip_list):
    ok_list = []
    not_ok_list =[]
    for ip in ip_list:
        result = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            ok_list.append(ip)
        else:
            not_ok_list.append(ip)
    return ok_list, not_ok_list


if __name__ == "__main__":
    print(ping_ip_addresses(["8.8.8.8", "192.168.1.1", "10.0.0.1"]))

# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import netmiko
import yaml
from pprint import pprint
from textfsm import clitable


def send_and_parse_show_command(device_dict, command, templates_path, index_file="index"):
    cli_table = clitable.CliTable(index_file, templates_path)
    attributes = {
                  "Command": command,
                  "Vendor": device_dict["device_type"],
                  }
    with netmiko.Netmiko(**device_dict) as r1:
        r1.enable()
        output = r1.send_command(command)
    cli_table.ParseCmd(output, attributes)
    result = [dict(zip(cli_table.header, row)) for row in cli_table]
    return result


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    pprint(send_and_parse_show_command(devices[0], "sh ip int br", templates_path="templates"))

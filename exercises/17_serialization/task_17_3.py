# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re


def parse_sh_cdp_neighbors(sh_cdp):
    """
    Функция которая обрабатывает
    вывод команды show cdp neighbors.
    """
    description_dict = {}
    regex1 = re.compile(r'(?P<loc_dev>\S+)>')
    regex2 = re.compile(r'(?P<rem_dev>\S+) +(?P<loc_intf>\S+ \S+) +\w+ +. . . +\w+ +(?P<rem_intf>\S+ \S+)')
    m1 = regex1.search(sh_cdp)
    m2 = regex2.finditer(sh_cdp)
    if m1 and m2:
        description_dict[m1.group('loc_dev')] = {}
        for m in m2:
            description_dict[m1.group('loc_dev')][m.group('loc_intf')] = {m.group('rem_dev'):m.group('rem_intf')}
    return description_dict


if __name__ == '__main__':
    with open('sh_cdp_n_sw1.txt') as f:
        print(parse_sh_cdp_neighbors(f.read()))

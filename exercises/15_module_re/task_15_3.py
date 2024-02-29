# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""
import re


def convert_ios_nat_to_asa(filename_ios, filename_asa):
    """
    Функция конвертирует правила NAT из синтаксиса cisco IOS в cisco ASA.
    """
    rule_list = []
    regex = re.compile(r'ip nat inside source static tcp (\S+) (\d+) interface \S+ (\S+)')
    with open(filename_ios) as f:
        for line in f:
            m = regex.search(line)
            if m:
                rule_list.append(m.groups())
    with open(filename_asa, 'w') as f:
        for rule in rule_list:
            asa_rule = (
                        f'object network LOCAL_{rule[0]}\n'
                        f' host {rule[0]}\n'
                        f' nat (inside,outside) static interface service tcp {rule[1]} {rule[2]}\n'
                        )
            f.write(asa_rule)


if __name__ == '__main__':
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'cisco_nat_config_asa.txt')

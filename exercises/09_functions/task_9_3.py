# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
from pprint import pprint

def get_int_vlan_map(config_filename):
    """
    config_filename - имя конфигурационного файла.

    Возвращает кортеж из двух словарей:

    * словарь портов в режиме access, где ключи номера портов,
      а значения access VLAN (числа):
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/16': 17}

    * словарь портов в режиме trunk, где ключи номера портов,
      а значения список разрешенных VLAN (список чисел):
    {'FastEthernet0/1': [10, 20],
     'FastEthernet0/2': [11, 30],
    'FastEthernet0/4': [17]}
    """
    access_check = ["interface", "access"]
    trunk_check = ["interface", "trunk"]
    access_config_dict = {}
    trunk_config_dict = {}
    with open(config_filename, "r") as f:
        for section in f.read().split("!"):
            if section:
                words = section.split()
                words_access = set(words) & set(access_check)
                words_trunk = set(words) & set(trunk_check)
                if words_access == set(access_check):
                    access_config_dict[words[1]] = int(words[8])
                elif words_trunk == set(trunk_check):
                    vlan_list = words[10].split(",")
                    int_vlan_list = []
                    for vlan in vlan_list:
                        int_vlan_list.append(int(vlan))
                    trunk_config_dict[words[1]] = int_vlan_list
    return access_config_dict, trunk_config_dict


access_config, trunk_config = get_int_vlan_map("config_sw1.txt")
print(access_config)
print(trunk_config)

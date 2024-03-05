# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""

import re
import yaml


def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    """
    Функция обрабатывает вывод
    команды show cdp neighbor из нескольких файлов и записывает итоговую
    топологию в один словарь.
    """
    description_dict = {}
    regex1 = re.compile(r'(?P<loc_dev>\S+)>')
    regex2 = re.compile(r'(?P<rem_dev>\S+) +(?P<loc_intf>\S+ \S+) +\d+.+ (?P<rem_intf>\S+ \S+)')
    for file in list_of_files:
        with open(file) as f:
            file_cont = f.read()
            m1 = regex1.search(file_cont)
            m2 = regex2.finditer(file_cont)
            if m1 and m2:
                description_dict[m1.group('loc_dev')] = {}
                for m in m2:
                    description_dict[m1.group('loc_dev')][m.group('loc_intf')] = {m.group('rem_dev'):m.group('rem_intf')}
    if save_to_filename:
        with open(save_to_filename, 'w') as f:
            yaml.dump(description_dict, f)
    return description_dict


if __name__ == '__main__':
    sh_cdp_n_list = ['sh_cdp_n_sw1.txt', 'sh_cdp_n_r1.txt', 'sh_cdp_n_r2.txt', 'sh_cdp_n_r3.txt', 'sh_cdp_n_r4.txt', 'sh_cdp_n_r5.txt', 'sh_cdp_n_r6.txt']
    print(generate_topology_from_cdp(sh_cdp_n_list, 'topology.yaml'))

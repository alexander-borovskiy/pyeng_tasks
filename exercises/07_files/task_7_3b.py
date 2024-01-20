# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
template = """{0:<7}  {1:<18}  {2}"""
list_for_sort = []
vlan = input("Enter VLAN number: ")
with open("CAM_table.txt", "r") as f:
    for line in f:
        note = line.split()
        if note and note[0].isdigit() and note[0] == vlan:
            list_for_sort.append([int(note[0]), note[1], note[3]])
    sorted_list = sorted(list_for_sort)
    for i in sorted_list:
        print(template.format(i[0], i[1], i[2]))

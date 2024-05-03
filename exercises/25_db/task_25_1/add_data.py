# -*- coding: utf-8 -*-
"""
Задание 25.1
Необходимо создать скрипт add_data.py.
Скрипт add_data.py - с помощью этого скрипта, выполняется добавление данных в БД.
Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding
и информацию о коммутаторах

Соответственно, в файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно
   также заполнять. Имя коммутатора определяется по имени файла с данными

Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data.py
База данных не существует. Перед добавлением данных, ее надо создать

Пример выполнения скрипта первый раз, после создания базы данных:
$ python add_data.py
Добавляю данные в таблицу switches...
Добавляю данные в таблицу dhcp...

Пример выполнения скрипта, после того как данные были добавлены в таблицу
(порядок добавления данных может быть произвольным, но сообщения должны
выводиться аналогично выводу ниже):

$ python add_data.py
Добавляю данные в таблицу switches...
При добавлении данных: ('sw1', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw2', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw3', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
Добавляю данные в таблицу dhcp...
При добавлении данных: ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
"""
import re
import sqlite3
import yaml
from create_db import check_db_exists


def add_switches(switches, db_name):
    if not check_db_exists(db_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return
    print('Добавляю данные в таблицу switches...')
    conn = db_connect(db_name)
    with open(switches) as f:
        switches = yaml.safe_load(f)['switches']
    for switch in switches.items():
        try:
            with conn:
                query = '''insert into switches (hostname, location)
                       values (?, ?)'''
                conn.execute(query, switch)
        except sqlite3.IntegrityError as e:
            print(f'При добавлении данных: {switch} Возникла ошибка: {e}')
    #cursor = conn.cursor()
    #cursor.execute('select * from switches')
    #print(cursor.fetchall())
    db_close(conn)


def add_dhcp(dhcp_snooping_files, db_name):
    if not check_db_exists(db_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return
    print('Добавляю данные в таблицу dhcp...')
    conn = db_connect(db_name)
    regex = re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    for file in dhcp_snooping_files:
        result = []
        with open(file) as data:
            sw = re.search("([^/]+)_dhcp_snooping.txt", file).group(1)
            for line in data:
                match = regex.search(line)
                if match:
                    value = list(match.groups())
                    value.append(sw)
                    result.append(tuple(value))
        for row in result:
            try:
                with conn:
                    query = '''insert into dhcp (mac, ip, vlan, interface, switch)
                       values (?, ?, ?, ?, ?)'''
                    conn.execute(query, row)
            except sqlite3.IntegrityError as e:
                print(f'При добавлении данных: {row} Возникла ошибка: {e}')
    #cursor = conn.cursor()
    #cursor.execute('select * from dhcp')
    #print(cursor.fetchall())
    db_close(conn)


def db_connect(db_name):
    return sqlite3.connect(db_name)


def db_close(connect):
    connect.close()


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    switches = 'switches.yml'
    dhcp_snooping_files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
    add_switches(switches, db_name)
    add_dhcp(dhcp_snooping_files, db_name)

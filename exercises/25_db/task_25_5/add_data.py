# -*- coding: utf-8 -*-
"""
Задание 25.5

Для заданий 25 раздела нет тестов!

После выполнения заданий 25.1 - 25.5 в БД остается информация о неактивных записях.
И, если какой-то MAC-адрес не появлялся в новых записях, запись с ним,
может остаться в БД навсегда.

И, хотя это может быть полезно, чтобы посмотреть, где MAC-адрес находился
в последний раз, постоянно хранить эту информацию не очень полезно.

Например, если запись в БД уже больше месяца, то её можно удалить.

Для того, чтобы сделать такой критерий, нужно ввести новое поле,
в которое будет записываться последнее время добавления записи.

Новое поле называется last_active и в нем должна находиться строка,
в формате: YYYY-MM-DD HH:MM:SS.

В этом задании необходимо:
* изменить, соответственно, таблицу dhcp и добавить новое поле.
 * таблицу можно поменять из cli sqlite, но файл dhcp_snooping_schema.sql тоже необходимо изменить
* изменить скрипт add_data.py, чтобы он добавлял к каждой записи время

Получить строку со временем и датой, в указанном формате,
можно с помощью функции datetime в запросе SQL.
Синтаксис использования такой:
sqlite> insert into dhcp (mac, ip, vlan, interface, switch, active, last_active)
   ...> values ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1', '0', datetime('now'));

То есть вместо значения, которое записывается в базу данных,
надо указать datetime('now').

После этой команды в базе данных появится такая запись:
mac                ip               vlan  interface        switch  active  last_active
-----------------  ---------------  ----  ---------------  ------  ------  -------------------
00:09:BC:3F:A6:50  192.168.100.100  1     FastEthernet0/7  sw1     0       2019-03-08 11:26:56
"""
import re
import sqlite3
import yaml
from create_db import check_db_exists
from datetime import datetime
from tabulate import tabulate


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
            sw = re.search("(\w+)_dhcp_snooping.txt", file).group(1)
            set_active_in_dhcp(sw, conn)
            for line in data:
                match = regex.search(line)
                if match:
                    value = list(match.groups())
                    value.append(sw)
                    value.append(1)
                    value.append(datetime.now().replace(microsecond=0))
                    result.append(tuple(value))
        for row in result:
            #db_check_mac_in_dhcp(row)
            try:
                with conn:
                    query = '''replace into dhcp (mac, ip, vlan, interface, switch, active, last_active)
                       values (?, ?, ?, ?, ?, ?, ?)'''
                    conn.execute(query, row)
            except sqlite3.IntegrityError as e:
                print(f'При добавлении данных: {row} Возникла ошибка: {e}')
    cursor = conn.cursor()
    cursor.execute('select * from dhcp')
    print(tabulate(cursor.fetchall()))
    db_close(conn)


def db_connect(db_name):
    return sqlite3.connect(db_name)


def db_close(connect):
    connect.close()


def set_active_in_dhcp(sw, conn):
    query = f"update dhcp set active = 0 where switch = '{sw}';"
    conn.execute(query)


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    switches = 'switches.yml'
    dhcp_snooping_files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
    new_dhcp_snooping_files = ['new_data\sw1_dhcp_snooping.txt', 'new_data\sw2_dhcp_snooping.txt', 'new_data\sw3_dhcp_snooping.txt']
    add_switches(switches, db_name)
    #add_dhcp(dhcp_snooping_files, db_name)
    add_dhcp(new_dhcp_snooping_files, db_name)

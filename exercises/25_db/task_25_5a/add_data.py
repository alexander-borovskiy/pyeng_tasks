# -*- coding: utf-8 -*-
"""
Задание 25.5a

Для заданий 25 раздела нет тестов!

После выполнения задания 25.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data.py, таким образом, чтобы он удалял все записи,
которые были активными более 7 дней назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active
в некоторых записях и поставить время 7 или более дней.

В файле задания описан пример работы с объектами модуля datetime.
Показано как получить дату 7 дней назад.
С этой датой надо будет сравнивать время last_active.

Обратите внимание, что строки с датой, которые пишутся в БД, можно сравнивать
между собой.

"""
import re
import sqlite3
import yaml
from create_db import check_db_exists
from datetime import datetime, timedelta
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
    delete_old_data(conn)
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


def delete_old_data(conn):
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    query = f"delete from dhcp where last_active < '{week_ago}';"
    conn.execute(query)


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    switches = 'switches.yml'
    dhcp_snooping_files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
    new_dhcp_snooping_files = ['new_data\sw1_dhcp_snooping.txt', 'new_data\sw2_dhcp_snooping.txt', 'new_data\sw3_dhcp_snooping.txt']
    #add_switches(switches, db_name)
    #add_dhcp(dhcp_snooping_files, db_name)
    add_dhcp(new_dhcp_snooping_files, db_name)

# -*- coding: utf-8 -*-
"""
Задание 25.4

Для заданий 25 раздела нет тестов!

Скопировать файл get_data из задания 25.2.
Добавить в скрипт поддержку столбца active, который мы добавили в задании 25.3.

Теперь, при запросе информации, сначала должны отображаться активные записи,
а затем, неактивные. Если неактивных записей нет, не отображать
заголовок "Неактивные записи".

Примеры выполнения итогового скрипта
$ python get_data.py
В таблице dhcp такие записи:

Активные записи:

-----------------  ----------  --  ----------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1   sw1  1
00:04:A3:3E:5B:69  10.1.15.2   15  FastEthernet0/15  sw1  1
00:05:B3:7E:9B:60  10.1.5.4     5  FastEthernet0/9   sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5   sw1  1
00:E9:BC:3F:A6:50  100.1.1.6    3  FastEthernet0/20  sw3  1
00:E9:22:11:A6:50  100.1.1.7    3  FastEthernet0/21  sw3  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7   sw2  1
00:B4:A3:3E:5B:69  10.1.5.20    5  FastEthernet0/5   sw2  1
00:A9:BC:3F:A6:50  10.1.10.65  20  FastEthernet0/2   sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4   sw2  1
-----------------  ----------  --  ----------------  ---  -

Неактивные записи:

-----------------  ---------------  -  ---------------  ---  -
00:09:BC:3F:A6:50  192.168.100.100  1  FastEthernet0/7  sw1  0
00:C5:B3:7E:9B:60  10.1.5.40        5  FastEthernet0/9  sw2  0
-----------------  ---------------  -  ---------------  ---  -

$ python get_data.py vlan 5

Информация об устройствах с такими параметрами: vlan 5

Активные записи:

-----------------  ---------  -  ---------------  ---  -
00:05:B3:7E:9B:60  10.1.5.4   5  FastEthernet0/9  sw1  1
00:B4:A3:3E:5B:69  10.1.5.20  5  FastEthernet0/5  sw2  1
-----------------  ---------  -  ---------------  ---  -

Неактивные записи:

-----------------  ---------  -  ---------------  ---  -
00:C5:B3:7E:9B:60  10.1.5.40  5  FastEthernet0/9  sw2  0
-----------------  ---------  -  ---------------  ---  -


$ python get_data.py vlan 10

Информация об устройствах с такими параметрами: vlan 10

Активные записи:

-----------------  ----------  --  ---------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5  sw1  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4  sw2  1
-----------------  ----------  --  ---------------  ---  -
"""
import sqlite3
import sys
from tabulate import tabulate


def get_data(db_name):
    keys = "mac ip vlan interface switch active".split()
    if check_args():
        key, value = check_args()
    else:
        return
    if not key in keys:
        print('Данный параметр не поддерживается.\n'
        'Допустимые значения параметров: {}'.format(', '.join(keys)))
        return
    print('\nИнформация об устройствах с такими параметрами: ', key, value)
    query_act = "select * from dhcp where {} = ? and active = 1".format(key)
    query_not_act = "select * from dhcp where {} = ? and active = 0".format(key)
    conn = db_connect(db_name)
    cursor = conn.cursor()
    result_act = cursor.execute(query_act, (value, ))
    print('\nАктивные записи:\n')
    print(tabulate(result_act))
    result_not_act = cursor.execute(query_not_act, (value, ))
    items = result_not_act.fetchall()
    if items:
        print('\nНеактивные записи:\n')
        print(tabulate(items))
    db_close(conn)


def get_alldata():
    print("В таблице dhcp такие записи:")
    conn = db_connect(db_name)
    cursor = conn.cursor()
    result_act = cursor.execute('select * from dhcp where active = 1')
    print('\nАктивные записи:\n')
    print(tabulate(result_act))
    result_not_act = cursor.execute('select * from dhcp where active = 0')
    items = result_not_act.fetchall()
    if items:
        print('\nНеактивные записи:\n')
        print(tabulate(items))
    db_close(conn)


def check_args():
    args = sys.argv[1:]
    if len(args) > 2 or len(args) == 1:
        print('Пожалуйста, введите два или ноль аргументов')
        return False
    elif not args:
        get_alldata()
    else:
        return args


def db_connect(db_name):
    return sqlite3.connect(db_name)


def db_close(connect):
    connect.close()


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    get_data(db_name)

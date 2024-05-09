# -*- coding: utf-8 -*-
"""
Задание 25.6

Для заданий 25 раздела нет тестов!

В этом задании выложен файл parse_dhcp_snooping.py.
В файле parse_dhcp_snooping.py нельзя ничего менять.

В файле созданы несколько функций и описаны аргументы командной строки,
которые принимает файл.

Есть поддержка аргументов для выполнения всех действий, которые,
в предыдущих заданиях, выполнялись в файлах create_db.py, add_data.py и get_data.py.

В файле parse_dhcp_snooping.py есть такая строка:
import parse_dhcp_snooping_functions as pds

И задача этого задания в том, чтобы создать все необходимые функции, в файле
parse_dhcp_snooping_functions.py на основе информации в файле parse_dhcp_snooping.py.

Из файла parse_dhcp_snooping.py, необходимо определить:
* какие функции должны быть в файле parse_dhcp_snooping_functions.py
* какие параметры создать в этих функциях

Необходимо создать соответствующие функции и перенести в них функционал,
который описан в предыдущих заданиях.

Вся необходимая информация, присутствует в функциях create, add, get,
в файле parse_dhcp_snooping.py.

В принципе, для выполнения задания, не обязательно разбираться с модулем argparse, но,
можно почитать о нем в разделе
https://pyneng.readthedocs.io/ru/latest/book/12_useful_modules/argparse.html

Для того, чтобы было проще начать, попробуйте создать необходимые функции в файле
parse_dhcp_snooping_functions.py и просто выведите аргументы функций, используя print.

Потом, можно создать функции, которые запрашивают информацию из БД
(базу данных можно скопировать из предыдущих заданий).

Можно создавать любые вспомогательные функции в файле parse_dhcp_snooping_functions.py,
а не только те, которые вызываются из файла parse_dhcp_snooping.py.


Проверьте все операции:
* создание БД
* добавление информации о коммутаторах
* добавление информации на основании вывода sh ip dhcp snooping binding из файлов
* выборку информации из БД (по параметру и всю информацию)

Чтобы было проще понять, как будет выглядеть вызов скрипта,
ниже несколько примеров.
В примерах показывается вариант, когда в базе данных есть поля active и last_active,
но можно также использовать вариант без этих полей.

$ python parse_dhcp_snooping.py get -h
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]

optional arguments:
  -h, --help            show this help message and exit
  --db DB_FILE          имя БД
  -k {mac,ip,vlan,interface,switch}
                        параметр для поиска записей
  -v VALUE              значение параметра
  -a                    показать все содержимое БД


$ python parse_dhcp_snooping.py add -h
usage: parse_dhcp_snooping.py add [-h] [--db DB_FILE] [-s]
                                  filename [filename ...]

positional arguments:
  filename      файл(ы), которые надо добавить

optional arguments:
  -h, --help    show this help message and exit
  --db DB_FILE  имя БД
  -s            если флаг установлен, добавлять данные коммутаторов, иначе -
                DHCP записи


$ python parse_dhcp_snooping.py add -h
usage: parse_dhcp_snooping.py add [-h] [--db DB_FILE] [-s]
                                  filename [filename ...]

positional arguments:
  filename      файл(ы), которые надо добавить

optional arguments:
  -h, --help    show this help message and exit
  --db DB_FILE  имя БД
  -s            если флаг установлен, добавлять данные коммутаторов, иначе
                добавлять DHCP записи


$ python parse_dhcp_snooping.py get -h
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]

optional arguments:
  -h, --help            show this help message and exit
  --db DB_FILE          имя БД
  -k {mac,ip,vlan,interface,switch}
                        параметр для поиска записей
  -v VALUE              значение параметра
  -a                    показать все содержимое БД


$ python parse_dhcp_snooping.py create_db
Создаю БД dhcp_snooping.db со схемой dhcp_snooping_schema.sql
Создаю базу данных...


$ python parse_dhcp_snooping.py add sw[1-3]_dhcp_snooping.txt
Читаю информацию из файлов
sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt

Добавляю данные по DHCP записях в dhcp_snooping.db


$ python parse_dhcp_snooping.py add -s switches.yml
Добавляю данные о коммутаторах

$ python parse_dhcp_snooping.py get
В таблице dhcp такие записи:

Активные записи:

-----------------  ---------------  --  ----------------  ---  -  -------------------
00:09:BB:3D:D6:58  10.1.10.2        10  FastEthernet0/1   sw1  1  2019-03-08 16:47:52
00:04:A3:3E:5B:69  10.1.5.2          5  FastEthernet0/10  sw1  1  2019-03-08 16:47:52
00:05:B3:7E:9B:60  10.1.5.4          5  FastEthernet0/9   sw1  1  2019-03-08 16:47:52
00:07:BC:3F:A6:50  10.1.10.6        10  FastEthernet0/3   sw1  1  2019-03-08 16:47:52
00:09:BC:3F:A6:50  192.168.100.100   1  FastEthernet0/7   sw1  1  2019-03-08 16:47:52
00:A9:BB:3D:D6:58  10.1.10.20       10  FastEthernet0/7   sw2  1  2019-03-08 16:47:52
00:B4:A3:3E:5B:69  10.1.5.20         5  FastEthernet0/5   sw2  1  2019-03-08 16:47:52
00:C5:B3:7E:9B:60  10.1.5.40         5  FastEthernet0/9   sw2  1  2019-03-08 16:47:52
00:A9:BC:3F:A6:50  10.1.10.60       20  FastEthernet0/2   sw2  1  2019-03-08 16:47:52
00:E9:BC:3F:A6:50  100.1.1.6         3  FastEthernet0/20  sw3  1  2019-03-08 16:47:52
-----------------  ---------------  --  ----------------  ---  -  -------------------


$ python parse_dhcp_snooping.py get -k vlan -v 10
Данные из БД: dhcp_snooping.db
Информация об устройствах с такими параметрами: vlan 10

Активные записи:

-----------------  ----------  --  ---------------  ---  -  -------------------
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1  1  2019-03-08 16:47:52
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/3  sw1  1  2019-03-08 16:47:52
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2  1  2019-03-08 16:47:52
-----------------  ----------  --  ---------------  ---  -  -------------------


$ python parse_dhcp_snooping.py get -k vln -v 10
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]
parse_dhcp_snooping.py get: error: argument -k: invalid choice: 'vln' (choose from 'mac', 'ip', 'vlan', 'interface', 'switch')

"""
import os
import re
import sqlite3
import yaml
from datetime import datetime, timedelta
from tabulate import tabulate


def create_db(db_name, db_schema_name):
    if check_db_exists(db_name):
        print('БД существует.')
    else:
        print('Создаю БД...')
        conn = sqlite3.connect(db_name)
        with open(db_schema_name, 'r') as f:
            schema = f.read()
            conn.executescript(schema)
        #print("Сделано!")
        conn.close()


def check_db_exists(db_name):
    if os.path.exists(db_name):
        return True
    else:
        return False


def add_data_switches(db_name, switches):
    switches = switches[0]
    if not check_db_exists(db_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return
    #print('Добавляю данные в таблицу switches...')
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
    db_close(conn)


def add_data(db_name, dhcp_snooping_files):
    if not check_db_exists(db_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return
    #print('Добавляю данные в таблицу dhcp...')
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


def get_data(db_name, key, value):
    #keys = "mac ip vlan interface switch active".split()
    #if check_args():
    #    key, value = check_args()
    #else:
    #    return
    #if not key in keys:
    #    print('Данный параметр не поддерживается.\n'
    #    'Допустимые значения параметров: {}'.format(', '.join(keys)))
    #    return
    #print('\nИнформация об устройствах с такими параметрами: ', key, value)
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


def get_all_data(db_name):
    #print("В таблице dhcp такие записи:")
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

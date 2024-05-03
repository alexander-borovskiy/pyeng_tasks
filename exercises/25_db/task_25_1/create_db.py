# -*- coding: utf-8 -*-
"""
Задание 25.1
Необходимо создать скрипт create_db.py.
Скрипт create_db.py - в этот скрипт должна быть вынесена функциональность по созданию БД:
* должна выполняться проверка наличия файла БД
* если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
  должна быть создана БД
* имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Пример выполнения скрипта, когда файла dhcp_snooping.db нет:
$ python create_db.py
Создаю базу данных...

После создания файла:
$ python create_db.py
База данных существует
"""
import os
import sqlite3


def create_db(db_name, db_schema_name):
    if check_db_exists(db_name):
        print('БД существует.')
    else:
        print('Создаю БД...')
        conn = sqlite3.connect(db_name)
        with open(db_schema_name, 'r') as f:
            schema = f.read()
            conn.executescript(schema)
        print("Сделано!")
        conn.close()


def check_db_exists(db_name):
    if os.path.exists(db_name):
        return True
    else:
        return False


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    db_schema_name = 'dhcp_snooping_schema.sql'
    create_db(db_name, db_schema_name)


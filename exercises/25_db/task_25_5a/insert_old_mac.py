# -*- coding: utf-8 -*-
import sqlite3
from tabulate import tabulate


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    data = [('00:09:BC:3F:A6:51', '192.168.100.101', '2', 'FastEthernet0/24', 'sw1', 0, '2020-05-08 16:30:27'),
            ('00:09:BC:3F:A6:52', '192.168.100.102', '22', 'FastEthernet1/24', 'sw2', 0, '2021-05-08 16:30:27'),
            ('00:09:BC:3F:A6:53', '192.168.100.103', '23', 'FastEthernet2/24', 'sw3', 0, '2024-05-02 16:30:27'),
            ('00:09:BC:3F:A6:54', '192.168.100.104', '24', 'FastEthernet3/24', 'sw1', 0, '2024-05-01 16:30:27'),
            ('00:09:BC:3F:A6:55', '192.168.100.105', '25', 'FastEthernet4/24', 'sw2', 0, '2024-05-01 18:30:27'),
            ('00:09:BC:3F:A6:56', '192.168.100.106', '26', 'FastEthernet5/24', 'sw3', 0, '2024-05-08 16:30:27')]
    connect = sqlite3.connect(db_name)
    query = '''insert into dhcp (mac, ip, vlan, interface, switch, active, last_active)
                       values (?, ?, ?, ?, ?, ?, ?)'''
    for row in data:
        connect.execute(query, row)
    connect.commit()
    cursor = connect.cursor()
    cursor.execute('select * from dhcp')
    print(tabulate(cursor.fetchall()))
    connect.close()

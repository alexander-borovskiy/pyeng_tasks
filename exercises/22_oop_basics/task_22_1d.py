# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


"""
from pprint import pprint


class Topology:
    def __init__(self, topology_dict): 
        self.topology = self._normalize(topology_dict)
        
    def _normalize(self, topology_dict):
        unique_network_map_dict = {}
        for side_a, side_b in topology_dict.items():
            if not unique_network_map_dict.get(side_b) == side_a:
                unique_network_map_dict[side_a] = side_b
        return unique_network_map_dict
    
    def delete_link(self, link_start, link_end):
        if link_start in self.topology and link_end == self.topology[link_start]:
            del self.topology[link_start]
        elif link_end in self.topology and link_start == self.topology[link_end]:
            del self.topology[link_end]
        else:
            print("Такого соединения нет")
    
    def delete_node(self, node):
        change_flag = False
        for key, value in list(self.topology.items()):
            if node in key or node in value:
                del self.topology[key]
                change_flag = True
        if not change_flag:
            print("Такого устройства нет")
    
    def add_link(self, link_start, link_end):
        if ((link_start in self.topology and link_end == self.topology[link_start]) or 
            (link_end in self.topology and link_start == self.topology[link_end])):
            print("Такое соединение существует")
        elif ((link_start in self.topology and link_end != self.topology[link_start]) or 
              (link_end in self.topology and link_start != self.topology[link_end])):
            print("Соединение с одним из портов существует")
        else:
            self.topology[link_start] = link_end
        

if __name__ == '__main__':
    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
                        }
    top = Topology(topology_example)
    pprint(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    pprint(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    pprint(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
    pprint(top.topology)

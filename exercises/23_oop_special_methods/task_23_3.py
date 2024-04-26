# -*- coding: utf-8 -*-

"""
Задание 23.3

Скопировать и изменить класс Topology из задания 22.1x.

Добавить метод, который позволит выполнять сложение двух экземпляров класса Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
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
            
    def __add__(self, other):
        new_dict = self.topology.copy()
        new_dict.update(other.topology)
        return Topology(new_dict)
        

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
    topology_example2 = {
        ("R1", "Eth0/4"): ("R7", "Eth0/0"),
        ("R1", "Eth0/6"): ("R9", "Eth0/0"),
                        }
    t1 = Topology(topology_example)
    pprint(t1.topology)
    t2 = Topology(topology_example2)
    pprint(t2.topology)
    t3 = t1 + t2
    pprint(t3.topology)
    pprint(t1.topology)
    pprint(t2.topology)

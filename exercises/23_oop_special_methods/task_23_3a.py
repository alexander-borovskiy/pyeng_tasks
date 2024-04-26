# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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
        
    def __getitem__(self, index):
        topology_list = list(self.topology.items())
        return topology_list[index]
        

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
    for link in t1:
        pprint(link)

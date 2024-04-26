# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
class IPAddress:
    def __init__(self, net):
        self._check_net(net)
        ip, mask = net.split("/")
        self._check_mask(mask)
        self.mask = int(mask)
        self._check_ip(ip)
        self.ip = ip
        self.net = net
            
    def _check_net(self, net):
        if "/" not in net:
            raise ValueError("Incorrect IPv4 address - нет /")
        
    def _check_mask(self, mask):
        if not mask.isdigit() or not (8 <= int(mask) <= 32):
            raise ValueError("Incorrect mask")
        
    def _check_ip(self, ip):
        if "." not in ip or len(ip.split(".")) != 4:
            raise ValueError("Incorrect IPv4 address")
        else:
            for octet in ip.split("."):
                if not octet.isdigit() or not (0 <= int(octet) <= 255):
                    raise ValueError("Incorrect IPv4 address")
                    
    def __str__(self):
        return f"IP address {self.net}"
        
    def __repr__(self):
        return f"IPAddress('{self.net}')"

            
if __name__ == "__main__":
    ip1 = IPAddress('10.1.1.1/24')
    print(str(ip1))
    print(ip1)
    ip_list = []
    ip_list.append(ip1)
    print(ip_list)

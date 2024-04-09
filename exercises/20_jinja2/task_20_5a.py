# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import netmiko
import os
import re
import yaml
from jinja2 import Environment, FileSystemLoader
from pprint import pprint
from task_20_5 import create_vpn_config


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    src_tunnel_list = map(int, tunnel_interfaces(src_device_params))
    dst_tunnel_list = map(int, tunnel_interfaces(dst_device_params))
    vpn_data_dict["tun_num"] = set_new_tunnel(src_tunnel_list, dst_tunnel_list)
    config1, config2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
    with netmiko.Netmiko(**src_device_params) as ssh:
        ssh.enable()
        result1 = ssh.send_config_set(config1.split("\n"))
    with netmiko.Netmiko(**dst_device_params) as ssh:
        ssh.enable()
        result2 = ssh.send_config_set(config2.split("\n"))
    return result1, result2

    
def tunnel_interfaces(device):
    with netmiko.Netmiko(**device) as ssh:
        ssh.enable()
        result = ssh.send_command("sh ip int br")
    list_of_tunnel_interfaces = re.findall(r'Tunnel(?P<tun_num>\d+)', result)
    return list_of_tunnel_interfaces
    
    
def set_new_tunnel(src_tunnel_list, dst_tunnel_list):
    tun_set = set(src_tunnel_list) | set(dst_tunnel_list) #множество имеющихся на обоих устройствах туннельных интерфейсов
    tun_num = min(set(range(max(tun_set) + 2)) - tun_set) #   #max определяет макс № интерфейса.
                                                          #   +2 для того чтобы в выборке появился +1 интерфейс, если все заняты и ещё +1 для функции range.
                                                          #   Функция range генерит арифметическую прогрессию от 0 до максимального инт. +1
                                                          #   Делаем из этого множество.
                                                          #   И вычитаем из множества range имеющиеся интерфейсы. Получается множество номеров, которые можно задать
                                                          #   в качестве номера интерфейса с учётом максимального имеющегося +1.
                                                          #   Функцией min выбираем минимальное число.
    return tun_num
    

if __name__ == "__main__":
    data = {
            "tun_num": None,
            "wan_ip_1": "192.168.100.1",
            "wan_ip_2": "192.168.100.2",
            "tun_ip_1": "10.0.1.1 255.255.255.252",
            "tun_ip_2": "10.0.1.2 255.255.255.252",
            }
    template_file1 = "templates/gre_ipsec_vpn_1.txt"
    template_file2 = "templates/gre_ipsec_vpn_2.txt"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    pprint(configure_vpn(devices[0], devices[1], template_file1, template_file2, data))

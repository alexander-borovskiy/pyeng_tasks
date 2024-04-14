# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""
import textfsm
from pprint import pprint

def parse_output_to_dict(template, command_output):
    with open(template) as templ:
        fsm = textfsm.TextFSM(templ)
        result = fsm.ParseTextToDicts(command_output)
        #result.insert(0, fsm.header)
    return result


if __name__ == "__main__":
    with open("output/sh_ip_int_br.txt") as f:
        output = f.read()
        result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    pprint(result)

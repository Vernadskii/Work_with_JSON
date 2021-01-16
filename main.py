""" Идея решения: из каждого json файла на входе выбираем номер пользователя и открываем по нему результирующую
    директорию, находим в ней файл с таким же номером и перезаписываем с новыми данными"""

import json
import os
from datetime import datetime


def delete_previous(path):
    """ Функция удаления файлов в директории """
    file_list = [f for f in os.listdir(path)]
    for f in file_list:
        os.remove(os.path.join(path, f))


def change_res_file(input_json, res_json):
    """Функция, которая редактирует результирующий файл на основе входного
    input_json, res_json - объекты класса json. """
    actions_list_input = input_json["sessions"][0]['actions']   # Перешли в ветку 'actions'
    actions_list_res = res_json['actions']      # Перешли в ветку 'actions'
    for action_inp in actions_list_input:
        type = action_inp['type']
        time_inp = datetime.strptime(action_inp['created_at'][9:-2], '%Y-%m-%dT%H:%M:%S').isoformat() # Читаем и преобразуем время
        print(time_inp, ' ', type)
        for action_res in actions_list_res:
            if action_res['type'] == type:
                action_res['count'] += 1
                time_res = action_res['last']
                if time_res:    # Если в 'last' уже есть записи
                    time_res = datetime.strptime(action_res['last'][9:-2], '%Y-%m-%dT%H:%M:%S').isoformat()
                    if time_inp > time_res:
                        print(time_inp, ' > ', time_res)
                        action_res['last'] = "ISODate('" + time_inp + "')"
                else:   # Если "last": null
                    action_res['last'] = "ISODate('" + time_inp + "')"


def create_pattern_json(number):
    """Функция создания шаблона результирущего файла
        Параметр number - идентификационный номер пользователя"""
    return json.dumps({'number': number,
                                    'actions': [
                                        {'type': 'create',
                                          'last': None,
                                          'count': 0},
                                         {'type': 'read',
                                          'last': None,
                                          'count': 0},
                                        {'type': 'update',
                                          'last': None,
                                          'count': 0},
                                        {'type': 'delete',
                                          'last': None,
                                          'count': 0}
                                        ]
                                    }, indent=2)


if __name__ == '__main__':
    tree = os.walk('Account')
    delete_previous("Results-data")     # Удаляем предыдущие результаты, если они есть
    for i in tree:
        print(i)
        for file_name in i[2]:      # Для каждого файла в каталоге Account
            try:
                with open(i[0] + '/' + file_name, 'r', encoding='utf8') as input_file:  # Читаем входящий файл
                    input_json = json.loads(input_file.read())      # Преобразуем его в объект класса json
                    res_path = 'Results-data/' + str(input_json['number']) + '.json'    # Запоминаем путь до результирующего файла
                    if not os.path.isfile(res_path):    # Если рез. файла ещё нет, то создаём и заполняем его по шаблону
                        print(res_path, ' создали')
                        with open(res_path, 'w+', encoding='utf8') as res_file:
                            res_file.write(create_pattern_json(input_json['number']))
                    # Начинаем дополнять рез. файл новой информацией
                    with open(res_path, 'r+', encoding='utf8') as res_file:
                        res_json = json.loads(res_file.read())  # Преобразовываем в json объект
                        change_res_file(input_json, res_json)
                        res_file.seek(0)
                        res_file.write(json.dumps(res_json, indent=4))  # Перезаписываем
                        res_file.truncate()
                        res_file.seek(0)
            except IOError:
                print("An IOError has occurred!")
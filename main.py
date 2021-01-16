""" Идея 1: из каждого json файла на входе выбираем номер пользователя и открываем по нему результирующую директорию,
    находим в ней файл с таким же номером и перезаписываем с новыми данными"""

import json
import os


def create_pattern_json(number):
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
    for i in tree:
        for file_name in i[2]:      # Для каждого файла в каталоге Account
            try:
                with open(i[0] + '/' + file_name, 'r', encoding='utf8') as input_file:  # Читаем входящий файл
                    input_json = json.load(input_file)
                    res_path = 'Results-data/' + str(input_json['number']) + '.json'    # Путь то результирующего файла
                    with open(res_path, 'w+', encoding='utf8') as res_file:    # Редактируем результирующий файл
                        if os.path.getsize(res_path) == 0:
                            # Если рез. файл ещё пустой, то заполняем его по шаблону

                            res_file.write(create_pattern_json(input_json['number']))

            except IOError:
                print("An IOError has occurred!")
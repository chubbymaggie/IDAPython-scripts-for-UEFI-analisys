# -*- coding: cp866 -*-

import os
import subprocess



# Принимает на вход имя и путь к файлу с расширением '.i64', открывает его и
# запускает вспомогательный скрипт, который работает внутри IdaPro.
def _start_i64(_name_i64, _path_to_i64, _path_to_py):
    subprocess.call("idaq64 -S\"%s\creat_txt_from_title.py\" \"%s\\%s\"" % (_path_to_py, _path_to_i64, _name_i64), shell=True)



#
#    ОСНОВНАЯ ФУНКЦИЯ
#
# Отталкиваясь от указанной директории '_dst_dir', пробегает по всем вложенным папкам
# и, если находит файл с расширением '.i64', передает имя файла, путь к нему и путь
# к вспомогательному файлу '.py' в функцию '_run_i64()'.
def main():
    _src_dir = os.getcwd()
    _dst_dir = r'c:\Users\Kyurchenko\Downloads\\' 
    for _path, _dirictories, _files in os.walk(_dst_dir):
        for _name in _files:
            if _name[-4:]=='.i64':
                _start_i64(_name, _path, _src_dir)



# Точка старта программы.
main()

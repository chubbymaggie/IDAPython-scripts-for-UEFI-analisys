# -*- coding: cp866 -*-

import os
import subprocess



# 
def _create_i64(_name_bin, _path_to_bin, _path_to_py):
    subprocess.call("idaq64 -A -S\"%s\create_comm_and_i64.py\" \"%s\\%s\"" % (_path_to_py, _path_to_bin, _name_bin), shell=False)



#
def _check_guid_xref_file():
    _files = os.listdir(os.getcwd())
    if 'Guid.xref' not in _files:
         print 'Проблема именования GUID\'ов: в текущей директории отсутсвует файл Guid.xref!'.decode('cp866')
         return 0


#
#    ОСНОВНАЯ ФУНКЦИЯ
#
# 
def main(): 
    if _check_guid_xref_file() != 0:
        _src_dir = os.getcwd()
        _dst_dir = r'\\lesheek\ResearchLab$\Universal\KOSTYAN_TEST\BIOS\\' 
        for _path, _dirictories, _files in os.walk(_dst_dir):
            for _name in _files:
                if _name[2:] in ('UI section.bin', 'DXE dependency section.bin', 'PEI dependency section.bin', 'Version section.bin', 'PEI apriory section.bin', 'DXE apriory section.bin'):
                    print '%s\%s' % (_path, _name)
                    _create_i64(_name, _path, _src_dir)
    os.system('pause')

# Точка старта программы.
main()

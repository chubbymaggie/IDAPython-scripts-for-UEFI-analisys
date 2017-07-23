# -*- coding: cp866 -*-

import os
import subprocess



#
def _create_txt(_name_i64, _path_to_i64, _path_to_py):
    subprocess.call("idaq64 -A -S\"%s\creat_txt_from_title.py\" \"%s\\%s\"" % (_path_to_py, _path_to_i64, _name_i64), shell=True)



# 
def _create_i64(_name_bin, _path_to_bin, _path_to_py):
    subprocess.call("idaq64 -A -S\"%s\create_comm_and_i64.py\" \"%s\\%s\"" % (_path_to_py, _path_to_bin, _name_bin), shell=False)



#
#    ОСНОВНАЯ ФУНКЦИЯ
#
# 
def main(): 
    _dst_dir = r'\\lesheek\ResearchLab$\Universal\KOSTYAN_TEST\BIOS\\'
    _src_dir = os.getcwd() 

    _bin_list = ('UI section.bin', 
                 'DXE dependency section.bin', 
                 'SMM dependency section.bin',
                 'PEI dependency section.bin', 
                 'Version section.bin', 
                 'PEI apriory section.bin', 
                 'DXE apriory section.bin')

    _i64_list = ('Raw section.i64', 
                 'PE32 image section.i64', 
                 'TE image section.i64')

    for _path, _dirictories, _files in os.walk(_dst_dir):
        for _name in _files:
            if _name[2:] in _bin_list:
                print 'create .i64'
                _create_i64(_name, _path, _src_dir)

            if _name[2:] in _i64_list:
                print 'create .txt'
                _create_txt(_name, _path, _src_dir)


    os.system('pause')


# Точка старта программы.
main()

# -*- coding: cp866 -*-

from idaapi import *
import os



# Закрывает файл с расширением '.i64', сохранив базу данных.
# создает '.i64' из '.bin'
def _close_programm():
    qexit(0)



#
def _make_guid_struct():
    add_struc(-1,"GUID",0)
    id = get_struc_id("GUID")
    AddStrucMember(id, "Data1",	0,	0x20000400,	-1,	4)
    AddStrucMember(id, "Data2",	0X4,	0x10000400,	-1,	2)
    AddStrucMember(id, "Data3",	0X6,	0x10000400,	-1,	2)
    AddStrucMember(id, "Data4",	0X8,	0x000400,	-1,	8)
    return id



#
def _num_dependency_guid(_start, _end, _size):
    _num_dependency_guid = (_end - _start - 1)//(1 + _size)
    return _num_dependency_guid


#
def _num_apriori_guid(_start, _end, _size):
    _num_aprior_guid = (_end - _start)//(_size)
    return _num_aprior_guid


#
def _make_dependency():
    _start_addr = cvar.inf.minEA
    _end_addr = cvar.inf.maxEA
    _size_guid = 0x10
    _guid_id = _make_guid_struct()
    _guid_num = _num_dependency_guid(_start_addr, _end_addr, _size_guid)
    _curr_addr = _start_addr
    for i in range(0, _guid_num):
        _curr_addr += 1
        doStruct(_curr_addr, get_struc_size(_guid_id), _guid_id)
        _curr_addr += _size_guid


#
def _make_apriory():
    start_addr = cvar.inf.minEA
    end_addr = cvar.inf.maxEA
    size_guid = 0x10
    _guid_id = _make_guid_struct()
    _guid_num = _num_apriori_guid(start_addr, end_addr, size_guid)
    _curr_addr = start_addr
    for i in range(0, _guid_num):
        doStruct(_curr_addr, get_struc_size(_guid_id), _guid_id)
        _curr_addr += size_guid    


#
def _make_cmt(_file_name):
    _content = open('%s' % _file_name,'r').read()
    if _content != None:
        ExtLinA(0,0,'%s' % _content.decode('cp1251').encode('cp866'))



#
def _sel_type_of_section(_name):
    if _name[2:] == r'DXE dependency section.bin':
        _make_dependency()
        _make_cmt('%s.txt' % _name[:-4])

    if _name[2:] == r'DXE apriory section.bin':
        _make_apriory()
        _make_cmt('%s.txt' % _name[:-4])
   
    if _name[2:] == r'PEI dependency section.bin':
        _make_dependency()
        _make_cmt('%s.txt' % _name[:-4])

    if _name[2:] == r'PEI apriory section.bin':
        _make_apriory()
        _make_cmt('%s.txt' % _name[:-4])
        
    if _name[2:] == r'UI section.bin':
        make_ascii_string(0,0,ASCSTR_UNICODE)
        _make_cmt('%s.txt' % _name[:-4])
        
    if _name[2:] == r'Version section.bin':
        make_ascii_string(0,0,ASCSTR_UNICODE)
        _make_cmt('%s.txt' % _name[:-4])
        


            
#
def _clear_all():
    do_unknown_range(cvar.inf.minEA, cvar.inf.maxEA - cvar.inf.minEA, DOUNK_EXPAND)    
    for i in range(0, 10):
        del_extra_cmt(cvar.inf.minEA, E_PREV + i)




#
#    ОСНОВНАЯ ФУНКЦИЯ
#
#
def main():
    _clear_all()
    _file_name = get_root_filename()
    _sel_type_of_section(_file_name)
    #_close_programm()



# Точка старта программы.    
main()

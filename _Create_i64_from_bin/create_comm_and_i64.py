# -*- coding: cp866 -*-

from idaapi import *
import os



# Закрывает файл с расширением '.i64', сохранив базу данных.
# создает '.i64' из '.bin'
def _close_programm():
    qexit(0)



#
def _add_apriory_guid_to_head(guid, guid_addr, _num_comm_line):
    file = open('C:\Work\Programs\IDAPython-scripts-for-UEFI-analisys\Create_i64_from_bin\Guid.xref', 'r')
    for line in file:
        if line[0:8] == guid[2:-1].upper():
            ExtLinA(0, _num_comm_line, ' - файл %s' % line[37:])
            set_name(guid_addr, line[37:], SN_NOWARN)



#
def _add_guid_to_head(guid, _num_comm_line):
    file = open('c:\Work\Programs\IDAPython-scripts-for-UEFI-analisys\Create_i64_from_bin\Guid.xref', 'r')
    for line in file:
        if guid[2:-1].upper() in line:
            ExtLinA(0, _num_comm_line, line)



#
def _calc_num_apriori_guid(_start, _end, _size):
    _num_aprior_guid = (_end - _start)//(_size)
    return _num_aprior_guid



#
def _calc_num_guid(_start, _end, _size):
    _num_guid = (_end - _start)//(1 + _size)
    return _num_guid


 
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
def _find_apriori_guides():
    start_addr = cvar.inf.minEA
    end_addr = cvar.inf.maxEA
    size_guid = 0x10
    _guid_id = _make_guid_struct()
    _guid_num = _calc_num_apriori_guid(start_addr, end_addr, size_guid)
    _curr_addr = start_addr
    for i in range(0, _guid_num):
        _guid = hex(Dword(_curr_addr))
        _add_apriory_guid_to_head(_guid, _curr_addr, i + 2)
        doStruct(_curr_addr, get_struc_size(_guid_id), _guid_id)
        _curr_addr += size_guid


        
#
def _find_guides():
    start_addr = cvar.inf.minEA
    end_addr = cvar.inf.maxEA
    size_guid = 0x10
    _guid_id = _make_guid_struct()
    _guid_num = _calc_num_guid(start_addr, end_addr, size_guid)
    curr_addr = start_addr
    for i in range(0, _guid_num):
        curr_addr += 1
        _guid = hex(Dword(curr_addr))
        _add_guid_to_head(_guid, i + 2)
        doStruct(curr_addr, get_struc_size(_guid_id), _guid_id)
        curr_addr += size_guid



#
def _select_type_section(_name):
    if _name[2:] == r'DXE dependency section.bin':
        ExtLinA(0,0,'Содержит зависимости запуска на исполнение модулей диспетчером DXE. ')
        ExtLinA(0,1,'Условием запуска является загрузка следующих протоколов:')
        _find_guides()

    if _name[2:] == r'DXE apriory section.bin':
        ExtLinA(0,0,'Содержит GUID\'ы файлов, которые диспетчер DXE запускает  ')
        ExtLinA(0,1,'в первую очередь, а именно: ')
        _find_apriori_guides()
    
    if _name[2:] == r'PEI dependency section.bin':
        ExtLinA(0,0,'Содержит зависимости запуска на исполнение модулей диспетчером PEI. ')
        ExtLinA(0,1,'Условием запуска является загрузка следующих протоколов:')
        _find_guides()

    if _name[2:] == r'PEI apriory section.bin':
        ExtLinA(0,0,'Содержит GUID\'ы файлов, которые диспетчер PEI запускает  ')
        ExtLinA(0,1,'в первую очередь, а именно: ')
        _find_apriori_guides()
        
    if _name[2:] == r'UI section.bin':
        make_ascii_string(0,0,ASCSTR_UNICODE)
        _content_str = GetString(0,-1,ASCSTR_UNICODE)
        ExtLinA(0,0,'Содержит строку интерфейса пользователя "%s" в формате unicode' % _content_str)
        
    if _name[2:] == r'Version section.bin':
        make_ascii_string(0,0,ASCSTR_UNICODE)
        _content_str = GetString(0,-1,ASCSTR_UNICODE)
        ExtLinA(0,0,'Секция содержит unicode-строку с версией файла. Имеет значение: %s' % _content_str)


            
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
    _select_type_section(_file_name)
    _close_programm()



# Точка старта программы.    
main()

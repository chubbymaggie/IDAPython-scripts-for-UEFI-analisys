#-*- coding: cp866 -*-

from idaapi import * 



# Закрывает файл с расширением '.i64', сохранив базу данных.
# создает '.i64' из '.bin'
def _close_programm():
    qexit(0)


      
# Ищет вутри открытого файла '.i64' точку входа (EntryPoint),
# если находит (это PE/TE) - копирует из нее комментарий, если
# не находит (это ROW) - копирует комментарий установленный
# на самый младший адрес файла. Перекодирует из cp866 в cp1251
# (cp866 не понятен операционной системе)
def _find_comment():
    _comm = ''
    if get_entry_qty() == 1:
        _comm = GetFunctionCmt(get_entry_ordinal(0), 1)
    else:
        _str = ''
        for i in range(0,100):
            if get_extra_cmt(0, idaapi.E_PREV + i) != None:
                _str += get_extra_cmt(0, idaapi.E_PREV + i)
                if _str[-1:] != ' ':
                    _str += ' '
    return _str.decode('cp866').encode('cp1251')


        
#
#    ОСНОВНАЯ ФУНКЦИЯ
#
#
# Запускается внутри открытого '.i64' файла. Получает имя файла,
# создает текстовый документ с таким же именем. Находит в '.i64'
# комментарий при помощи функции '_find_comment()', записывает
# найденный комментарий в текстовый файл. Закрывает '.i64'
def main():
    _file_name = get_root_filename()
    _file = open('%s.txt' % _file_name[:-4], 'w')
    _comment = _find_comment()
    _file.write('%s' % _comment)
    _close_programm()



# Точка старта программы.    
main()

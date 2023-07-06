import asyncio
import os
import shutil

from check_by_pyro import check_by_pyro
from lib_example import convert_tdata_to_tl_sess
from sqlite_work import sqlite_data_transfer


def main():

    # Конвертируем tdata в сессию telethon
    tl_usr_id = asyncio.run(convert_tdata_to_tl_sess())

    # Копируем шаблон файла сессии pyrogram для его наполнения
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tl_session_path = os.path.join(current_dir, 'convert_telethon.session')
    # source_file = os.path.join(current_dir, 'blank_pyro.session')
    destination_path = os.path.join(current_dir, 'new_pyro.session')
    shutil.copy(src=os.path.join(current_dir, 'blank_pyro.session'), dst=destination_path)

    # Трансфер SQL инфы файлов сессий между собой
    sqlite_data_transfer(tl_sess_path=tl_session_path, pyro_sess_path=destination_path, tl_usr_id=tl_usr_id)

    # Проверяем работу сессии pyrogram
    asyncio.run(check_by_pyro())

    # Перемещаем файлы сессии в отдельную папку
    shutil.move(src=destination_path, dst=os.path.join(current_dir, 'raw_converter', 'res_sessions'))
    shutil.move(src=tl_session_path, dst=os.path.join(current_dir, 'raw_converter', 'res_sessions'))


if __name__ == '__main__':
    main()


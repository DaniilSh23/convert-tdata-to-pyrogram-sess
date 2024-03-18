import asyncio
import os
from pathlib import Path
import shutil

from check_by_pyro import check_by_pyro
from chek_by_telethon import check_by_tl
from lib_example import convert_tdata_to_tl_sess
from session_converter import SessionConverter
from sqlite_work import sqlite_data_transfer


BASE_DIR = Path(__name__).resolve().parent


def tl_to_pyro_converter():
    """
    Функция для конвертации сессий telethon в сессиий pyrogram
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for tl_session_file in os.listdir(path=os.path.join(current_dir, 'raw_converter', 'tl_to_pyro')):
        if not tl_session_file.endswith(".session"):
            continue
        session_name, extension = os.path.splitext(tl_session_file)
        # Копируем шаблон файла сессии pyrogram для его наполнения
        tl_session_path = os.path.join(current_dir, 'raw_converter', 'tl_to_pyro', tl_session_file)
        destination_path = os.path.join(current_dir, f'pyro_{tl_session_file}')
        json_data_path = os.path.join(current_dir, 'raw_converter', 'tl_to_pyro', f'{session_name}.json')
        shutil.copy(src=os.path.join(current_dir, 'blank_pyro.session'), dst=destination_path)

        # Чекаем и берём ID из сессии телетон
        print(f'чекаем телетон {tl_session_path}')
        tl_usr_id = check_by_tl(
            tl_sess_path=tl_session_path,
            json_path=json_data_path,
            proxy_path='/home/da/PycharmProjects/convert_tdata_to_pyro_sess/proxy_list',
        )

        # Трансфер SQL инфы файлов сессий между собой
        sqlite_data_transfer(tl_sess_path=tl_session_path, pyro_sess_path=destination_path, tl_usr_id=tl_usr_id)

        # Проверяем работу сессии pyrogram
        asyncio.run(check_by_pyro(
            sess_name=f'pyro_{session_name}',
            json_path=json_data_path,
            proxy_path='/home/da/PycharmProjects/convert_tdata_to_pyro_sess/proxy_list',
        ))

        # Перемещаем файлы сессии в отдельную папку
        shutil.move(src=destination_path, dst=os.path.join(current_dir, 'raw_converter', 'res_sessions'))
        shutil.move(src=tl_session_path, dst=os.path.join(current_dir, 'raw_converter', 'res_sessions'))


def main():
    convert_mode = input('Введите 1 - конвертировать из telethon в сессию pyrogram. '
                         'Иначе из tdata в telethon и pyrogram\n>>> ')
    if convert_mode == '1':
        tl_to_pyro_converter()
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for tdata_dir in os.listdir(path=os.path.join(current_dir, 'raw_converter', 'tdata_to_sessions')):
            print(f'Конвертируем аккаунт: {tdata_dir!r}')
            # Конвертируем tdata в сессию telethon
            tl_usr_id = asyncio.run(convert_tdata_to_tl_sess(tdata_dir_name=tdata_dir))
            if not tl_usr_id:
                print(f'Пропускаем аккаунт: {tdata_dir!r}')
                continue

            # Копируем шаблон файла сессии pyrogram для его наполнения
            tl_session_path = os.path.join(current_dir, f'tl_{tdata_dir}.session')
            # source_file = os.path.join(current_dir, 'blank_pyro.session')
            destination_path = os.path.join(current_dir, f'pyro_{tdata_dir}.session')
            shutil.copy(src=os.path.join(current_dir, 'blank_pyro.session'), dst=destination_path)

            # Трансфер SQL инфы файлов сессий между собой
            sqlite_data_transfer(tl_sess_path=tl_session_path, pyro_sess_path=destination_path, tl_usr_id=tl_usr_id)

            # Проверяем работу сессии pyrogram
            asyncio.run(check_by_pyro(
                sess_name=f'pyro_{tdata_dir}',
                # json_path=,
                # proxy_path=,
            ))

            # Перемещаем файлы сессии в отдельную папку
            shutil.move(src=destination_path, dst=os.path.join(current_dir, 'raw_converter', 'res_sessions'))
            shutil.move(src=tl_session_path, dst=os.path.join(current_dir, 'raw_converter', 'res_sessions'))


def make_result_sessions_dirs(result_sessions_parent_dir):
    """
    Функция создания директорий для хранения файлов сессий, полученных в результате конвертации из TDATA
    """
    # Проверка и создание, при необходимости, директории для хранения файлов сессий pyrogram
    pyro_sessions_result_path = os.path.join(result_sessions_parent_dir, "pyrogram_sessions")
    if not os.path.exists(pyro_sessions_result_path):
        os.mkdir(pyro_sessions_result_path)

    # Проверка и создание, при необходимости, директории для хранения файлов сессий telethon
    telethon_sessions_result_path = os.path.join(result_sessions_parent_dir, "telethon_sessions")
    if not os.path.exists(telethon_sessions_result_path):
        os.mkdir(telethon_sessions_result_path)


if __name__ == '__main__':
    # TODO: Закоментил класс, который конвертит из тдата, ниже функция мэйн, в ней выбор из тдата в телетон и
    #  пайрограмм или из телетона в пайрограм, но лучше всё упаковать в класс

    source_dir = os.path.join(BASE_DIR, "raw_converter", "tdata_to_sessions")
    dest_dir = os.path.join(BASE_DIR, "raw_converter", "res_sessions")
    session_converter = SessionConverter(source_dir=source_dir, dest_dir=dest_dir)

    # Создаем папок для хранения результатов конвертации, если их еще нет
    make_result_sessions_dirs(result_sessions_parent_dir=dest_dir)

    session_converter.convert_tdata_to_pyro_and_tl()
    # main()


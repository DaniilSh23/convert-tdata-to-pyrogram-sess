import asyncio

from check_by_pyro import check_by_pyro
from raw_converter.lib_example import convert_tdata_to_tl_sess
from sqlite_work import sqlite_data_transfer


def main():
    # TODO: дописать перемещение файла сессии телетона в нужную папку, копирование шаблона файла сессии pyrogram
    #  также в нужную папку и передавать все эти пути в функцию трансфера sqlite
    asyncio.run(convert_tdata_to_tl_sess())
    sqlite_data_transfer()
    asyncio.run(check_by_pyro())


if __name__ == '__main__':
    main()


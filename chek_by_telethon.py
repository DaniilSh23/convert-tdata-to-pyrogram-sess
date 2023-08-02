import asyncio

from telethon import TelegramClient
from opentele.tl.telethon import TelegramClient


async def main(client):
    # Getting information about yourself
    me = await client.get_me()
    print(me.id)
    return me.id


def check_by_tl(tl_sess_path):
    """
    Функция, которая запускает клиент телетона, проверяет работу файла сессии и возвращает TLG ID
    :param tl_sess_path: str - путь к файлу сессии телетона
    :return: str - TLG ID
    """
    # client = TelegramClient(tl_sess_path, app_version='4.0.2 x64')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with TelegramClient(tl_sess_path, app_version='4.0.2 x64', loop=loop) as client:
        tlg_id = client.loop.run_until_complete(main(client))
    return tlg_id


# check_by_tl(tl_sess_path='/home/da/PycharmProjects/convert_tdata_to_pyro_sess/raw_converter/tl_to_pyro/18259394771.session')

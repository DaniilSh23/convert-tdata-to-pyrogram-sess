import asyncio
import json
import random

import socks
from telethon import TelegramClient
from opentele.tl.telethon import TelegramClient


async def main(client):
    # Getting information about yourself
    me = await client.get_me()
    print('Telethon session checked\n', me)
    return me.id


def check_by_tl(tl_sess_path, json_path, proxy_path):
    """
    Функция, которая запускает клиент телетона, проверяет работу файла сессии и возвращает TLG ID
    :param proxy_path: str - путь к файлу с проксями
    :param json_path: str - путь к файлу с json данными об аккаунте
    :param tl_sess_path: str - путь к файлу сессии телетона
    :return: str - TLG ID
    """
    # Открываем json с данными об аккаунте
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
    app_version = json_data.get("app_version")
    api_id = json_data.get("app_id")
    api_hash = json_data.get("app_hash")
    device_model = json_data.get("device")
    use_ipv6 = True     # TODO: захардкодил

    # Открываем файл с проксями
    with open(proxy_path, 'r') as proxy_file:
        proxy_lines = proxy_file.read().split('\n')
    proxy = random.choice(proxy_lines).strip().split(':')
    proxy_dct = dict(
        proxy_type=socks.SOCKS5,
        addr=proxy[0],
        port=proxy[1],
        username=proxy[2],
        password=proxy[3],
        # rdns=True,
    )

    # client = TelegramClient(tl_sess_path, app_version='4.0.2 x64')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with TelegramClient(
            tl_sess_path,
            app_version=app_version,
            api_id=api_id,
            api_hash=api_hash,
            device_model=device_model,
            # proxy=proxy_dct,
            # use_ipv6=use_ipv6,
            loop=loop,
            connection_retries=5,
    ) as client:
        tlg_id = client.loop.run_until_complete(main(client))
        print()
    return tlg_id

# check_by_tl(tl_sess_path='/home/da/PycharmProjects/convert_tdata_to_pyro_sess/raw_converter/tl_to_pyro/18259394771.session')

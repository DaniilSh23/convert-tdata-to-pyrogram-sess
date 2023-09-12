import asyncio
import json
import random


async def check_by_pyro(sess_name, json_path, proxy_path):
    """
    Фукнция для проверки работоспособности файла сессии pyrogram
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
    proxy = dict(
        scheme="socks5",
        hostname=proxy[0],
        port=proxy[1],
        username=proxy[2],
        password=proxy[3],
    )

    from pyrogram import Client
    async with Client(
            sess_name,
            api_id=api_id,
            api_hash=api_hash,
            app_version=app_version,
            device_model=device_model,
            ipv6=use_ipv6,
            proxy=proxy,
    ) as app:
        getme_rslt = await app.get_me()
        print(getme_rslt)

    # Принтуем в терминал сообщение об успехе
    green_txt_clr = '\033[92m'
    reset_txt_clr = '\033[0m'
    print(f"{green_txt_clr}Файл сессии Pyrogram проверен и успешно работает{reset_txt_clr}")


async def send_msg_to_me():
    from pyrogram import Client
    proxy = {
        'scheme': 'socks5',
        # 'scheme': 'http',
        'hostname': '45.145.57.234',
        'port': 11914,
        'username': '0ywKnr',
        'password': 'FQZMqo',
    }
    try:
        async with Client('pyro_18172145752_мой_штаты', proxy=proxy, ipv6=True) as app:
            send_rslt = await app.send_message(chat_id='CourseTrainBot', text='/start')
            print(send_rslt)
            return

            print(await app.get_me())
            return

            send_rslt = await app.send_message(chat_id='DanyaSevas', text='Hello World. Successful convert acc')
            print(send_rslt)
            rslt = await app.join_chat('@test_channel_for_my_bot32')
            print(rslt)
    except Exception as err:
        print(err)

# asyncio.run(send_msg_to_me())

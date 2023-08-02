import asyncio
import os


async def check_by_pyro(sess_name):
    """
    Фукнция для проверки работоспособности файла сессии pyrogram
    """
    from pyrogram import Client
    async with Client(sess_name) as app:
        getme_rslt = await app.get_me()
        print(getme_rslt)

    # Принтуем в терминал сообщение об успехе
    green_txt_clr = '\033[92m'
    reset_txt_clr = '\033[0m'
    print(f"{green_txt_clr}Файл сессии Pyrogram проверен и успешно работает{reset_txt_clr}")


async def send_msg_to_me():
    from pyrogram import Client
    async with Client('new_pyro') as app:
        send_rslt = await app.send_message(chat_id='DanyaSevas', text='Hello World. Successful convert acc')
        print(send_rslt)

# asyncio.run(send_msg_to_me())

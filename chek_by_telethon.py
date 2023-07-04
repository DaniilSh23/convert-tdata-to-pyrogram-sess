from telethon import TelegramClient
from opentele.tl.telethon import TelegramClient


async def main():
    # Getting information about yourself
    me = await client.get_me()
    print(me)


def check_by_tl():
    client = TelegramClient('telethon')
    with client:
        client.loop.run_until_complete(main())
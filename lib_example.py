import os.path

from opentele.td import TDesktop
from opentele.api import UseCurrentSession


async def convert_tdata_to_tl_sess():
    """
    Функция, которая конвертирует tdata в сесиию telethon
    """
    # Load TDesktop client from tdata folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tdata_folder = os.path.join(current_dir, 'raw_converter/tdata_to_sessions', 'tdata')
    tdesk = TDesktop(tdata_folder)

    # Check if we have loaded any accounts
    assert tdesk.isLoaded()

    # flag=UseCurrentSession
    #
    # Convert TDesktop to Telethon using the current session.
    client = await tdesk.ToTelethon(session="convert_telethon.session", flag=UseCurrentSession)

    await client.connect()
    await client.PrintSessions()
    tl_getme_rslt = await client.get_me()
    print(f'Результат конвертации в сессию telethon. Метод get_me: {tl_getme_rslt}')
    return tl_getme_rslt.id

# asyncio.run(convert_tdata_to_tl_sess())


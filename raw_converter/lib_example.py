from opentele.td import TDesktop
from opentele.api import UseCurrentSession


async def convert_tdata_to_tl_sess():
    # Load TDesktop client from tdata folder
    tdata_folder = r"/home/da/PycharmProjects/convert_tdata_to_pyro_sess/raw_converter/tdata_to_sessions/tdata"
    tdesk = TDesktop(tdata_folder)

    # Check if we have loaded any accounts
    assert tdesk.isLoaded()

    # flag=UseCurrentSession
    #
    # Convert TDesktop to Telethon using the current session.
    client = await tdesk.ToTelethon(session="telethon.session", flag=UseCurrentSession)

    await client.connect()
    await client.PrintSessions()


# asyncio.run(convert_tdata_to_tl_sess())


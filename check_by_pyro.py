# import asyncio


async def check_by_pyro():
    from pyrogram import Client
    async with Client("test_sess") as app:
        getme_rslt = await app.get_me()
        print(getme_rslt)


# asyncio.run(check_by_pyro())

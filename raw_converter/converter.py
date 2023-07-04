# -*- coding: utf-8 -*-
from telethon.sync import types
from telethon.tl import functions
from telethon.errors.rpcerrorlist import PhoneNumberBannedError, FloodWaitError, UserDeactivatedBanError, \
    PhoneCodeInvalidError, SessionPasswordNeededError
import os
import socket
from uuid import getnode as get_mac

import shutil
import asyncio
import datetime

import os
from faker import Faker
import json
import rich
from opentele.api import UseCurrentSession
from opentele.td import TDesktop as TD
from opentele.tl.configs import API
from opentele.tl import TelegramClient
from opentele.tl import TelegramClient as TC


#директории 
SESSIONS_DIR = "./res_sessions/"
TDATAS_DIR = "./res_tdatas/"
CONVERT_TDATA = "./tdata_to_sessions/"  # here load sessions to TDATA!! (folder/*/tdata) - where * name of session.
CONVERT_SESSION = "./sessions_to_tdata/"
#____________________________________#

#работа с рандомизацией
api = API.TelegramAndroid.Generate()
person = Faker()
first_name, last_name = person.name().split(" ")
username = "MaxConvert"
#____________________________________#


#Работа с json
date = str(datetime.date.today())
register_time = int(datetime.datetime.now().timestamp())
            
def get_json(session_phone: str):
    jsonic = {
                'session_file': session_phone,
                'phone': session_phone,
                'register_time': register_time,
                'app_id': api.api_id,
                'app_hash': api.api_hash,
                'sdk': api.system_version,
                'app_version': api.app_version,
                'device': api.device_model,
                'last_check_time': register_time,
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'sex': 0,
               'lang_pack': api.lang_code,
                'system_lang_pack': api.system_lang_code,
                'ipv6': False,
            }
            
    return json.dump(jsonic, open(SESSIONS_DIR + session_phone + ".json", "w+"))
#______________________________________#

#Очистка папок 
def clear():
    for dir in [TDATAS_DIR, SESSIONS_DIR, CONVERT_SESSION, CONVERT_TDATA]:
        try:
            shutil.rmtree(dir)
        except OSError:
            for file in os.listdir(dir):

                os.remove(file)

    for dir in [TDATAS_DIR, SESSIONS_DIR, CONVERT_SESSION, CONVERT_TDATA]:
        os.mkdir(dir)
#______________________________________#        

class TData:
    def __init__(self, path: str = "./sessions_to_tdata/") -> None:
        self.path = path

    async def session_to_tdata(self, session_path: str) -> None:
        await self._session_to_tdata(session_path)

    async def _session_to_tdata(self, session_path: str) -> None:
        client = TC(os.path.join(self.path, session_path))
        tdesk = await client.ToTDesktop(flag=UseCurrentSession)
        try:
            os.mkdir(os.path.join("tdata", session_path.split(".")[0]))
        except:
            pass

        try:
            tdesk.SaveTData(f"./res_tdatas/{session_path.split('.')[0]}/tdata")

        except TypeError:
            pass

        await client.disconnect()

    def pack_to_zip(self, tdata_path: str) -> None:
        shutil.make_archive(f"{tdata_path}", "zip", tdata_path)

# С сесии в тдату

async def SessionToTData():
    tdata = TData()

    for session in os.listdir(CONVERT_SESSION):

        if "." in session and session.split(".")[1] == "session":
            await tdata.session_to_tdata(session_path=session)

    tdata.pack_to_zip(tdata_path=TDATAS_DIR)
#____________________________________#

  # С тдаты в сессию
async def TDataToSession():
    
    tdataFolder = CONVERT_TDATA

    for session in os.listdir(tdataFolder):

        tdesk = TD(tdataFolder + session + "/tdata/")
        if tdesk.isLoaded():
            session = await tdesk.ToTelethon(
                session=f"./res_sessions/{session.strip('/')}.session",
                flag=UseCurrentSession,
            )

            await session.connect()
            data = await session.get_me()
            phone = data.phone

            print(phone)

            get_json(phone)

            await session.disconnect()
#____________________________________#

 # Меню       
async def main():
    rich.print(
        "[bold]Меню[/bold]\n\n"
        "[bright_cyan]| 1 |[/bright_cyan] [bright_red italic]C session в tdata [/bright_red italic]\n"
        "[bright_cyan]| 2 |[/bright_cyan] [bright_red italic]C tdata в session [/bright_red italic]\n"
        "[bright_cyan]| 3 |[/bright_cyan] [bright_red italic]Очистить папки [/bright_red italic]\n"
        "[cyan bold]Select: [/cyan bold] ",
        end="",
    )

    choiced = input()

    while choiced not in ["1", "2", "3"]:
        os.system("cls") if os.name == "nt" else os.system("clear")
        rich.print(
            "[bold]Меню[/bold]\n\n"
        "[bright_cyan]| 1 |[/bright_cyan] [bright_red italic] C session в tdata [/bright_red italic]\n"
        "[bright_cyan]| 2 |[/bright_cyan] [bright_red italic] C tdata в session [/bright_red italic]\n"
        "[bright_cyan]| 3 |[/bright_cyan] [bright_red italic] Очистить папки [/bright_red italic]\n"
        "[cyan bold]Select: [/cyan bold] ",
            end="",
        )

    if choiced == "1":
        await SessionToTData()

    elif choiced == "2":
        await TDataToSession()

    elif choiced == "3":
        clear()

        os.system("cls") if os.name == "nt" else os.system("clear")
        rich.print("[bold]Очищено[/bold]")
        await main()
#________________________________#

if __name__ == "__main__":
    #check()
    asyncio.run(main())
    print("Успешно.")
    
